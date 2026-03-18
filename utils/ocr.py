# utils/ocr.py
import pytesseract
import cv2
import streamlit as st

def run_ocr(img, lang_str, draw_boxes=False):
    try:
        custom_config = r'--oem 3 --psm 6'
        if draw_boxes:
            boxes_img = img.copy()
            data = pytesseract.image_to_data(
                img, lang=lang_str, config=custom_config,
                output_type=pytesseract.Output.DICT
            )
            for i in range(len(data['level'])):
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                cv2.rectangle(boxes_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            text = pytesseract.image_to_string(img, lang=lang_str, config=custom_config)
            return text, boxes_img
        else:
            text = pytesseract.image_to_string(img, lang=lang_str, config=custom_config)
            return text, img
    except Exception as e:
        st.error(f"OCR error: {e}")
        return "", img