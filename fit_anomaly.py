import os, pandas as pd
from src.ocr.ocr_engine import ocr_file, normalize_text
from src.features.tfidf import TfidfFeaturizer
from src.models.anomaly import AnomalyDetector
import joblib

SYN_CSV = "data/synthetic_docs/labels.csv"

def main():
    df = pd.read_csv(SYN_CSV)
    good = df[df.label==0].path.tolist()
    texts = [normalize_text(ocr_file(p).lower()) for p in good]
    tfidf = TfidfFeaturizer(max_features=8000, ngram_range=(1,2))
    X = tfidf.fit(texts).transform(texts)
    an = AnomalyDetector(contamination=0.1)
    an.fit(X)
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(tfidf, "artifacts/iforest_tfidf.joblib")
    joblib.dump(an,    "artifacts/iforest.joblib")

if __name__ == "__main__":
    main()
