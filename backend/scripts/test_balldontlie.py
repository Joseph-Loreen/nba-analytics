import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BALLDONTLIE_API_KEY")

headers = {
    "Authorization": API_KEY
}

response = requests.get(
    "https://api.balldontlie.io/v1/players",
    params={"search": "LeBron"},
    headers=headers
)

print(response.status_code)
print(response.json())