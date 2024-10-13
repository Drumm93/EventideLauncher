import boto3
from botocore.client import Config
import os

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

BUCKET_NAME = 'eventide'
OBJECT_KEY = 'Eventide.rar'

def create_presigned_url(bucket_name, object_key, expiration=43200):
    """Generate a pre-signed URL for an S3 object."""
    s3_client = boto3.client('s3',
                             endpoint_url='https://s3.us-central-1.wasabisys.com',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY,
                             config=Config(signature_version='s3v4'))
    
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_key},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None
    
    return response

if __name__ == "__main__":
    presigned_url = create_presigned_url(BUCKET_NAME, OBJECT_KEY)
    if presigned_url:
        with open('download_link.txt', 'w') as f:
            f.write(presigned_url)
            print("Pre-signed URL successfully written to download_link.txt")
