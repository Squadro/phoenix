from django.db import models
from pgvector.django import VectorField


# Create your models here.

class ImageEmbedding(models.Model):
    key = models.CharField(max_length=255)
    embedding = VectorField()

    def __str__(self):
        return f"ImageEmbedding - {self.key}"
