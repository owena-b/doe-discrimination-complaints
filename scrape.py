import csv
from datetime import datetime

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from fixes import state_fixes

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

URL = 'https://ocrcas.ed.gov/open-investigations'

CSV_FILE = 'doe-discrimination-complaints.csv'

CSV_HEADERS = [
    'State',
    'Institution',
    'Type_of_Discrimination',
    'Investigation_Start_Date'
    ]

r = requests.get(URL, verify=False)
r.raise_for_status()

table = BeautifulSoup(r.text, 'html.parser').find('table')

with open(CSV_FILE, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=CSV_HEADERS)

    writer.writeheader()

    for row in table.find_all('tr')[1:]:
        cell = row.find_all('td')

        if cell[2].string.strip() != 'PSE':
            continue

        state_list = [cell[0].string.strip()]

        for state in state_list:
            state = state_fixes.get(state, state)

        institution = cell[1].text.strip()

        discrim_type = cell[3].text.strip()

        date = datetime.strptime(
            cell[4].text.strip(),
            '%m/%d/%Y'
        ).date().isoformat()

        writer.writerow({
            'State': state,
            'Institution': institution,
            'Type_of_Discrimination': discrim_type,
            'Investigation_Start_Date': date
        })

    print(f'Wrote {CSV_FILE}')