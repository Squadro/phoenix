from django.db import models


class ProductVariantInformation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    variant_erp_code = models.CharField(max_length=255, blank=True, null=True)
    variant_status = models.IntegerField(blank=True, null=True)
    variant_product_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_variant_information'
        app_label = "default"

    def __str__(self):
        return (f"Product Variant Information - Id=  {self.id} ,  ERP Code = {self.variant_erp_code},"
                f"Product Id = {self.variant_product_id}, Status = {self.variant_status} ")
