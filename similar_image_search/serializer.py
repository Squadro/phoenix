from rest_framework import serializers


class SearchImagesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    image_id = serializers.IntegerField(required=True)


class SearchImagesForTextSerializer(serializers.Serializer):
    data = serializers.CharField(required=True)


class StatusSerializer(serializers.Serializer):
    product_id_status = serializers.JSONField()
    product_variant_id_status = serializers.JSONField()

    def validate_product_id_status(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid data structure for product_id_status.")

        for status, product_list in value.items():
            if not isinstance(product_list, list) or not product_list:
                raise serializers.ValidationError(f"Product list for status {status} cannot be empty.")

        return value

    def validate_product_variant_id_status(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid data structure for product_variant_id_status.")

        for status, product_list in value.items():
            if not isinstance(product_list, list) or not product_list:
                raise serializers.ValidationError(f"Product Variant list for status {status} cannot be empty.")

        return value

    # def validate_payload(self, value):
    #     valid_keys = {1, 2, 3}
    #     keys = set(value.keys())
    #
    #     if keys != valid_keys:
    #         raise serializers.ValidationError("Invalid product_id keys. Only 1, 2, and 3 are allowed.")
    #
    #     return value
