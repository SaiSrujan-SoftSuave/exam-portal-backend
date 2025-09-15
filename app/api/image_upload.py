from fastapi import APIRouter, UploadFile, File, HTTPException, status
from minio import Minio
from minio.error import S3Error
from app.core.config import config
import io

router = APIRouter()

minio_client = Minio(
    config.MINIO_ENDPOINT,
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False  # Use True for HTTPS
)

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Check if bucket exists, if not, create it
        found = minio_client.bucket_exists(config.MINIO_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(config.MINIO_BUCKET_NAME)
        else:
            print(f"Bucket '{config.MINIO_BUCKET_NAME}' already exists")

        file_content = await file.read()
        object_name = file.filename

        minio_client.put_object(
            config.MINIO_BUCKET_NAME,
            object_name,
            io.BytesIO(file_content),
            len(file_content),
            content_type=file.content_type
        )
        return {"message": f"Successfully uploaded {object_name} to bucket {config.MINIO_BUCKET_NAME}"}
    except S3Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"MinIO S3 Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")