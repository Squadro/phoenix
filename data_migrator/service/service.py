# services.py - Service Layer

import json
import logging
import random
import time

from django.core.paginator import EmptyPage

from constant import KAFKA_MIGRATION_TOPIC, MAX_RETRIES, BASE_DELAY
from data_migrator.database.repository import VariantRepository

logger = logging.getLogger(__name__)


class MigrationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MigrationService, cls).__new__(cls)
            cls._instance.variant_repository = VariantRepository()
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True

    @staticmethod
    def process_variant_data(variant_data, message_producer):
        success_count = 0
        failed_offset = None
        retries = 0
        while retries < MAX_RETRIES:
            try:
                formatted_data = {
                    "product_variant_id": variant_data["record_id__id"],
                    "product_id": variant_data["record_id__product_id"],
                    "image_id": variant_data["blob_id"],
                    "s3_key": variant_data["blob__key"],
                    "status": variant_data["record_id__status"],
                    "product_erp_code": variant_data["record_id__erp_code"],
                }
                # Produce variant data to the message queue
                message_producer.produce_message(
                    KAFKA_MIGRATION_TOPIC, json.dumps(formatted_data).encode("utf-8")
                )

                success_count += 1
                logger.debug(
                    f"Message send to message producer which has blob_id:{variant_data['blob_id']}"
                )
                break  # Break out of the retry loop if successful

            except Exception as e:
                logger.error(f"Error processing variant data: {e}")
                # In the failed Offset we are storing the image_id which failed and logging it.
                failed_offset = variant_data["blob_id"]
                retries += 1

                # Calculate exponential backoff delay
                delay = BASE_DELAY * (2**retries) + random.uniform(
                    0, 0.1
                )  # Add some jitter
                logger.warning(
                    f"Retrying processing variant data. Retry attempt: {retries}, Delay: {delay} seconds"
                )
                time.sleep(delay)

        return success_count, failed_offset

    def migrate_variant_data_sync(self, message_producer):
        try:
            chunk_size = 1
            last_successful_page = self.variant_repository.get_last_successful_page()
            page_number = last_successful_page + 1

            while True and page_number < 2:
                try:
                    success_count = 0
                    failure_count = 0
                    failed_offsets = []

                    variants_data = self.variant_repository.get_variants_data(
                        page_number, chunk_size
                    )

                    for variant_data in variants_data:
                        success, failed_offset = self.process_variant_data(
                            variant_data, message_producer
                        )
                        success_count += success
                        failure_count += 1 if failed_offset is not None else 0
                        if failed_offset is not None:
                            failed_offsets.append(failed_offset)

                        logger.info(
                            f"Variant data migration done for {chunk_size} records. Success count: {success_count}, "
                            f"Failure count: {failure_count}, 'failed_offsets': {failed_offsets}"
                        )

                    page_number += 1

                except EmptyPage:
                    break

        except Exception as e:
            logger.error(f"Error in migrate_variant_data_sync: {e}")
            raise
