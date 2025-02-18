import streamlit as st
import pandas as pd
import os
import logging
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)

# Streamlit page setup
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for Dark Mode UI
st.markdown("""
    <style>
        .main { background-color: #121212; }
        .block-container {
            padding: 2rem;
            border-radius: 10px;
            background-color: #1e1e1e;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3, h4, h5, h6 { color: #66c2ff; }
        .stButton>button {
            background-color: #0078D7; color: white;
            border-radius: 8px; padding: 0.75rem 1.5rem;
            font-size: 1rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }
        .stButton>button:hover { background-color: #005a9e; cursor: pointer; }
        .stDataFrame, .stTable { border-radius: 10px; overflow: hidden; }
        .stDownloadButton>button { background-color: #28a745; color: white; }
        .stDownloadButton>button:hover { background-color: #218838; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Advanced Data Sweeper")
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

            # Get file size safely
            file.seek(0, os.SEEK_END)  
            file_size = file.tell() / 1024  
            file.seek(0)  

            # Display file info
            st.write(f"**📄 File Name:** {file.name}")
            st.write(f"**📏 File Size:** {file_size:.2f} KB")

            # Show data preview
            st.write("🔍 **Preview of the Uploaded File:**")
            st.dataframe(df.head())

            # Data Cleaning Options (inside an expander)
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
