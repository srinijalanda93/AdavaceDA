import pandas as pd
from pathlib import Path

class RegistryChecker:
    def __init__(self, base_path='data/registries'):
        self.base = Path(base_path)
        self.iso = pd.read_csv(self.base / 'valid_iso.csv') if (self.base / 'valid_iso.csv').exists() else None

    def check_cert(self, scheme, cert_id, issuer=None):
        if self.iso is None or not cert_id or not scheme:
            return {"exists": False, "issuer_match": False}
        df = self.iso
        m = df[(df.scheme.str.lower()==scheme.lower()) & (df.cert_id.str.upper()==str(cert_id).upper())]
        ok = len(m)>0
        issuer_ok = (issuer is None) or (ok and (m.issuer.str.lower().str.contains(issuer.lower()).any()))
        return {"exists": ok, "issuer_match": issuer_ok}
