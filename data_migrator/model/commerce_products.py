from django.db import models


class CommerceProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    erp_code = models.CharField(max_length=255, blank=True, null=True)
    vendor_code = models.CharField(max_length=255, blank=True, null=True)
    transportation_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    transportation_charge_type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    unit = models.IntegerField(blank=True, null=True)
    order_type = models.IntegerField(blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    tax_category = models.IntegerField(blank=True, null=True)
    view_type = models.IntegerField(blank=True, null=True)
    backend_product_type = models.IntegerField(blank=True, null=True)
    old_product_map_id = models.IntegerField(blank=True, null=True)
    product_template_id = models.BigIntegerField(blank=True, null=True)
    account_id = models.BigIntegerField(blank=True, null=True)
    product_category_id = models.BigIntegerField(blank=True, null=True)
    product_brand_id = models.BigIntegerField(blank=True, null=True)
    stage_template_id = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    labour_charges_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_editable = models.BooleanField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commerce_product_variants'
        app_label = "read_replica"
