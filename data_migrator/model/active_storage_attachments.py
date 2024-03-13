from django.db import models

from data_migrator.model.active_storage_blobs import ActiveStorageBlobs
from data_migrator.model.commerce_product_variant import CommerceProductVariants


class ActiveStorageAttachments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    record_type = models.CharField(max_length=255)
    record_id = models.ForeignKey(CommerceProductVariants, models.DO_NOTHING, db_column='record_id')
    blob = models.ForeignKey(ActiveStorageBlobs, models.DO_NOTHING,db_column='blob_id')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        app_label = "read_replica"
        db_table = 'active_storage_attachments'
        unique_together = (('record_type', 'record_id', 'name', 'blob'),)
