from time import sleep
from hashlib import md5
import sys

from requests.exceptions import RequestException
from pymongo import MongoClient

import scrape
import runtime
import extract

# TODO
# - [ ] setup proper logger
# - [ ] reasonable request error handling (keep trying every 60 seconds forever)
# - [ ] mongo storage
# - [ ] scrape timer
# - [ ] package properly

SCRAPE_INTERVAL = 60*60*24*2

def save_to_db(db, pdf_filepath):
    table = extract.extract_table(pdf_filepath)
    print(table)
    for _, row in table.iterrows():
        call = extract.row_to_json(row)
        db.insert_one(call)

def main():
    db = MongoClient().ames_911
    calls_doc = db.calls

    while True:
        try:
            prev_metadata = runtime.read_last_scrape_metadata()
        except FileNotFoundError:
            print('No metadata file exists.')
            prev_metadata = None

        # Since this downloads to the disk, we'll want to delete it if it's a duplicate
        # Note: need to handle bad request.
        while True:
            try:
                pdf_blob = scrape.download_pdf('./data/pdf')
                pdf_md5 = md5(pdf_blob).hexdigest()
                break
            except RequestException as error:
                print(f'PDF download failed with exception: {error}')
                print('Trying again in a minute..')
                sleep(60)

        print(prev_metadata)
        print(pdf_md5)
        if prev_metadata and prev_metadata.md5 == pdf_md5:
            print('Same log, skipping.')
            sleep(SCRAPE_INTERVAL)
            continue

        print('New log!')
        # TODO: Remove -- use for testing live.
        # sys.exit(0)

        pdf_metadata = scrape.write_pdf_blob(pdf_blob) 
        print('Saved new pdf log')
        runtime.write_last_scrape_metadata(pdf_metadata)
        print('Wrote new metadata')
        # Perform extraction here
        save_to_db(calls_doc, pdf_metadata.filepath)

        sleep(SCRAPE_INTERVAL)
        continue

if __name__ == '__main__':
    main()
