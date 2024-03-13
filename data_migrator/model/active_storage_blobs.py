from django.db import models


class ActiveStorageBlobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(unique=True, max_length=255)
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    byte_size = models.BigIntegerField()
    checksum = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'active_storage_blobs'
        app_label = "read_replica"
