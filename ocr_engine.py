import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import cv2, re, os, numpy as np
from pathlib import Path

def _binarize(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    thr = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,11)
    return thr

def pdf_to_images(pdf_path: str, dpi: int = 300):
    pages = convert_from_path(pdf_path, dpi=dpi)
    out = []
    for p in pages:
        out.append(cv2.cvtColor(np.array(p), cv2.COLOR_RGB2BGR))
    return out

def ocr_file(path: str) -> str:
    p = Path(path)
    imgs = []
    if p.suffix.lower() == '.pdf':
        imgs = pdf_to_images(path)
    else:
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Cannot read image: {path}")
        imgs = [img]
    texts = []
    for img in imgs:
        proc = _binarize(img)
        text = pytesseract.image_to_string(proc, config='--oem 3 --psm 6')
        texts.append(text)
    return "\n".join(texts)

def normalize_text(t: str) -> str:
    t = t.replace('\u00a0',' ').replace('\t',' ')
    t = re.sub(r"\s+", " ", t)
    return t.strip()