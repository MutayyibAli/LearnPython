import requests
import gradio as gr
from PIL import Image
from io import BytesIO
from transformers import AutoProcessor, BlipForConditionalGeneration
from bs4 import BeautifulSoup

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def caption_images(url):
    # Download webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all image tags
    imgs = soup.find_all("img")
    captions = []
    images = 0
    for img in imgs:
        # Stop after 10 images
        if images > 10:
            break
        images += 1

        # Get the image URL
        img_url = img["src"]

        # Skip if the image is an SVG or too small (likely an icon)
        if "svg" in img_url or "1x1" in img_url:
            continue

        # Correct the URL if it's malformed
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif not img_url.startswith("http://") and not img_url.startswith("https://"):
            continue  # Skip URLs that don't start with http:// or https://
        try:
            # Download the image
            response = requests.get(img_url)
            # Convert the image data to a PIL Image
            raw_image = Image.open(BytesIO(response.content))
            if raw_image.size[0] * raw_image.size[1] < 400:  # Skip very small images
                continue

            raw_image = raw_image.convert("RGB")

        except Exception as e:
            print(f"Error processing image {img_url}: {e}")
            continue
        # Convert numpy array to PIL Image and convert to RGB
        raw_image = raw_image.convert("RGB")

        # Process the image
        inputs = processor(raw_image, return_tensors="pt")

        # Generate a caption for the image
        out = model.generate(**inputs, max_length=50)

        # Decode the generated tokens to text
        caption = processor.decode(out[0], skip_special_tokens=True)

        captions.append(caption)

    return str(captions)


iface = gr.Interface(
    fn=caption_images,
    inputs="text",
    outputs="text",
    title="Image Captioning",
    description="This is a simple web app for generating captions for images using a trained model.",
)

iface.launch(server_name="127.0.0.1", server_port=8080)
