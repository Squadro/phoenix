# tasks.py
import json
import logging
import random
import time

from data_migrator.model.active_storage_attachments import ActiveStorageAttachments
from data_migrator.model.commerce_product_variant import CommerceProductVariants
from django.db.models import OuterRef, Subquery, Q

logger = logging.getLogger(__name__)
MAX_RETRIES = 3  # Maximum number of retries for processing a variant data
BASE_DELAY = 1  # Base delay in seconds for exponential backoff


def get_variants_data(offset, chunk_size):
    print("get_variants_data function")
    return CommerceProductVariants.objects.annotate(
        blob_id=Subquery(
            ActiveStorageAttachments.objects.filter(
                record_type='Commerce::ProductVariant',
                blob__id=OuterRef('id'),
                name='images'
            ).order_by('created_at').values('blob_id')[:1]
        ),
        s3_key=Subquery(
            ActiveStorageAttachments.objects.filter(
                record_type='Commerce::ProductVariant',
                blob__id=OuterRef('id'),
                name='images'
            ).order_by('created_at').values('blob__key')[:1]
        )
    ).filter(
        Q(is_default=True) | Q(blob_id__isnull=False)
    ).values(
        'id', 'product_id', 'erp_code', 'status', 'blob_id', 's3_key'
    )[offset:offset + chunk_size]


# We are processing the variant data we pulled from Read Replica database and sending it to Kafka queue
def process_variant_data(variant_data, message_producer):
    success_count = 0
    failed_offset = None
    retries = 0

    while retries < MAX_RETRIES:
        try:
            formatted_data = {
                'product_variant_id': variant_data['id'],
                'product_id': variant_data['product_id'],
                'image_id': variant_data['blob_id'],
                's3_key': variant_data['s3_key'],
                'status': variant_data['id'],
                'product_erp_code': variant_data['erp_code']
            }
            print(formatted_data)

            # Produce variant data to the message queue
            message_producer.produce_message('migration_messages',
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


def migrate_variant_data_sync(last_successful_offset, total_records, chunk_size, message_producer):
    try:
        offset = last_successful_offset
        while offset < total_records:
            success_count = 0
            failure_count = 0
            failed_offsets = []
            variants_data = get_variants_data(offset, chunk_size)
            for variant_data in variants_data:
                success, failed_offset = process_variant_data(variant_data, message_producer)
                success_count += success
                failure_count += 1 if failed_offset is not None else 0
                if failed_offset is not None:
                    failed_offsets.append(failed_offset)
                logger.info(
                    f"Variant data migration done for {chunk_size} records. Success count: {success_count}, Failure "
                    f"count: {failure_count}, 'failed_offsets': {failed_offsets}")

            offset += chunk_size

    except Exception as e:
        logger.error(f"Error in migrate_variant_data_sync: {e}")
        raise


def sync_operation():
    time.sleep(5)
    print("Sync Operation Completed")
