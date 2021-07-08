'''
TODO

- [ ] Strip all carriage returns, replace with commas (requires quoting on csv side of things)
- [x] Make sure ids are integers, not floats
- [x] Dates need converted to timestamps
- [ ] Data needs stored in sql or mongo (appended each successful scrape). Rather use mongo at this point.
- [ ] Setup on DO

Scraping is very straightforward. Every 24 hours, fetch the document from the ames site.
Perform a hash and compare to the last doc. If they're different, the data should be appended to the DB.
Make sure there are no duplicate entries.
Keep all scraped pdfs for historical reference
'''

from enum import Enum
from datetime import datetime

import csv
import tabula
import pandas as pd

Call = Enum('Call', 'date id type desc address report_no code na', start=0)

def row_to_json(table_row) -> dict:
    return {
        call.name: table_row[call.value]
        for call in Call
    }


def clean_date(date):
    # Remove \r and pad front of date to work with strptime
    date = ('0'+date.split('\r')[0]).replace('^00', '0')
    return int(datetime.strptime(date, '%m/%d/%Y %I:%M%p').timestamp())

# Need code to convert this table to json for mongo input
# Each row needs a json representation
def extract_table(filepath: str) -> pd.DataFrame:
    # Not sure exactly what the last column is
    # May just want a named tuple actually?
    names = [call.name for call in Call]

    #tabula.convert_into("log.pdf", "output.csv", output_format="csv", pages='all')
    # First requirement is that we flatten the pages into a single table
    df = tabula.read_pdf(filepath, lattice=True, pages='all')

    table = pd.concat(df, ignore_index=True)
    table.columns = [name for name in names]

    table[Call.id.name] = table[Call.id.name].apply(int)
    table[Call.date.name] = table[Call.date.name].apply(clean_date)

    #results = table[table[Call.desc.name].str.contains('|'.join(['TOW']))]

    # Force quoting
    #table.to_csv('out.csv', quoting=csv.QUOTE_NONNUMERIC)

    # Next, need to iterate through each row and remove all carriage returns 

    return table
