# Fetcher

The fetcher is a set of scripts that scrape the appropriate page on Google cloud website to generate the appropriate
data files that will be used on the website.

## Regions fetcher

It retrieves the list of regions available on Google cloud and generate a json file.

### Actual format:

```json
[
  {
    "Region": "asia-east1",
    "Location": "Changhua County, Taiwan, APAC",
    "Zones": [
      {
      {
        "Location": "Jurong West, Singapore, APAC",
        "Machine types": "E2, N2, N2D, C3, T2D, N1, M1, C2, C2D",
        "CPUs": "Intel Ivy Bridge, Sandy Bridge, Haswell, Broadwell, Skylake, Cascade Lake, Ice Lake, Sapphire Rapids, AMD EPYC Rome, AMD EPYC Milan",
        "Resources": "GPUs",
        "CO2 emissions": "",
        "Zone": "asia-southeast1-a"
      },
      ...
    ]
  }
]
```

### Fields

- `Region`: the name of the region
- `Location`: the location of the region
- `Zones`: the list of zones in the region
- `Zones.Zone`: the name of the zone
- `Zones.Location`: the location of the zone
- `Zones.Machine types`: the list of machine types available in the zone
- `Zones.CPUs`: the list of CPUs available in the zone
- `Zones.Resources`: the list of resources available in the zone
- `Zones.CO2 emissions`: the CO2 emissions of the zone

### Usage

```bash
python3 regions_fetcher.py
```

## Products fetcher

It retrieves the list of products available on google cloud, create a mapping value based on their availability in the
regions and generate a json file.
The products are then group by continent.

### Actual format:

```json
[
  {
    "Name": "AMERICAS",
    "ProductsGroups": [
      {
        "Name": "Compute",
        "Products": {
          "Name": "Compute Engine",
          "Availabilities": [
            {
              "region": "us-west1",
              "availability": true
            },
            {
              "region": "us-west2",
              "availability": true
            },
            {
              "region": "us-west3",
              "availability": true
            },
            {
              "region": "us-west4",
              "availability": true
            },
            {
              "region": "us-central1",
              "availability": true
            },
            {
              "region": "us-east1",
              "availability": true
            },
            {
              "region": "us-east4",
              "availability": true
            },
            {
              "region": "us-east5",
              "availability": true
            },
            {
              "region": "us-south1",
              "availability": true
            },
            {
              "region": "northamerica-northeast1",
              "availability": true
            },
            {
              "region": "northamerica-northeast2",
              "availability": true
            },
            {
              "region": "southamerica-west1",
              "availability": true
            },
            {
              "region": "southamerica-east1",
              "availability": true
            }
          ]
        }
      },
      ...
    ]
```

### Fields

- `Name`: the name of the continent
- `ProductsGroups`: the list of products groups available in the continent
- `ProductsGroups.Name`: the name of the product group
- `ProductsGroups.Products`: the list of products available in the product group
- `ProductsGroups.Products.Name`: the name of the product
- `ProductsGroups.Products.Availabilities`: the list of availabilities of the product in the regions
- `ProductsGroups.Products.Availabilities.region`: the name of the region
- `ProductsGroups.Products.Availabilities.availability`: the availability of the product in the region

### Usage

```bash
python3 products_fetcher.py
```


