# from io import BytesIO
# from django.db import transaction
# from PIL import Image
# from transformers import CLIPModel, CLIPProcessor, CLIPTokenizer
# from constant import CLOUDFRONT_URL
# from embedding_generator.models import ImageEmbedding
# import torch
# import requests
#
#
# def process_images(message):
#     # Example image URLs (replace with your actual URLs)
#     print(type(message))
#     image_urls = ["Es9pbSSaTag4JKcyCSpPyNJF",
#                   "EcPazEun5GRDD9MJtzTDs4Jf",
#                   "nYkHLDmVTwRiA6snR1jaE2LB",
#                   "pUmHGFSDwggAv5NRPfRuT8Ft",
#                   "ZELCLZHcG3UqdYEJ72RRcs56",
#                   "qtAstDx7dRPm8z4gPUb6thkP",
#                   "TTzrMHuaypSct9ocXLx2ea9t",
#                   "LvZkCDdztWPHbVcUyjADPXQU",
#                   "hUg1NASAXQDpsVEAvqffJHqv",
#                   "2Kqv9t1cgNTucRWPWX5yAFca",
#                   "ub3GzJ8yT4ZBtpicX9ZzTaYv",
#                   "1K55GUdk7YNtA45UbPmSD7vt"]
#     image_urls1 = ["Es9pbSSaTag4JKcyCSpPyNJF"]
#
#     for image_url in image_urls1:
#         # Download the image from CloudFront
#         download_image_and_create_embedding(CLOUDFRONT_URL + image_url)
#
#
# def download_image_and_create_embedding(image_url):
#     # Download the image
#     response = requests.get(image_url)
#     if response.status_code == 200:
#         # Process the image and create an embedding
#         embedding = create_embedding(response.content)
#
#         # Update the embedding field in the Django model
#         print(embedding)
#
#
# def get_model_info(model_ID, device):
#     # Save the model to device
#     model = CLIPModel.from_pretrained(model_ID).to(device)
#     # Get the processor
#     processor = CLIPProcessor.from_pretrained(model_ID)
#     # Get the tokenizer
#     tokenizer = CLIPTokenizer.from_pretrained(model_ID)
#     # Return model, processor & tokenizer
#     return model, processor, tokenizer
#
#
# def create_embedding(image_content):
#     # Load the CLIP model and processor
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model_id = "openai/clip-vit-base-patch32"
#     model, processor, tokenizer = get_model_info(model_id, device)
#
#     # Open the image from BytesIO
#     image_content = Image.open(BytesIO(image_content))
#
#     # Encode the image using the CLIP processor
#     image_input = processor(
#         text=None,
#         images=image_content,
#         return_tensors="pt"
#     )["pixel_values"].to(device)
#     embedding = model.get_image_features(image_input)
#     embedding_as_np = embedding.cpu().detach().numpy()
#     return embedding_as_np.flatten()
#
#
# def save_embedding_to_database(image_url, embedding):
#     # Save the image embedding to the database with PgVector
#     with transaction.atomic():
#         ImageEmbedding.objects.create(url=image_url, embedding=embedding)
#         print(f"Image embedding for {image_url} saved to the database.")
