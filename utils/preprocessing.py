# utils/preprocessing.py
import cv2
import numpy as np
import streamlit as st

def preprocess_image(img, method="Auto"):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if method == "None":
            return img
        elif method == "Grayscale":
            return gray
        elif method == "Threshold":
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            return thresh
        elif method == "Adaptive Threshold":
            return cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == "Auto":
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            h, w = sharpened.shape
            resized = cv2.resize(sharpened, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
            _, thresh = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY)
            coords = np.column_stack(np.where(thresh > 0))
            angle = cv2.minAreaRect(coords)[-1]
            angle = -(90 + angle) if angle < -45 else -angle
            M = cv2.getRotationMatrix2D((w*2//2, h*2//2), angle, 1)
            deskewed = cv2.warpAffine(
                thresh, M, (w*2, h*2),
                flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
            )
            return deskewed
    except Exception as e:
        st.error(f"Preprocessing error: {e}")
        return img