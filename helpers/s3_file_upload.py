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

bucket_name = 'pps-bucket'

def upload_file_to_s3(file_object, app_type):
    if app_type == 'professional':
        object_name = 'uploads/pdf/professional/' + file_object.filename
    elif app_type == 'ssw':
        object_name = 'uploads/pdf/ssw/' + file_object.filename
    elif app_type == 'trainee':
        object_name = 'uploads/pdf/trainee/' + file_object.filename
    
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file_object.file.read()
            with temp as f:
                f.write(contents)
        except ClientError as e:
            return {"message": "There was an error uploading the file. " + str(e)}
        finally:
            file_object.file.close()
                        
        # upload here
        client.upload_file(temp.name, bucket_name, object_name, ExtraArgs={"ACL": 'public-read', "ContentType": file_object.content_type})
        
    except ClientError as e:
        return {"message": "There was an error processing the file.", "error": e}
    finally:
        os.remove(temp.name)
        # print(contents)  # Handle file contents as desired
        return {"filename": file_object.filename}

def upload_image_to_s3(imageFile, new_image_name):    
    object_name = 'uploads/img/'+ imageFile.filename
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
        client.upload_file(temp.name, bucket_name, object_name, ExtraArgs={"ACL": 'public-read', "ContentType": imageFile.content_type})
        
        #  rename s3 uploaded file
        client.copy_object(Bucket=bucket_name, CopySource=bucket_name + '/' + object_name, Key='uploads/img/' + new_image_name, ACL='public-read')
               
        # delete old file
        response = client.delete_object(
            Bucket=bucket_name,
            Key=object_name,
            )
        print('delete', response)
    except ClientError as e:
        return {"message": "There was an error processing the file.", "error": e}
    finally:
        os.remove(temp.name)
        # print(contents)  # Handle file contents as desired
        return {"filename": imageFile.filename}
