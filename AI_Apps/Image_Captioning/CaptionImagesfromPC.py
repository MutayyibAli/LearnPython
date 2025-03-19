import glob
import os
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# Specify the directory containing the images
image_dir = "D:\\"
# Specify the image file extensions to search for
image_exts = ["jpg", "jpeg", "png"]
images = 0

with open("D:\\captions.txt", "w") as f:
    for image_ext in image_exts:
        # Stop after 10 images
        if images > 10:
            break
        images += 1

        # Get the image from directory
        for img_path in glob.glob(os.path.join(image_dir, f"*.{image_ext}")):
            # Load your image
            raw_image = Image.open(img_path).convert("RGB")

            # Process the image
            inputs = processor(raw_image, return_tensors="pt")

            # Generate a caption for the image
            out = model.generate(**inputs, max_length=50)

            # Decode the generated tokens to text
            caption = processor.decode(out[0], skip_special_tokens=True)
            print(caption)
            f.write(f"{os.path.basename(img_path)}: {caption}\n")
