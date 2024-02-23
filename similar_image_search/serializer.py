from rest_framework import serializers


class SearchImagesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    image_id = serializers.IntegerField(required=True)


class SearchImagesForTextSerializer(serializers.Serializer):
    data = serializers.CharField(required=True)


class ErpCodesSerializer(serializers.Serializer):
    erp_codes = serializers.ListField(
        child=serializers.CharField(), required=True, allow_empty=False
    )

    def validate_erp_codes(self, value):
        if not value:
            raise serializers.ValidationError("ERP codes cannot be empty.")
        return value


class StatusSerializer(serializers.Serializer):
    product_id_status = serializers.JSONField(required=False)
    product_variant_id_status = serializers.JSONField(required=False)

    ALLOWED_STATUSES = {0, 1, 2}

    def validate(self, data):
        product_id_status = data.get('product_id_status')
        product_variant_id_status = data.get('product_variant_id_status')

        if not product_id_status and not product_variant_id_status:
            raise serializers.ValidationError("Either 'product_id_status' or 'product_variant_id_status' must be "
                                              "present.")

        if product_id_status:
            self.validate_status_data(product_id_status, "product_id_status")

        if product_variant_id_status:
            self.validate_status_data(product_variant_id_status, "product_variant_id_status")

        return data

    def validate_status_data(self, status_data, field_name):
        if not isinstance(status_data, dict):
            raise serializers.ValidationError(f"Invalid data structure for {field_name}.")

        for status, product_list in status_data.items():
            if not isinstance(product_list, list) or not product_list:
                raise serializers.ValidationError(f"Product list for status {status} cannot be empty.")

            if int(status) not in self.ALLOWED_STATUSES:
                raise serializers.ValidationError(
                    f"Invalid status value {status}. Allowed values are {self.ALLOWED_STATUSES}.")
