# tasks.py
import json
import logging
import random
import time

from data_migrator.model.active_storage_attachments import ActiveStorageAttachments
from data_migrator.model.commerce_product_variant import CommerceProductVariants
from django.db.models import OuterRef, Subquery, Q
from django.core.paginator import Paginator, EmptyPage
from constant import KAFKA_MIGRATION_TOPIC

logger = logging.getLogger(__name__)
MAX_RETRIES = 3  # Maximum number of retries for processing a variant data
BASE_DELAY = 1  # Base delay in seconds for exponential backoff


def get_variants_data(page):
    return (
            ActiveStorageAttachments.objects
            .select_related('blob', 'record_id')
            .filter(record_type='Commerce::ProductVariant', name='images')
            .order_by('created_at')
            .values('id', 'blob_id', 'blob__key', 'record_id__id', 'record_id__erp_code', 'record_id__status',
                    'record_id__product_id')
        )[page.start_index() - 1:page.end_index()]


def get_variant_data_querySet():
    queryset = (
            ActiveStorageAttachments.objects
            .select_related('blob', 'record_id')
            .filter(record_type='Commerce::ProductVariant', name='images')
            .order_by('created_at')
            .values('id', 'blob_id', 'blob__key', 'record_id__id', 'record_id__erp_code', 'record_id__status',
                    'record_id__product_id')
        )

    # Get the count for the entire query
    return queryset


# We are processing the variant data we pulled from Read Replica database and sending it to Kafka queue
def process_variant_data(variant_data, message_producer):
    success_count = 0
    failed_offset = None
    retries = 0
    while retries < MAX_RETRIES:
        try:
            formatted_data = {
                'product_variant_id': variant_data['record_id__id'],
                'product_id': variant_data['record_id__product_id'],
                'image_id': variant_data['blob_id'],
                's3_key': variant_data['blob__key'],
                'status': variant_data['record_id__status'],
                'product_erp_code': variant_data['record_id__erp_code']
            }
            # Produce variant data to the message queue
            message_producer.produce_message(KAFKA_MIGRATION_TOPIC,
                                             json.dumps(formatted_data).encode('utf-8'))

            success_count += 1
            logger.debug(f"Message send to message producer which has blob_id:{variant_data['blob_id']}")
            break  # Break out of the retry loop if successful

        except Exception as e:
            logger.error(f"Error processing variant data: {e}")
            # In the failed Offset we are storing the image_id which failed and logging it.
            failed_offset = variant_data['blob_id']
            retries += 1

            # Calculate exponential backoff delay
            delay = BASE_DELAY * (2 ** retries) + random.uniform(0, 0.1)  # Add some jitter
            logger.warning(f"Retrying processing variant data. Retry attempt: {retries}, Delay: {delay} seconds")
            time.sleep(delay)

    return success_count, failed_offset


def migrate_variant_data_sync(last_successful_page, chunk_size, message_producer):

    try:
        page_number = last_successful_page + 1
        # Remove the second condition for if
        while True and page_number < 2:
            try:
                success_count = 0
                failure_count = 0
                failed_offsets = []
                queryset = get_variant_data_querySet()
                paginator = Paginator(queryset, 1)
                page = paginator.page(page_number)
                variants_data = get_variants_data(page)

                for variant_data in variants_data:
                    success, failed_offset = process_variant_data(variant_data, message_producer)
                    success_count += success
                    failure_count += 1 if failed_offset is not None else 0
                    if failed_offset is not None:
                        failed_offsets.append(failed_offset)
                    logger.info(
                        f"Variant data migration done for {chunk_size} records. Success count: {success_count}, Failure "
                        f"count: {failure_count}, 'failed_offsets': {failed_offsets}")

                page_number += 1;
            except EmptyPage:
                break

    except Exception as e:
        logger.error(f"Error in migrate_variant_data_sync: {e}")
        raise
