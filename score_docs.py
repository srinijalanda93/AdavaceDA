import sys, os
# make sure parent folder is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
from src.ocr.ocr_engine import ocr_file, normalize_text
from src.features.tfidf import TfidfFeaturizer
from src.parsing.extract_fields import parse_fields
from src.checks.registry_checks import RegistryChecker
from src.models.risk_score import risk_score
from src.models.utils import sigmoid

import os, sys, joblib
from src.ocr.ocr_engine import ocr_file, normalize_text
from src.features.tfidf import TfidfFeaturizer
from src.parsing.extract_fields import parse_fields
from src.checks.registry_checks import RegistryChecker
from src.models.risk_score import risk_score
from src.models.utils import sigmoid

# Load classifier artifacts
clf = joblib.load("/Users/srinija/Desktop/ADA_PRJ/artifacts/linear_svm.joblib")
cls_vec = joblib.load("/Users/srinija/Desktop/ADA_PRJ/artifacts/tfidf.joblib")

# (Optional) anomaly artifacts
an_vec_path = "/Users/srinija/Desktop/ADA_PRJ/artifacts/iforest_tfidf.joblib"
an_path     = "/Users/srinija/Desktop/ADA_PRJ/artifacts/iforest.joblib"
AN_VEC = joblib.load(an_vec_path) if os.path.exists(an_vec_path) else None
AN     = joblib.load(an_path)     if os.path.exists(an_path)     else None

rc = RegistryChecker('/Users/srinija/Desktop/ADA_PRJ/src/checks/registry_checks.py')

def score_one(path):
    text = normalize_text(ocr_file(path).lower())
    Xc = cls_vec.transform([text])
    d  = clf.decision_function(Xc)[0]
    p_fake = float(sigmoid(d))

    # Field/registry
    fields = parse_fields(text)
    cert = fields.get('cert') or ''
    scheme = None
    cert_id = None
    if cert:
        parts = cert.split()
        scheme = (parts[0] + ('' if len(parts)==1 else ' ' + parts[1])) if 'ISO' in cert.upper() else parts[0]
        cert_id = parts[-1]
    reg = rc.check_cert(scheme, cert_id, issuer=fields.get('issuer'))
    registry_fail = 1 - int(reg.get('exists', False) and reg.get('issuer_match', True))

    # Anomaly
    an_flag = 0
    if AN and AN_VEC:
        Xa = AN_VEC.transform([text])
        an_flag = int(AN.predict_flag(Xa)[0])

    risk = risk_score(p_fake, registry_fail, an_flag)
    return {
        "path": path,
        "prob_fake": round(p_fake, 3),
        "registry": reg,
        "anomaly_flag": int(an_flag),
        "risk": round(risk, 3),
        "fields": fields,
    }

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv)>1 else "data/synthetic_docs/fake_0002.pdf"
    print(score_one(path))
