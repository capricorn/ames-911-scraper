from hashlib import md5
from collections import namedtuple
import datetime

import requests

# Possibly override equality operator to compare md5 hashes
PDFMetadata = namedtuple('PDFMetadata', 'filepath md5')

# Have this return bytes instead..? (Rename to 'download_pdf_blob')
def download_pdf(full_path: str) -> bytes:
    resp = requests.get('https://data.city.ames.ia.us/publicinformation/PressLog.pdf')
    resp.raise_for_status()

    return resp.content

def write_pdf_blob(pdf_blob: bytes) -> PDFMetadata:
    md5_hash = md5(pdf_blob).hexdigest()
    download_date = datetime.date.today().strftime('%Y-%m-%d')
    filepath = f'./data/pdf/{download_date}-{md5_hash}.pdf'

    with open(filepath, 'wb') as f:
        f.write(pdf_blob)

    return PDFMetadata(filepath, md5_hash)
