# views.py

import asyncio
import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.http import JsonResponse

from constant import KAFKA_BOOTSTRAP_SERVERS
from constant import getCurrentTime
from data_migrator.database.repository import VariantRepository
from data_migrator.model.active_storage_attachments import ActiveStorageAttachments
from data_migrator.model.commerce_products import CommerceProducts
from data_migrator.service.service import MigrationService
from message_producer.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)


async def migrate_images(request):
    try:
        # Start the asynchronous migration task
        message_producer = KafkaProducer(KAFKA_BOOTSTRAP_SERVERS)

        variant_repository = VariantRepository()
        migration_service = MigrationService(
            message_producer=message_producer, variant_repository=variant_repository
        )
        loop = asyncio.get_event_loop()
        loop.run_in_executor(
            None,
            migration_service.migrate_variant_data_sync,
        )
        logger.info(f"Migration Started time: {getCurrentTime()}")
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
def check(request):
    product_data = CommerceProducts.objects.values(
        product_id=F('id'),
        product_name=F('name'),
        product_description=F('description'),
        product_erp_code=F('erp_code'),
        product_status=F('status')
        # Add other fields you need with the "product_" prefix
    )

    q = (ActiveStorageAttachments.objects.select_related("blob", "record_id").
    filter(record_type="Commerce::ProductVariant", name="images").
    order_by("-created_at").values(
        "id",
        "blob_id",
        "blob__key",
        "record_id__id",
        "record_id__name",
        "record_id__description",
        "record_id__erp_code",
        "record_id__status",
        product_id=F("record_id__product_id"),  # Include fields from CommerceProducts

    ))

    combined_queryset = product_data.filter(product_id__isnull=False).union(
        q.filter(product_id__isnull=False)
    )[:2]

    # Convert product_data to a dictionary for easy lookup

    # Fetch commerce product names with relevant product data

    # Convert to a list for JSON serialization
    product_names_list = list(combined_queryset)

    # Serialize the list to JSON
    json_data = json.dumps(product_names_list, cls=DjangoJSONEncoder)

    # Use JsonResponse to return JSON in a Django view or API endpoint
    return JsonResponse({'product_names': json_data})
