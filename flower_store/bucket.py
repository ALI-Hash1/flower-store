import boto3
from django.conf import settings


class Bucket:
    """CDN Bucket manager

    init method creates connection.

    NOTE:
        none of these methods are async. use public interface in tasks.py modules instead.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_object(self, file, key, content_type='image/png'):
        """
        Upload a file to ArvanCloud bucket

        اینطوری ما باید این تابع را صدا بزنیم: bucket.upload_object('/path/to/local/file.jpg', 'images/file.jpg')
        یا حالت دیگر اینکه جای اینکه مسیر فایل را در پارامتر اول بدهیم خود شیء باز شده فایل را بدهیم.
        """

        if isinstance(file, str):
            with open(file, 'rb') as f:
                file_data = f.read()
        else:
            file_data = file.read()

        self.conn.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key,
            Body=file_data,
            ContentType=content_type
        )
        return True


bucket = Bucket()
