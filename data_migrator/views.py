# views.py

import asyncio

from django.http import JsonResponse
from data_migrator.tasks import migrate_variant_data_sync
from message_producer.kafka_producer import KafkaProducer
from data_migrator.tasks import get_variants_data
from constant import KAFKA_BOOTSTRAP_SERVERS

import logging

logger = logging.getLogger(__name__)

messageProducer = KafkaProducer(KAFKA_BOOTSTRAP_SERVERS)


async def migrate(request):
    try:

        # Start the asynchronous migration task
        last_successful_offset = 0
        total_records = 10
        chunk_size = 10
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, migrate_variant_data_sync, last_successful_offset, total_records, chunk_size,
                             messageProducer)
        print("{'status': 'Variant data migration started successfully'}, status = 201")

        # Respond with 201 status and task ID
        return JsonResponse({'status': 'Variant data migration started successfully'}, status=201)

    except Exception as e:
        logger.error(f"Error in migrate: {e}")
        return JsonResponse({'error': 'Failed to start variant data migration'}, status=500)


def check(request):
    variant_data = get_variants_data(10, 10)
    for data in variant_data:
        print(data)
