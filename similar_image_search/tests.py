import json

from rest_framework import status
from rest_framework.test import APITestCase


class ProductStatusAPITestCase(APITestCase):
    def test_valid_payload_serialization(self):
        # Valid payload data
        data = {
            "payload": {
                "product_id": {
                    "1": [1234, 2345, 2345],
                    "2": [],
                    "3": []
                }
            }
        }

        # Serialize the data
        response = self.client.post('search/updateStatus/', data=json.dumps(data), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the serialized data in the response
        expected_response_data = {"message": "Status updated successfully"}
        self.assertEqual(response.data, expected_response_data)

    def test_invalid_payload_serialization(self):
        # Invalid payload data (missing 'payload' key)
        data = {
            "invalid_key": {
                "product_id": {
                    "1": [1234, 2345, 2345],
                    "2": [],
                    "3": []
                }
            }
        }

        # Serialize the data
        response = self.client.post('search/updateStatus/', data=json.dumps(data), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message in the response
        expected_response_data = {"errors": {"payload": ["This field is required."]}}
        self.assertEqual(response.data, expected_response_data)
