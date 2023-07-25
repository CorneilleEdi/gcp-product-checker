import requests
from bs4 import BeautifulSoup
import json

REGIONS_AND_ZONES_URL = 'https://cloud.google.com/compute/docs/regions-zones'
response = requests.get(REGIONS_AND_ZONES_URL)

regions_soup = BeautifulSoup(response.text, 'html.parser')

regions_table = regions_soup.select_one(
    "#gc-wrapper > main > devsite-content > article > div:nth-of-type(2) > div:nth-of-type(2) > "
    "devsite-filter")
if regions_table:
    global zones
    table_data = []
    headers = [th.text for th in regions_table.select("thead th")]
    rows = regions_table.select("tbody tr")
    for row in rows:
        # " ".join(td.text.replace('\n', '').split()) is for formatting and remove unnecessary spaces
        # td.text can just be used
        row_data = [" ".join(td.text.replace('\n', '').split()) for td in row.select("td")]
        row_dict = dict(zip(headers, row_data))

        # Change the ley 'Zones'  to 'Zone'
        row_dict['Zone'] = row_dict.pop('Zones')

        table_data.append(row_dict)
    zones = table_data
else:
    raise Exception("Zones table not found")

regions = []
for zone in zones:
    if not any(region['Location'] == zone['Location'] for region in regions):
        regions.append({
            'Region': zone['Zone'][:-2],
            'Location': zone['Location'],
            'Zones': [zone]
        })
    else:
        for region in regions:
            if region['Location'] == zone['Location']:
                region['Zones'].append(zone)

with open("regions.json", "w") as fp:
    json.dump(regions, fp, indent=2)
