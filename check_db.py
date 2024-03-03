import requests
import zipfile
import io
import os

def download_and_unzip(zip_url, extract_to):
    # Attempt to download the ZIP file
    response = requests.get(zip_url)
    if response.status_code == 200:
        # Use a BytesIO object as a buffer for the ZIP file content
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # Extract the content to the specified directory
            zip_ref.extractall("./")
        print("File unzipped successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def db_check():
    # URL of the ZIP file
    zip_url = 'https://github.com/NChanko/rag_chat/blob/main/medical_db.zip?raw=true'
    # Local directory path
    db_folder_path = './medical_db'
    
    # Check if the db_folder_path exists, if not, download and unzip
    if not os.path.exists(db_folder_path):
        print(f"'{db_folder_path}' does not exist. Starting download and unzip process.")
        download_and_unzip(zip_url, db_folder_path)
    else:
        print(f"'{db_folder_path}' already exists.")