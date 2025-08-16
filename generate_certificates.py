from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from faker import Faker
import random, csv, os, re
from pathlib import Path

SCHEMES = ["ISO 9001", "CE", "RoHS", "UL"]
ISSUERS = ["Global Cert Labs", "EuroConformity BV", "AsiaTest Pvt Ltd", "UL Solutions"]

fake = Faker()

def make_cert_text():
    scheme = random.choice(SCHEMES)
    cert_id = fake.bothify(text='??-#####').upper()
    company = fake.company()
    date = fake.date_between(start_date='-3y', end_date='today').isoformat()
    issuer = random.choice(ISSUERS)
    lines = [
        f"Certificate of Conformity ({scheme})",
        f"Company: {company}",
        f"Serial No: {fake.bothify(text='SN-########').upper()}",
        f"Batch No: {fake.bothify(text='BATCH-####').upper()}",
        f"Issued By: {issuer}",
        f"Cert: {scheme} #{cert_id}",
        f"Issue Date: {date}",
    ]
    return scheme, cert_id, issuer, company, date, "\n".join(lines)

def render_pdf(path, text):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 30*mm
    for line in text.split("\n"):
        c.drawString(25*mm, y, line)
        y -= 8*mm
    c.save()

def corrupt(text):
    t = text
    t = t.replace("Certificate of Conformity", "Certificate of Confirmity")  # subtle typo
    t = t.replace("Issued By:", "Issued By : ")
    t = re.sub(r"(Cert:.*#.*)(\d)", lambda m: m.group(1)+str((int(m.group(2))+7)%10), t, count=1)
    return t

def generate(n_real=200, n_fake=200, out_dir="data/synthetic_docs"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n_real):
        scheme, cert_id, issuer, company, date, text = make_cert_text()
        pdf = os.path.join(out_dir, f"real_{i:04d}.pdf")
        render_pdf(pdf, text)
        rows.append([pdf, 0, scheme, cert_id, issuer, company, date])
    for i in range(n_fake):
        scheme, cert_id, issuer, company, date, text = make_cert_text()
        forged = corrupt(text)
        pdf = os.path.join(out_dir, f"fake_{i:04d}.pdf")
        render_pdf(pdf, forged)
        rows.append([pdf, 1, scheme, cert_id, issuer, company, date])
    with open(os.path.join(out_dir, "labels.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path","label","scheme","cert_id","issuer","company","date"])
        w.writerows(rows)

if __name__ == "__main__":
    generate()