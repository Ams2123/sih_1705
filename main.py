import streamlit as st
import zipfile
import io
import os
from GDBMAPPING import *
from PIL import Image
import plotly.express as px
from village_info import *

def home():
    st.title("Upload the .zip file which contaisn the .ecw file \
            and .gdb file(optional)")

    uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

    if uploaded_file:
        # Extract the ZIP file
        extracted_files = extract_zip(uploaded_file, os.getcwd())
        
        # Check for .gdb folder
        gdb_files = [file for file in extracted_files.keys() if ".gdb" in file]
        gdb_folders = set(os.path.dirname(file) for file in gdb_files)
        
        if gdb_folders:
            with open("dat.txt",'w') as f: f.write(gdb_files[0][:-1])
            st.session_state.page = "vis"
            st.rerun()
        else: st.write("No .ecw folder found in the ZIP archive.")

def vis():
    
        # Assuming the first .gdb file is what you want to use
    with open("dat.txt",'r') as f: gdb_file = f.read()
    village = village_map_gen(gdb_file, *gdb_file.split('/')[-1].split('_')[1].split(".")[:-1])
    layers = village.layers_available()
    
    col1,col2 = st.columns([1,3])
    with col1:
        st.write("Found .ecw folder. Select the  layers...")
        if layers:
            # Display checkboxes for all available layers
            selected_layers = []
            for layer in layers:
                if st.checkbox(layer, key=layer):
                    selected_layers.append(layer)
            else: st.write("No layers selected. Please select at least one layer.")
        else: st.write("No layers available in the .ecw folder.")
    
    with col2:
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


if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == "home":
    home()

elif st.session_state.page == "vis":
    vis()

