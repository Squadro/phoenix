# repository.py - Database Layer

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F

from data_migrator.model.active_storage_attachments import ActiveStorageAttachments
from data_migrator.model.commerce_products import CommerceProducts
from data_migrator.model.last_successful_page import (
    LastSuccessfulPage,
)  # Import the LastSuccessfulPage model


class VariantRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VariantRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            # Your initialization logic here, if needed

    def get_variants_data(self, page_number, page_size):
        queryset = self.get_variant_data_query_set()

        paginator = Paginator(queryset, page_size)
        try:
            variants_data = paginator.page(page_number)
            distinct_product_ids = variants_data.object_list.values_list("record_id__product_id", flat=True).distinct()
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            variants_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            variants_data = paginator.page(paginator.num_pages)
            distinct_product_ids = variants_data.object_list.values_list("record_id__product_id", flat=True).distinct()
            if not variants_data.has_next():
                raise EmptyPage("The last page is empty.")

        # Store the last successful page after retrieving the data
        return variants_data

    @staticmethod
    def get_last_successful_page():
        last_successful_page = LastSuccessfulPage.objects.last()
        if last_successful_page:
            return last_successful_page.page_number
        else:
            return 0

    @staticmethod
    def store_last_successful_page(page_number):
        LastSuccessfulPage.objects.create(page_number=page_number)

    @staticmethod
    def get_product_data(product_ids):
        product_data = CommerceProducts.objects.filter(id__in=product_ids).values(
            id=F('id'),
            product_name=F('name'),
            product_description=F('description'),
            product_short_description=F('short_description'),
            product_erp_code=F('erp_code'),
            product_status=F('status'),
            product_category_id=F('product_category_id'),
            # Add other fields you need with the "product_" prefix
        )

        # Convert product_data to a dictionary for easy lookup
        product_data_dict = {product['id']: product for product in product_data}

        return product_data_dict

    @staticmethod
    def get_product_data_query_set():
        return (
            ActiveStorageAttachments.objects.select_related("blob", "record_id")
            .filter(record_type="Commerce::ProductVariant", name="images")
            .order_by("-created_at")
            .values(
                "id",
                "blob_id",
                "blob__key",
                "record_id__id",
                "record_id__name",
                "record_id__description",
                "record_id__erp_code",
                "record_id__status",
                "record_id__product_id",  # Include fields from CommerceProducts

            )
        )
