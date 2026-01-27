from minio.api import Minio

from src.core.config import settings

client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)
minio_client = client

BUCKET_INPUT_FILE = settings.INPUT_BUCKET
BUCKET_OUTPUT_FILE = settings.OUTPUT_BUCKET

def create_buckets():
    """
    Создает бакеты, если их нет
    """
    for bucket in [BUCKET_INPUT_FILE, BUCKET_OUTPUT_FILE]:
        is_existing = client.bucket_exists(bucket)
        if not is_existing:
            client.make_bucket(bucket_name=bucket)
            print("Created bucket", bucket)
        else:
            print("Bucket", bucket, "already exists")