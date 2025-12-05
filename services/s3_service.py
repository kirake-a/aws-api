import os
from botocore.exceptions import ClientError
from fastapi import UploadFile
from config.aws_client import get_aws_client

class S3Service:
    def __init__(self):
        self.s3_client = get_aws_client('s3')
        self.bucket_name = os.getenv("AWS_BUCKET_NAME")

    def upload_file(self, file: UploadFile, file_name: str) -> str:
        """
        Uploads a file to S3 and returns the public URL.
        """
        try:
            # Upload the file
            # ExtraArgs={'ACL': 'public-read'} makes the file accessible via browser
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                file_name,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': file.content_type
                }
            )
            
            # Construct the public URL manually
            # Format: https://{bucket}.s3.{region}.amazonaws.com/{key}
            region = os.getenv("AWS_REGION")
            url = f"https://{self.bucket_name}.s3.{region}.amazonaws.com/{file_name}"
            
            return url
            
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            raise e