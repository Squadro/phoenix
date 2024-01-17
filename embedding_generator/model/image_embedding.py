from django.db import models
from pgvector.django import VectorField


class ImageEmbedding(models.Model):
    s3_key = models.CharField(max_length=255)
    embedding = VectorField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'image_embeddings'
        app_label = "default"

    def __str__(self):
        return f"ImageEmbedding - {self.s3_key}"
