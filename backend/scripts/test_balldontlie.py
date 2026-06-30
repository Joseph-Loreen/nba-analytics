import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("78904aa7-af7c-4f9c-9411-3e632bfa58a7")

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