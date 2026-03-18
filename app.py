# app.py
import streamlit as st
from utils.preprocessing import preprocess_image
from utils.ocr import run_ocr
from utils.pdf_utils import pdf_to_images
from PIL import Image
import numpy as np
import concurrent.futures
from config import TESSERACT_PATH, DEFAULT_LANGS
import pytesseract

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Streamlit UI
st.set_page_config(page_title="Khmer OCR", page_icon="assets/khmerOCR_logo.png", layout="wide")

st.image("assets/khmerOCR_logo.png", width=100)
st.markdown('<div style="font-size:2em; font-weight:bold;">Khmer OCR</div>', unsafe_allow_html=True)
st.markdown("Extract text from images or PDFs instantly")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    langs = ["eng", "khm"]
    selected_langs = st.multiselect("Select OCR Languages", langs, default=DEFAULT_LANGS)
    lang_str = "+".join(selected_langs)

    preprocess_option = st.selectbox(
        "Choose Preprocessing Method",
        ["Auto", "None", "Grayscale", "Threshold", "Adaptive Threshold"],
        index=1
    )

    show_boxes = st.checkbox("Show Detected Text Boxes", value=False)
    st.info("💡 Drag & drop multiple files below or click to upload.")

# Upload files
uploaded_files = st.file_uploader(
    "Upload Images or PDFs", type=["png","jpg","jpeg","pdf"],
    accept_multiple_files=True
)

# Function to process single page (thread safe)
def process_page(file_idx, page_idx, img, lang_str, preprocess_option, show_boxes, local_cache):
    key = f"{file_idx}_{page_idx}"
    if key in local_cache:
        processed_img = local_cache[key]
    else:
        processed_img = preprocess_image(img, preprocess_option)
        local_cache[key] = processed_img
    text, display_img = run_ocr(processed_img, lang_str, draw_boxes=show_boxes)
    return text, display_img

# Main loop
if uploaded_files:
    all_files_text = []
    for file_idx, uploaded_file in enumerate(uploaded_files):
        st.markdown(f"### 📁 File {file_idx+1}: {uploaded_file.name}")
        try:
            # PDF or image
            if uploaded_file.type == "application/pdf":
                images = pdf_to_images(uploaded_file.read())
            else:
                images = [Image.open(uploaded_file)]

            if images:
                combined_text = [None]*len(images)
                display_images = [None]*len(images)
                local_cache = {}

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {
                        executor.submit(process_page, file_idx, idx, np.array(img),
                                        lang_str, preprocess_option, show_boxes, local_cache): idx
                        for idx, img in enumerate(images)
                    }
                    for future in concurrent.futures.as_completed(futures):
                        idx = futures[future]
                        try:
                            text, display_img = future.result()
                            combined_text[idx] = text
                            display_images[idx] = display_img
                        except Exception as e:
                            st.error(f"Error processing page {idx+1}: {e}")

                # Show each page
                for idx, img in enumerate(images):
                    if combined_text[idx] is None:
                        continue
                    with st.expander(f"Page {idx+1}", expanded=False):
                        col1, col2 = st.columns([1,1])
                        with col1:
                            show_original = st.checkbox(f"Show Original", key=f"{file_idx}_{idx}")
                            st.image(np.array(img) if show_original else display_images[idx], width=600)
                        with col2:
                            st.text_area("OCR Text", combined_text[idx], height=300)
                            st.download_button(f"⬇️ Download Page {idx+1} Text",
                                               combined_text[idx],
                                               file_name=f"ocr_page_{file_idx+1}_{idx+1}.txt")

                # Combined text per file
                file_text = "\n".join([t for t in combined_text if t])
                all_files_text.append(file_text)
                st.download_button(f"⬇️ Download All Pages of {uploaded_file.name}", file_text,
                                   file_name=f"ocr_{uploaded_file.name}.txt")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

    # Download all files combined
    try:
        all_text = "\n".join([t for t in all_files_text if t])
        st.download_button("⬇️ Download All Files Combined", all_text,
                           file_name="ocr_all_files_combined.txt")
    except Exception as e:
        st.error(f"Error generating combined text for all files: {e}")