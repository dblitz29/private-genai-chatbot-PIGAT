# import requests
# import json
# import boto3

# def get_file_size(bucket_name, object_key):
#     """Fetches the size of a file in an S3 bucket."""
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id="04DLRFS9FHJJ5PCC83O1",
#         aws_secret_access_key="TCmd0S1xRRdCzHL7HWfE3xFqqyleIaFnOAQQN0ZH",
#         endpoint_url="https://s3-jkt1.dcloud.co.id"
#     )

#     try:
#         response = s3.head_object(Bucket=bucket_name, Key=object_key)
#         return response["ContentLength"]
#     except Exception as e:
#         print(f"Error getting file size: {e}")
#         return None

# if __name__ == "__main__":
#     url = "https://sanggar.cloudciti.io/v9/dbaas/backup/MWZhM2M5YzktMjc0Ni00MGE3LWIxZmEtNDdiOWE1NGQwNzUy/validateBackup"
#     headers = {
#         "Accept": "*/*",
#         "User-Agent": "Thunder Client (https://www.thunderclient.com)",
#         "Content-Type": "application/json",
#     }
#     s3_bucket = "test-terminated-staging-4bxka" 
#     filename = "test-terminated-staging-4bxka-2024-07-10" + ".tgz"
#     file_size = get_file_size(s3_bucket, filename)

#     if file_size:
#         print(f"The size of '{filename}' in bucket '{s3_bucket}' is: {file_size} bytes")
    


#     payload = {
#         "status": "success",
#         "path": "s3://test-terminated-staging-4bxka/",
#         "message": "",
#         "file_name": "test-terminated-staging-4bxka-2024-07-10",
#         "size": file_size,
#     }

#     response = requests.get(url, headers=headers, json=payload)
#     result = response.json()

#     print(result)


# ===================================================================================================

import requests
import json
import boto3

def get_file_size(bucket_name, object_key):
    """Fetches the size of a file in an S3 bucket."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id="04DLRFS9FHJJ5PCC83O1",
        aws_secret_access_key="TCmd0S1xRRdCzHL7HWfE3xFqqyleIaFnOAQQN0ZH",
        endpoint_url="https://s3-jkt1.dcloud.co.id"
    )

    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        return response["ContentLength"]
    except Exception as e:
        print(f"Error getting file size: {e}")
        return None

if __name__ == "__main__":
    url = "https://sanggar.cloudciti.io/v9/dbaas/backup/MWZhM2M5YzktMjc0Ni00MGE3LWIxZmEtNDdiOWE1NGQwNzUy/validateBackup"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/json",
    }
    s3_bucket = data['bucket_name']
    filename = data['file_name'] + ".tgz"
    file_size = get_file_size(s3_bucket, filename)

    payload = {
        "status": "success",
        "path": "s3://test-terminated-staging-4bxka/",
        "message": "",
        "file_name": "test-terminated-staging-4bxka-2024-07-10",
        "size": file_size,
    }

    response = requests.get(url, headers=headers, json=payload)
    result = response.json()

    print(result)
