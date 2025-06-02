import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_to_cloudinary(image_bytes, filename):

    result = cloudinary.uploader.upload(
        image_bytes,
        public_id=filename,
        folder="restaurants",
        overwrite=True,
        resource_type="image",
    )
    return result["secure_url"]
