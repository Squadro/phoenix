from django.db import models
from pgvector.django import VectorField


class ImageEmbedding(models.Model):
    image_s3_key = models.CharField(max_length=255)
    image_embedding = VectorField()
    image_id = models.IntegerField(primary_key=True)
