import zipfile
import io
import os

def extract_zip(file, output_dir):
    """Extract the ZIP file and return a dictionary of file names and their content."""
    extracted_files = {}
    with zipfile.ZipFile(file, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            # Read the file into memory
            with zip_ref.open(file_info.filename) as f:
                extracted_files[file_info.filename] = f.read()
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    return extracted_files