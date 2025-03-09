from transformers import BlipProcessor, TFBlipForConditionalGeneration
from PIL import Image
import tensorflow as tf
import database

# Load TensorFlow-based BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = TFBlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_caption(image_path):
    # Check if caption exists in DB
    caption = database.get_caption(image_path)
    if caption:
        return caption

    # Process image & generate caption
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="tf")  # Use TensorFlow tensors
    caption_ids = model.generate(**inputs)
    
    # Decode the generated caption
    caption = processor.batch_decode(caption_ids, skip_special_tokens=True)[0]

    # Save to database
    database.insert_caption(image_path, caption)
    return caption


