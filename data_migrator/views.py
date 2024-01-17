# views.py

import asyncio
import logging

from django.http import JsonResponse

from constant import KAFKA_BOOTSTRAP_SERVERS
from data_migrator.service.service import MigrationService
from message_producer.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

messageProducer = KafkaProducer(KAFKA_BOOTSTRAP_SERVERS)


async def migrate(request):
    try:
        # Start the asynchronous migration task
        migration_service = MigrationService()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(
            None,
            migration_service.migrate_variant_data_sync,
            messageProducer,
        )

        # Respond with 201 status and task ID
        return JsonResponse(
            {"status": "Variant data migration started successfully"}, status=201
        )

    except Exception as e:
        logger.error(f"Error in migrate: {e}")
        return JsonResponse(
            {"error": "Failed to start variant data migration"}, status=500
        )


# Have to Remove this code
# def check(request):
#      test()
