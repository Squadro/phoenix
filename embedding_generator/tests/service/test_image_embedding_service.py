from unittest.mock import patch, MagicMock

import pytest
import requests

# Assuming constant.py is in the same directory as image_embedding_service.py
from embedding_generator.service.image_embedding_service import (
    ImageEmbeddingService,
)  # Corrected import
from phoenix.settings_dev import *  # noqa


@pytest.fixture
def mock_dependencies():
    with (
        patch(
            "embedding_generator.service.image_embedding_service.EmbeddingProcessor"
        ) as mock_embedding_processor,
        patch(
            "embedding_generator.service.image_embedding_service.EmbeddingRepository"
        ) as mock_embedding_repository,
        patch(
            "embedding_generator.service.image_embedding_service.DataProcessingService"
        ) as mock_data_processor,
        patch(
            "embedding_generator.service.image_embedding_service.requests.get"
        ) as mock_requests_get,
    ):
        yield mock_embedding_processor, mock_embedding_repository, mock_data_processor, mock_requests_get


def test_process_images_success(mock_dependencies):
    (
        mock_embedding_processor,
        mock_embedding_repository,
        mock_data_processor,
        mock_requests_get,
    ) = mock_dependencies

    # Mock data
    message = {"s3_key": "/path/to/image.jpg"}

    # Set up mocks
    mock_data_processor_instance = mock_data_processor.return_value
    mock_data_processor_instance.process_data.return_value = message

    mock_embedding_processor_instance = mock_embedding_processor.return_value
    mock_embedding_processor_instance.create_embedding.return_value = "fake_embedding"

    mock_repository_instance = mock_embedding_repository.return_value

    # Mock successful image download response
    mock_requests_get.return_value.raise_for_status.return_value = None
    mock_requests_get.return_value.content = b"fake_image_data"

    # Create ImageEmbeddingService instance
    image_embedding_service = ImageEmbeddingService()

    # Call the method to be tested
    image_embedding_service.process_images(message)

    # Assert that methods were called with the correct arguments
    mock_data_processor_instance.process_data.assert_called_once_with(message)
    mock_embedding_processor_instance.create_embedding.assert_called_once_with(
        b"fake_image_data"
    )
    mock_repository_instance.save_embedding.assert_called_once_with(
        message, "fake_embedding"
    )


def test_download_image_error():
    mock_requests_get = MagicMock()
    mock_requests_get.side_effect = requests.exceptions.RequestException("Mocked error")

    with pytest.raises(requests.exceptions.RequestException):
        ImageEmbeddingService.download_image("https://example.com/image.jpg")


def test_process_images_error(mock_dependencies):
    _, _, _, mock_requests_get = mock_dependencies

    # Mock data
    message = {"s3_key": "/path/to/image.jpg"}

    # Create ImageEmbeddingService instance
    image_embedding_service = ImageEmbeddingService()

    # Mock error during image download
    mock_requests_get.side_effect = requests.exceptions.RequestException("Mocked error")

    # Call the method to be tested
    with pytest.raises(requests.exceptions.RequestException):
        image_embedding_service.process_images(message)
