import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AQICN_API_TOKEN')
print("Token:", token)

city = "tehran"
url = f"https://api.waqi.info/feed/{city}/?token={token}"
response = requests.get(url)
print(response.json())
