import requests
import zipfile
import os
def download_and_unzip(zip_url, extract_to):
    """
    Downloads a ZIP file from the specified URL and extracts it to the given directory.
    """
    extract_to = "./"
    # Download the ZIP file
    zip_path = './medical_db.zip'
    if not os.path.exists(zip_path):
        print(f"Downloading ZIP file from '{zip_url}'...")
        response = requests.get(zip_url)
        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)
        print("Download completed.")
    else:
        print("ZIP file already exists.")

    # Unzip the downloaded file
    print(f"Extracting '{zip_path}' to '{extract_to}'...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction completed.")

def db_check():
    zip_url = 'https://github.com/NChanko/rag_chat/blob/main/medical_db.zip?raw=true'
    db_folder_path = './medical_db'

    if not os.path.exists(db_folder_path):
        print(f"'{db_folder_path}' does not exist. Starting download and unzip process.")
        download_and_unzip(zip_url, db_folder_path)
    else:
        print(f"'{db_folder_path}' already exists.")

# Example usage
db_check()