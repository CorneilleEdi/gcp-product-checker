import requests
from bs4 import BeautifulSoup
import json
import re


# A product group is defined as follows:
# - it is a table row that has a th element with the class "product-group"
# - it ends when another product group is found

class ProductGroup:
    def __init__(self, name):
        self.name = name
        self.product_data = {}

    def add_product(self, product, region, availability):
        if product not in self.product_data:
            self.product_data[product] = []
        self.product_data[product].append({"region": region, "availability": availability})


class ContinentProductGroup:
    def __init__(self, name):
        self.name = name
        self.product_groups = []

    def add_product_group(self, product_group):
        self.product_groups.append(product_group)


def get_region_from_text(region_str):
    pattern = r"\((.*?)\)"
    matches = re.findall(pattern, region_str)
    if matches:
        result = matches[0]
        return result
    else:
        # raise exception if the region is not found and print the stack trace
        raise Exception("Region matching from text failed")


CONTINENTS = ["AMERICAS", "EUROPE", "ASIA PACIFIC", "MIDDLE EAST"]
URL = "https://cloud.google.com/about/locations"
response = requests.get(URL)

products_table_soup = BeautifulSoup(response.text, 'html.parser')

continents_products_list = []

for continent in CONTINENTS:
    continent_product_group = ContinentProductGroup(continent)
    product_group = None

    # The following selector does not work. I had no idea why. I think that the library is not able to parse the response
    # like a browser does.
    # selector = '#tabpanel-americas > cloudx-table > div > table' I had to explore the response and
    # find the table manually.

    products_table_selector = f"#{continent.replace(' ', '-').lower()}-content >  div > table"
    products_table = products_table_soup.select_one(products_table_selector)
    products_table = products_table_soup.find("table", class_="cloud-table")

    if products_table:
        try:

            # Initialize a list to store the product groups
            product_groups = []

            # Extract the table header to get the regions
            header = products_table.find("thead")
            if header:
                regions = [th.get_text(strip=True) for th in header.find_all("th")][1:]

            # Extract the table body to get the product availability data
            body = products_table.find("tbody")
            if body:
                rows = body.find_all("tr")
                current_group = None

                for row in rows:
                    # Check if the row represents a product group
                    product_group = row.find("th", class_="product-group")
                    if product_group:
                        current_group = product_group.get_text(strip=True)
                        product_groups.append(ProductGroup(current_group))
                    elif current_group:
                        # Process the rows that are part of a group
                        # Extract the product name
                        product_name = row.find("th", scope="row")
                        if product_name:
                            product = product_name.get_text(strip=True)
                            # remove all numbers and special characters from the product name
                            try:
                                product = re.sub(r'[^a-zA-Z ]', '', product)
                            except Exception as e:
                                raise Exception("Error removing numbers and special characters from the product name")

                            # Extract the availability for each region in the row
                            availability_data = row.find_all("span", class_="region-availability")

                            availability = [span["aria-label"] for span in availability_data]

                            try:
                                availability = list(map(lambda item: item == 'available', availability))
                            except Exception as e:
                                raise Exception("Error converting the availability to boolean")

                            # Add the product and its availability to the product group
                            for region, avail in zip(regions, availability):
                                region = get_region_from_text(region)
                                product_groups[-1].add_product(product, region, avail)

            # Convert the product groups to a JSON representation
            # try:
            #     product_groups_json = []
            #     for group in product_groups:
            #         group_data = {"name": group.name, "products": []}
            #         for product, data in group.product_data.items():
            #             group_data["products"].append({"name": product, "availability": data})
            #         product_groups_json.append(group_data)
            # except Exception as e:
            #     raise Exception("Error converting the product groups to JSON")
            #
            # # Convert the JSON data to a JSON-formatted string
            # json_string = json.dumps(product_groups_json, indent=4)
            #
            # # Print the JSON representation
            # print(json_string)

            # Add the product groups to the continent product group
            for group in product_groups:
                continent_product_group.add_product_group(group)

            # Add the continent product group to the list of continent product groups
            continents_products_list.append(continent_product_group)


        except Exception as e:
            raise Exception("Error parsing the product table")

    else:
        raise Exception("Product table not found.")

# Convert the data to JSON format
try:
    json_data = json.dumps([{"Name": continent.name,
                             "ProductsGroups": [{"Name": group.name,
                                                 "Products": {
                                                     "Name": list(group.product_data.keys())[0],
                                                     "Availabilities": group.product_data[
                                                         list(group.product_data.keys())[0]]
                                                 }}
                                                for group in continent.product_groups]}
                            for continent in continents_products_list], indent=2)
except Exception as e:
    raise Exception("Error parsing the product table to JSON")

# Save the JSON data to a file
with open("continents_products.json", "w") as file:
    file.write(json_data)
