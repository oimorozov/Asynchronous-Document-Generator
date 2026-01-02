from minio.api import Minio

from src.config import settings

client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

BUCKET_INPUT_FILE="input-files-bucket"
BUCKET_OUTPUT_FILE="output-files-bucket"
BUCKETS = [BUCKET_INPUT_FILE, BUCKET_OUTPUT_FILE]

def create_buckets():
    """
    Создает бакеты, если их нет
    """
    for bucket in BUCKETS:
        isExisting = client.bucket_exists(bucket)
        if not isExisting:
            client.make_bucket(bucket_name=bucket)
            print("Created bucket", isExisting)
        else:
            print("Bucket", isExisting, "already exists")
