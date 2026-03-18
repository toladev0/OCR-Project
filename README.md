# **Khmer OCR**

Khmer OCR is a **Streamlit-based OCR application** that can extract text from images and PDFs. It supports multiple languages, multiple files, and optional image preprocessing to enhance OCR accuracy.

---

## **Features**
- Multi-page PDF and multi-image support
- Select OCR languages (`eng`, `khm`) or both
- Optional preprocessing: Auto, None, Grayscale, Threshold, Adaptive Threshold
- Optional display of detected text boxes
- Download extracted text per page, per file, or all files combined
- Modern, compact Streamlit UI

---

## **Installation**

1. Clone or download this repository:
```bash
git clone https://github.com/toladev0/OCR-Project.git
```

2. Create a virtual environment (recommended):
```bash
python -m venv .env
```

3. Activate the environment:
- Windows:
```bash
.env\Scripts\activate
```
- Mac/Linux:
```bash
source .env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Poppler](http://blog.alivate.com.au/poppler-windows/) if not installed.  
   - Update paths in `config.py`:
```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"
```

---

## **Usage**

Run the Streamlit app:
```bash
streamlit run app.py
```

- Upload images or PDFs using drag & drop.
- Select OCR languages and optional preprocessing.
- Toggle “Show Detected Text Boxes” if needed.
- Download extracted text per page, per file, or all files combined.

---

## **Customizations**

- **Default OCR languages:** Change in `config.py`:
```python
DEFAULT_LANGS = ["eng", "khm"]
```

- **Default preprocessing:** Set `index` in sidebar selectbox in `app.py`.

- **UI style:** Modify CSS in `app.py` markdown section.

---

## **Dependencies**

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Pillow](https://python-pillow.org/)
- [OpenCV](https://opencv.org/)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [NumPy](https://numpy.org/)

---

## **Tips for Accuracy**
- Use `Auto` preprocessing for scanned or low-quality images.
- Ensure images are high-resolution (300 DPI recommended for PDFs).
- Multi-language OCR can slow down processing for large files.

---

## **License**

MIT License – free to use, modify, and distribute.