# myapp/dao.py
from django.core.exceptions import ObjectDoesNotExist

from embedding_generator.models import ImageEmbedding


class ImageEmbeddingDAO:
    @classmethod
    def save_embedding(cls, url, embedding):
        """
        Save the image embedding to the database.
        """
        image_embedding = ImageEmbedding.objects.create(key=url, embedding=embedding)
        return image_embedding

    @classmethod
    def get_embedding_by_url(cls, url):
        """
        Retrieve the image embedding from the database by URL.
        Returns None if not found.
        """
        try:
            return ImageEmbedding.objects.get(key=url).embedding
        except ObjectDoesNotExist:
            return None

    @classmethod
    def delete_embedding_by_url(cls, url) -> bool:
        """
        Delete the image embedding from the database by URL.
        Returns True if the deletion is successful, False otherwise.
        """
        try:
            ImageEmbedding.objects.get(key=url).delete()
            return True
        except ObjectDoesNotExist:
            return False
