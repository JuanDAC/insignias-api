
from botocore.exceptions import ClientError
from boto3 import client
from app.core.config import settings

async def upload_file_to_s3(filename, file_data):
  s3_client = client("s3")
  bucket_name = settings.AWS_S3_BUCKET_NAME

  try:
    response = s3_client.put_object(
      Body=file_data, Bucket=bucket_name, Key=filename
    )
    return f"https://{bucket_name}.s3.amazonaws.com/{response['Location']}"
  except Exception as e:
      raise Exception(f"Error uploading file to S3: {str(e)}")
