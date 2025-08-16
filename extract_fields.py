import re
from dateutil import parser as dparser

CERT_ID_RGX = re.compile(r"(ISO\s?9001|CE|RoHS|UL)\s*[:#-]?\s*([A-Z0-9\-]{2,}\b)", re.I)
BATCH_RGX   = re.compile(r"batch\s*no\.?\s*([A-Z0-9\-]{3,})", re.I)
SERIAL_RGX  = re.compile(r"serial\s*no\.?\s*([A-Z0-9\-]{3,})", re.I)
ISSUER_RGX  = re.compile(r"issued\s*by\s*:?\s*([A-Za-z\s,&.]{3,})", re.I)
COMPANY_RGX = re.compile(r"(company|manufacturer|supplier)\s*:?\s*([A-Za-z0-9\s,&.\-]{3,})", re.I)
DATE_RGX    = re.compile(r"(\d{4}[\-/]\d{1,2}[\-/]\d{1,2}|\d{1,2}[\-/]\d{1,2}[\-/]\d{2,4})")

FIELDS = [("cert", CERT_ID_RGX),("batch",BATCH_RGX),("serial",SERIAL_RGX),("issuer",ISSUER_RGX),("company",COMPANY_RGX)]

def parse_fields(text: str):
    out = {k: None for k,_ in FIELDS}
    for k, rgx in FIELDS:
        m = rgx.search(text)
        if not m: continue
        if k == "cert":
            out[k] = f"{m.group(1)} {m.group(2)}".strip()
        else:
            out[k] = (m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)).strip()
    dm = DATE_RGX.search(text)
    if dm:
        try:
            out["date"] = dparser.parse(dm.group(0), dayfirst=False, fuzzy=True).date().isoformat()
        except Exception:
            out["date"] = dm.group(0)
    return out
