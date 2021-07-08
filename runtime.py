from scrape import PDFMetadata

# May rename file as metadata.py

METADATA_FILENAME = 'scraper.dat'

def parse_metadata(metadata_content: str) -> PDFMetadata:
    '''
    METADATA_FILENAME contains the following string:
    YYYY-MM-DD-${md5(pdf)}.pdf

    The md5 hash can be split off, and used for comparison.
    '''

    MD5_HASH_IDX = 3
    return PDFMetadata(metadata_content, metadata_content.split('-')[MD5_HASH_IDX][:-4])

def read_last_scrape_metadata() -> PDFMetadata:
    with open(METADATA_FILENAME, 'r') as f:
        raw_metadata = f.read()
        return parse_metadata(raw_metadata)

def write_last_scrape_metadata(metadata: PDFMetadata):
    with open(METADATA_FILENAME, 'w') as f:
        f.write(metadata.filepath)
