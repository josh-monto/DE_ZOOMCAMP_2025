import os
from google.cloud import storage
import time


#Change this to your bucket name
BUCKET_NAME = "kestra-zm-448523-bucket"  

#If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "keys/my-creds.json"  
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

file_path = "yellow_tripdata_2024.parquet"

CHUNK_SIZE = 8 * 1024 * 1024  

bucket = client.bucket(BUCKET_NAME)

def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE  
    
    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")
            
            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
        
        time.sleep(5)  
    
    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    upload_to_gcs(file_path)

    print("File processed and verified.")