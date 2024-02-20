import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

from fixes import state_fixes

URL = 'https://ocrcas.ed.gov/open-investigations'

payload1 = {'page': 0, 'items_per_page': 1000, 'field_ois_institution_type': 752}
payload2 = {'page': 1, 'items_per_page': 1000, 'field_ois_institution_type': 752}
payload3 = {'page': 2, 'items_per_page': 1000, 'field_ois_institution_type': 752}
r1 = requests.get(URL, params=payload1)
r1.raise_for_status()
r2 = requests.get(URL, params=payload2)
r2.raise_for_status()
r3 = requests.get(URL, params=payload3)
r3.raise_for_status()

r_list = [r1, r2, r3]

CSV_FILE = 'doe-discrimination-complaints.csv'

CSV_HEADERS = [
    'State',
    'Institution',
    'Type_of_Discrimination',
    'Investigation_Start_Date'
    ]

table1 = BeautifulSoup(r1.text, 'html.parser').find('table')
table2 = BeautifulSoup(r2.text, 'html.parser').find('table')
table3 = BeautifulSoup(r3.text, 'html.parser').find('table')

table_list = [table1, table2, table3]

with open(CSV_FILE, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=CSV_HEADERS)

    writer.writeheader()

    for i in table_list:
        for row in i.find_all('tr')[1:]:
            cell = row.find_all('td')

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
