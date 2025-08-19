from imagekitio import ImageKit
import os
import base64
from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException, status
import uuid
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

load_dotenv()

imageKit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL_ENDPOINT"),
)


async def upload_profile_img(profile_img: UploadFile) -> str | None:
    if not profile_img or not profile_img.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No image provided."
        )

    if profile_img.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format."
        )

    image_content = await profile_img.read()

    if not image_content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    file_b64 = base64.b64encode(image_content).decode("utf-8")

    ext = profile_img.filename.rsplit(".", 1)[-1].lower()
    image_name = f"profile_{uuid.uuid4().hex}.{ext}"

    try:
        result = imageKit.upload_file(
            file=file_b64,
            file_name=image_name,
            options=UploadFileRequestOptions(
                tags=["users", "profiles"],
                folder="users/profile",
                response_fields=["is_private_file", "tags"],
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
    return result.url
