import requests
from bs4 import BeautifulSoup

ZONES_URL = 'https://cloud.google.com/compute/docs/regions-zones'
response = requests.get(ZONES_URL)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.select_one("#gc-wrapper > main > devsite-content > article > div:nth-of-type(2) > div:nth-of-type(2) > "
                        "devsite-filter")

if table:
    global zones
    table_data = []
    headers = [th.text for th in table.select("thead th")]
    rows = table.select("tbody tr")
    for row in rows:
        row_data = [td.text for td in row.select("td")]
        row_dict = dict(zip(headers, row_data))
        table_data.append(row_dict)
    zones = table_data
else:
    raise Exception("Zones table not found")

regions = []
for zone in zones:
    if not any(region['Location'] == zone['Location'] for region in regions):
        regions.append({
            'Region': zone['Zones'][:-2],
            'Location': zone['Location'],
            'Zones': [zone]
        })
    else:
        for region in regions:
            if region['Location'] == zone['Location']:
                region['Zones'].append(zone)
print(regions)
