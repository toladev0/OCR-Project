# utils/pdf_utils.py
from pdf2image import convert_from_bytes
import streamlit as st
from config import POPLER_PATH

def pdf_to_images(file_bytes):
    try:
        images = convert_from_bytes(file_bytes, dpi=300, poppler_path=POPLER_PATH)
        return images
    except Exception as e:
        st.error(f"PDF processing error: {e}")
        return []