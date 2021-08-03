import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError

IMAGES_URL = os.environ['IMAGES_URL']
IMAGES_START = int(os.environ['IMAGES_START'])
IMAGES_END = int(os.environ['IMAGES_END'])

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
SERVICE_POINT = 'http://' + os.environ['SERVICE_POINT'] + ':' + os.environ['SERVICE_POINT_PORT']
BUCKET_NAME = os.environ['BUCKET_NAME']

s3client = boto3.client('s3','us-east-1', endpoint_url=SERVICE_POINT,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3client.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

seq = list(range(IMAGES_START, IMAGES_END))
for index, value in enumerate(seq, start=1) :
    v = str(value)
    r = requests.get(IMAGES_URL + v + '.png', allow_redirects=True)
    open('/tmp/' + v + '.png', 'wb').write(r.content)
    uploaded = upload_to_aws('/tmp/' + v + '.png', BUCKET_NAME, 'images/' + v + '.png')
    if uploaded :
        print('Uploaded ' + v + '.png to bucket ' + BUCKET_NAME)
    else :
        print('Could not upload ' + v + '.png to bucket ' + BUCKET_NAME)

images=[]
for image in s3client.list_objects(Bucket=BUCKET_NAME,Prefix='images/')['Contents']:
    images.append(image['Key'])
print('Uploaded images: ' + str(images))
