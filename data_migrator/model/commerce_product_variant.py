from django.db import models


class CommerceProductVariants(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    erp_code = models.CharField(max_length=255, blank=True, null=True)
    vendor_code = models.CharField(max_length=255, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mrp = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lead_days = models.IntegerField(blank=True, null=True)
    labour_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    default_unit_size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    old_product_variant_map_id = models.IntegerField(blank=True, null=True)
    labour_tax_category = models.IntegerField(blank=True, null=True)
    labour_charge_type = models.IntegerField(blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    is_partial = models.BooleanField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commerce_product_variants'
        app_label = "read_replica"
