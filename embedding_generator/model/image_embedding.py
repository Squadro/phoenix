from django.db import models
from pgvector.django import VectorField


class ImageEmbedding(models.Model):
    image_s3_key = models.CharField(max_length=255)
    image_embedding = VectorField()
    image_id = models.IntegerField(primary_key=True)

    # class Meta:
    #     managed = False
    #     db_table = "image_embeddings"
    #     app_label = "default"
    #
    # def __str__(self):
    #     return f"ImageEmbedding - {self.image_s3_key}"
