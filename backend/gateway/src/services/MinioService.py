from fastapi import UploadFile

from minio.api import Minio

from src.core.minio.minio import client

class MinioService:
    def __init__(self, client: Minio):
        self.BUCKET_INPUT_FILE="input-files-bucket"
        self.BUCKET_OUTPUT_FILE="output-files-bucket"
        self.BUCKETS = [self.BUCKET_INPUT_FILE, self.BUCKET_OUTPUT_FILE]
    
    def create_buckets(self):
        """
        Создает бакеты, если их нет
        """
        for bucket in self.BUCKETS:
            isExisting = client.bucket_exists(bucket)
            if not isExisting:
                client.make_bucket(bucket_name=bucket)
                print("Created bucket", isExisting)
            else:
                print("Bucket", isExisting, "already exists")
    
    def save_obj(self, obj: UploadFile, bucket: str):
        """
        Кладёт в bucket объект
        """
        client.put_object(
            bucket_name=bucket,
            object_name=obj.filename,
            data=obj.file,
            length=obj.size,
            content_type=obj.content_type
        )


minioService = MinioService(client=client)