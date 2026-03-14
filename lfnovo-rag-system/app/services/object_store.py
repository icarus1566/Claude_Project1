from minio import Minio
import io

class ObjectStoreService:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        # HTTP 통신을 위해 secure=False 처리 (개발/내부망 기준)
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name
        
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file_name: str, file_bytes: bytes) -> str:
        self.client.put_object(
            self.bucket_name,
            file_name,
            data=io.BytesIO(file_bytes),
            length=len(file_bytes)
        )
        return f"s3://{self.bucket_name}/{file_name}"
