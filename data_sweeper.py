import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure Streamlit page
st.set_page_config(page_title="Data Sweeper - By Asma Khan", layout="wide")

# Dark/Light Mode Toggle
mode = st.sidebar.radio("Select Mode:", ["Dark Mode", "Light Mode"])

# Custom CSS for themes
dark_mode_css = """
    <style>
        .main { background-color: #121212; color: white; }
        .block-container {
            padding: 2rem;
            border-radius: 10px;
            background-color: #1e1e1e;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3, h4, h5, h6 { color: #66c2ff; }
        .stButton>button { background-color: #0078D7; color: white; }
        .stDownloadButton>button { background-color: #28a745; color: white; }
    </style>
"""

light_mode_css = """
    <style>
        .main { background-color: #ffffff; color: black; }
        .block-container {
            padding: 2rem;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3, h4, h5, h6 { color: #0078D7; }
        .stButton>button { background-color: #0078D7; color: white; }
        .stDownloadButton>button { background-color: #28a745; color: white; }
    </style>
"""

# Apply CSS based on mode
st.markdown(dark_mode_css if mode == "Dark Mode" else light_mode_css, unsafe_allow_html=True)

# App title
st.title("🚀 Advanced Data Sweeper - By Asma Khan")
st.write("Upload and clean your files (CSV or Excel), visualize data, and convert formats easily!")

# Sidebar options
st.sidebar.header("🔧 Options")
conversion_type = st.sidebar.radio("Convert File To:", ["CSV", "Excel"])

# File uploader
uploaded_files = st.file_uploader("📂 Upload your CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

# Process uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        try:
            # Read file based on type
            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"⚠️ Unsupported file type: {file_extension}")
                continue

            # Display file info
            st.write(f"**📄 File Name:** {file.name}")
            st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")
            
            # Show data preview
            st.write("🔍 **Preview of the Uploaded File:**")
            st.dataframe(df.head())

            # Data Cleaning Options
            with st.expander("🛠 Data Cleaning Options", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("✅ Duplicates Removed!")

                with col2:
                    if st.button(f"Fill Missing Values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing Values Filled!")

            # Select columns to convert
            with st.expander("🎯 Select Columns to Convert", expanded=False):
                selected_columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
                df = df[selected_columns]

            # Visualization Options
            with st.expander("📊 Data Visualization", expanded=False):
                if st.checkbox(f"Show Visualization for {file.name}"):
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # File conversion & download
            buffer = BytesIO()
            file_name = file.name.replace(file_extension, f".{conversion_type.lower()}")

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(label=f"⬇️ Download {file.name} as {conversion_type}",
                               data=buffer, file_name=file_name, mime=mime_type)

        except Exception as e:
            st.error(f"❌ Error processing file {file.name}: {e}")

st.success("🎉 All files processed successfully!")
