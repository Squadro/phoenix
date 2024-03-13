from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse


class SearchViewTest(TestCase):
    def test_search_view_success(self):
        # Mock the SearchService to avoid actual database operations
        with patch("similar_image_search.views.SearchService") as mock_search_service:
            # Set up the mock service to return a success response
            mock_search_service.return_value.getSimilarImageSearchProductId.return_value = (
                "Some success response"
            )

            # Simulate an HTTP GET request to the view with parameters
            response = self.client.get(
                reverse("search"), {"productId": "123", "Image_id": "456"}
            )

            # Assert that the response is successful (HTTP 200)
            self.assertEqual(response.status_code, 200)

            # Assert that the response content matches the expected result
            self.assertEqual(
                response.content.decode(), "Product ID: 123, Image ID: 456"
            )

            # Assert that the SearchService method was called with the correct parameters
            mock_search_service.return_value.getSimilarImageSearchProductId.assert_called_once_with(
                "456", "123"
            )

    def test_search_view_missing_parameters(self):
        # Simulate an HTTP GET request to the view without required parameters
        response = self.client.get(reverse("search"))

        # Assert that the response is a bad request (HTTP 400)
        self.assertEqual(response.status_code, 400)

    def test_search_view_object_does_not_exist(self):
        # Mock the SearchService to raise ObjectDoesNotExist
        with patch("similar_image_search.views.SearchService") as mock_search_service:
            mock_search_service.return_value.getSimilarImageSearchProductId.side_effect = (
                ObjectDoesNotExist
            )

            # Simulate an HTTP GET request to the view with parameters
            response = self.client.get(
                reverse("search"), {"productId": "123", "Image_id": "456"}
            )

            # Assert that the response is a not found (HTTP 404)
            self.assertEqual(response.status_code, 404)
