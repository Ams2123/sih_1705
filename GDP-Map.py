from village_info import *
import streamlit as st
import zipfile
import io
import os
from PIL import Image
import plotly.express as px

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

def list_files_in_directory(files, directory):
    """List files in a specific directory from the extracted files."""
    return [file for file in files.keys() if file.startswith(directory + '/')]

def combine_images(images):
    """Combine a list of images with overlapping regions."""
    base_image = images[0].convert("RGBA")
    for img in images[1:]:
        img = img.convert("RGBA")
        base_image = Image.alpha_composite(base_image, img)
    return base_image.convert("RGB")

st.title('ZIP File Upload and Check for .gdb Folder')

uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

if uploaded_file:
    # Extract the ZIP file
    extracted_files = extract_zip(uploaded_file, os.getcwd())
    
    # Check for .gdb folder
    gdb_files = [file for file in extracted_files.keys() if ".gdb" in file]
    gdb_folders = set(os.path.dirname(file) for file in gdb_files)
    
    if gdb_folders:
        st.write("Found .gdb folder. Checking layers...")
        # Assuming the first .gdb file is what you want to use
        gdb_file = gdb_files[0][:-1]  # Adjust if necessary
        village = village_info(gdb_file, *gdb_file.split('/')[-1].split('_')[1].split(".")[:-1])
        layers = village.layers_available()
        
        if layers:
            # Display checkboxes for all available layers
            selected_layers = []
            for layer in layers:
                if st.checkbox(layer, key=layer):
                    selected_layers.append(layer)
            
            # Generate and display the map based on selected layers
            if selected_layers:
                st.write("Building map with selected layers...")

                st.write(village.house_info(selected_layers[0]))
                st.write(village.road_info(selected_layers[0]))
                # Check if more than one layer is selected
                if len(selected_layers) > 1:
                    fig = village.graph_gen_multiple(selected_layers)
                    st.plotly_chart(fig)
                else:
                    # Use pic_gen for a single layer
                    fig = village.graph_gen(selected_layers[0])
                    st.plotly_chart(fig)
               
                
                
            else:
                st.write("No layers selected. Please select at least one layer.")
        else:
            st.write("No layers available in the .gdb folder.")
    else:
        st.write("No .gdb folder found in the ZIP archive.")
