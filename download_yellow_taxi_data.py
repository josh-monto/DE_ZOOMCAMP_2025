import os
import urllib.request

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
DOWNLOAD_DIR = "."

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


if __name__ == "__main__":
    for month in ['01','02','03','04','05','06']:
        download_file(month)

    print("All files downloaded")