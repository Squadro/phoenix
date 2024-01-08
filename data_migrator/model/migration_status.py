# models.py

from django.db import models


class MigrationStatus(models.Model):
    id = models.AutoField(primary_key=True)
    last_successful_offset = models.IntegerField(default=0)

    def __str__(self):
        return f"MigrationStatus - Last Successful Offset: {self.last_successful_offset}"

    class Meta:
        managed = True
        db_table = 'migration_status'
        app_label = "default"
