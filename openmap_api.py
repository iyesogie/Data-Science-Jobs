import requests

city = "Atlanta"
state = "Georgia"
query = f"https://nominatim.openstreetmap.org/search.php?q={city}+{state}&polygon_geojson=1&format=json"
response = requests.get("https://nominatim.openstreetmap.org/search.php?q=Warsaw+Poland&polygon_geojson=1&format=json")
print(response.status_code)
print(response.json())
