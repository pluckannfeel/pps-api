import os, boto3, shutil, time
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from helpers.definitions import get_directory_path
from tempfile import NamedTemporaryFile

load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

client = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key)

# file upload
upload_path = get_directory_path() +  '\\uploads'


def upload_image_to_s3(imageFile, new_image_name):
    bucket_name = 'pps-bucket'
    object_name = 'uploads/'+ imageFile.filename
    print(new_image_name)
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = imageFile.file.read()
            with temp as f:
                f.write(contents)
        except ClientError as e:
            return {"message": "There was an error uploading the file. " + str(e)}
        finally:
            imageFile.file.close()
            
        # upload here
        client.upload_file(temp.name, bucket_name, object_name, ExtraArgs={"ACL": 'public-read-write', "ContentType": imageFile.content_type})
        
        #  rename s3 uploaded file
        client.copy_object(Bucket=bucket_name, CopySource=bucket_name + '/' + object_name, Key='uploads/' + new_image_name, ACL='public-read-write')
        
        # delete old file
        client.delete_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        return {"message": "There was an error processing the file."}
    finally:
        os.remove(temp.name)
        # print(contents)  # Handle file contents as desired
        return {"filename": imageFile.filename}