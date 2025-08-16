import os, pandas as pd, numpy as np
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.ocr.ocr_engine import ocr_file, normalize_text
from src.features.tfidf import TfidfFeaturizer
from src.models.classifier import make_linear_svm
import joblib

# SYN_CSV = "data/synthetic_docs/labels.csv"
# RVL_DIR = "data/rvl_cdip"

# def load_paths_and_labels():
#     df = pd.read_csv(SYN_CSV)
#     paths = df.path.tolist()
#     labels = df.label.tolist()
#     # Add RVL-CDIP as real (label=0)
#     rvl_files = glob(os.path.join(RVL_DIR, "**", "*.*"), recursive=True)
#     rvl_files = [p for p in rvl_files if os.path.splitext(p)[1].lower() in {'.png','.jpg','.jpeg','.tif','.tiff','.pdf'}]
#     paths.extend(rvl_files)
#     labels.extend([0]*len(rvl_files))
#     return pd.DataFrame({"path": paths, "label": labels})

# def main():
#     df = load_paths_and_labels()
#     texts, y = [], []
#     for p, lab in zip(df.path, df.label):
#         try:
#             t = ocr_file(p)
#             texts.append(normalize_text(t.lower()))
#             y.append(lab)
#         except Exception as e:
#             print("[WARN] OCR failed:", p, e)
#     tfidf = TfidfFeaturizer(max_features=8000, ngram_range=(1,2))
#     X = tfidf.fit(texts).transform(texts)

#     y = pd.Series(y)
#     Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#     clf = make_linear_svm()
#     clf.fit(Xtr, ytr)
#     y_pred = clf.predict(Xte)
#     print(classification_report(yte, y_pred, digits=3))
#     os.makedirs("artifacts", exist_ok=True)
#     joblib.dump(tfidf, "artifacts/tfidf.joblib")
#     joblib.dump(clf,   "artifacts/linear_svm.joblib")

# if __name__ == "__main__":
#     main()


# --- Update paths here ---
SYN_CSV = "/Users/srinija/Desktop/ADA_PRJ/data/synthetic_docs/labels.csv"
RVL_DIR = "/Users/srinija/Desktop/ADA_PRJ/data/rvl_cdip"

def load_paths_and_labels():
    df = pd.read_csv(SYN_CSV)
    paths = df.path.tolist()
    labels = df.label.tolist()

    # Add RVL-CDIP as real (label=0)
    rvl_files = glob(os.path.join(RVL_DIR, "**", "*.*"), recursive=True)
    rvl_files = [
        p for p in rvl_files
        if os.path.splitext(p)[1].lower() in {'.png','.jpg','.jpeg','.tif','.tiff','.pdf'}
    ]
    paths.extend(rvl_files)
    labels.extend([0]*len(rvl_files))

    return pd.DataFrame({"path": paths, "label": labels})

def main():
    df = load_paths_and_labels()
    texts, y = [], []

    for p, lab in zip(df.path, df.label):
        try:
            t = ocr_file(p)
            if not t.strip():
                print(f"[SKIP] Empty OCR result: {p}")
                continue
            texts.append(normalize_text(t.lower()))
            y.append(lab)
        except Exception as e:
            print("[WARN] OCR failed:", p, e)

    print("Number of documents:", len(texts))
    print("First document preview:", texts[0][:500] if texts else "EMPTY")

    if not texts:
        print("[ERROR] No documents were processed. Exiting.")
        return

    tfidf = TfidfFeaturizer(max_features=8000, ngram_range=(1,2))
    X = tfidf.fit(texts).transform(texts)

    y = pd.Series(y)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = make_linear_svm()
    clf.fit(Xtr, ytr)
    y_pred = clf.predict(Xte)

    print(classification_report(yte, y_pred, digits=3))

    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(tfidf, "artifacts/tfidf.joblib")
    joblib.dump(clf,   "artifacts/linear_svm.joblib")

if __name__ == "__main__":
    main()
