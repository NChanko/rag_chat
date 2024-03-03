import os
import zipfile

def check_and_unzip_medical_db():
    # Define the path to the medical_db folder and the zip file
    db_folder_path = './medical_db'
    zip_file_path = 'medical_db.zip'
    
    # Check if the medical_db folder exists
    if not os.path.exists(db_folder_path):
        print(f"'{db_folder_path}' not found. Unzipping '{zip_file_path}'...")
        
        # Ensure the ZIP file exists
        if os.path.exists(zip_file_path):
            # Unzip the medical_db.zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('.')  # Extract to the current directory
            print(f"Unzipped '{zip_file_path}' successfully.")
        else:
            print(f"Error: The zip file '{zip_file_path}' does not exist.")
    else:
        print(f"'{db_folder_path}' already exists.")
