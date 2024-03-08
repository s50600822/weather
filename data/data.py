import requests
from bs4 import BeautifulSoup
import json

url = "https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"class": "wikitable"})

all_city_data = []

for row in table.find_all("tr")[1:]:
    columns = row.find_all("td")
    city_name = columns[0].text.strip()
    country = columns[1].text.strip()
    temperatures = [col.text.strip() for col in columns[2:15]]
    all_city_data.append({
        "city_name": city_name,
        "country": country,
        "average_temperature": temperatures
    })

json_data = json.dumps(all_city_data, indent=4)
print(json_data)
with open("city_temperatures.json", "w") as json_file:
    json_file.write(json_data)