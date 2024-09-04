# to run - streamlit run file.py --server.maxUploadSize 500

import streamlit as st
import zipfile

def extract_zip(file):
    """ Extract the ZIP file and return a dictionary of .ecw file names and their content. """
    extracted_files = {}
    with zipfile.ZipFile(file, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.ecw'):  # Only process .ecw files
                with zip_ref.open(file_info.filename) as f:
                    extracted_files[file_info.filename] = f.read()
    return extracted_files

st.title('ZIP File Upload and .ecw File Selection')

uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

if uploaded_file:
    # Unzip the file and get a dictionary of .ecw file names and their contents
    ecw_files = extract_zip(uploaded_file)

    # Display the names of the .ecw files
    if ecw_files:
        st.write("Available .ecw files in the ZIP archive:")

        # Use st.radio to let the user select one .ecw file
        selected_file = st.radio(
            "Choose one of the .ecw files:",
            options=list(ecw_files.keys())
        )

        if selected_file:
            st.write(f"You selected: {selected_file}")

            # Optionally display file contents or do something with it
            # Note: Displaying binary files directly may not be useful; this is just an example

    else:
        st.write("No .ecw files found in the ZIP archive.")

