# image_embedding_processor.py
from io import BytesIO
from PIL import Image
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizer
import torch
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = "openai/clip-vit-base-patch32"
        self.model, self.processor, self.tokenizer = self.get_model_info()

    def get_model_info(self):
        model = CLIPModel.from_pretrained(self.model_id).to(self.device)
        processor = CLIPProcessor.from_pretrained(self.model_id)
        tokenizer = CLIPTokenizer.from_pretrained(self.model_id)
        return model, processor, tokenizer

    def create_embedding(self, image_content):
        try:
            image_content = Image.open(BytesIO(image_content))
            image_input = self.processor(
                text=None,
                images=image_content,
                return_tensors="pt"
            )["pixel_values"].to(self.device)
            embedding = self.model.get_image_features(image_input)
            embedding_as_np = embedding.cpu().detach().numpy()
            return embedding_as_np.flatten()
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise
