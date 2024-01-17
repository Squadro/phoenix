import json
import logging
from io import BytesIO
from django.db import transaction, IntegrityError
from PIL import Image
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizer
from constant import CLOUDFRONT_URL
import torch
import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def process_images(message):
    # Download the image from CloudFront
    # {
    # 'product_variant_id': 16170,
    # 'product_id': 11725,
    # 'image_id': 2199,
    # 's3_key': 'cfXnfL6DCDdD4rfudEUyigKG',
    # 'status': 2,
    # 'product_erp_code': None
    # }
    embedding = download_image_and_create_embedding(CLOUDFRONT_URL + message['s3_key'])
    save_embedding_to_database(message, embedding)


def download_image_and_create_embedding(image_url):
    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        # Process the image and create an embedding
        return create_embedding(response.content)

        # Update the embedding field in the Django model


def get_model_info(model_id, device):
    # Save the model to device
    model = CLIPModel.from_pretrained(model_id).to(device)
    # Get the processor
    processor = CLIPProcessor.from_pretrained(model_id)
    # Get the tokenizer
    tokenizer = CLIPTokenizer.from_pretrained(model_id)
    # Return model, processor & tokenizer
    return model, processor, tokenizer


def create_embedding(image_content):
    # Load the CLIP model and processor
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_id = "openai/clip-vit-base-patch32"
    model, processor, tokenizer = get_model_info(model_id, device)

    # Open the image from BytesIO
    image_content = Image.open(BytesIO(image_content))

    # Encode the image using the CLIP processor
    image_input = processor(
        text=None,
        images=image_content,
        return_tensors="pt"
    )["pixel_values"].to(device)
    embedding = model.get_image_features(image_input)
    embedding_as_np = embedding.cpu().detach().numpy()
    return embedding_as_np.flatten()


def save_embedding_to_database(data, embedding):
    # Save the image embedding to the database with PgVector
    from message_consumer.models import ImageEmbedding, ProductVariantInformation, ProductImageRelation
    try:
        with transaction.atomic():
            # Insert data into ImageEmbedding table
            embedding_obj = ImageEmbedding.objects.create(
                s3_key=data['s3_key'],
                embedding=embedding,
                id=data['image_id']

            )

            # Insert data into ProductVariantInformation table
            variant_obj = ProductVariantInformation.objects.create(
                id=data['product_variant_id'],
                variant_erp_code=data.get('product_erp_code', ''),
                variant_status=data.get('status', 0),
                variant_product_id=data.get('product_id', None)
            )

            try:
                # Insert data into ProductImageRelation table
                relation_obj = ProductImageRelation.objects.create(
                    product_id=data['product_id'],
                    image_id=data['image_id']
                )
            except IntegrityError as e:
                # Log the IntegrityError
                logger.warning(f"IntegrityError: {e}")
                # Handle IntegrityError (e.g., print a message)

                pass

    except Exception as e:
        # Log the general exception
        logger.error(f"Error adding data: {e}")
        # Handle other exceptions (e.g., print a message)
