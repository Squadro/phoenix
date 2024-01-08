from django.db import models

from data_migrator.model.active_storage_blobs import ActiveStorageBlobs


class ActiveStorageAttachments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    record_type = models.CharField(max_length=255)

    blob = models.ForeignKey(ActiveStorageBlobs, models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        app_label = "read_replica"
        db_table = 'active_storage_attachments'
        unique_together = (('record_type', 'record_id', 'name', 'blob'),)
