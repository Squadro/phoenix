from rest_framework import serializers


class SearchImagesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    image_id = serializers.IntegerField(required=True)


class SearchImagesForTextSerializer(serializers.Serializer):
    data = serializers.CharField(required=True)
