import requests

HOST = "http://127.0.0.1:8000"
LIST_DRINK = f"{HOST}/drinks"

response = requests.get(LIST_DRINK)
print(response.json())
