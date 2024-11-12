import json

import requests

from Config import getMCPort
from api.API import get_online

url = "http://127.0.0.1:5000/sendmessage"

url2 = "http://localhost:8080/message"
data = {"message": "bruh", "name": "LFscrolls"}

# response = requests.post(url2, json={"name": "Phonix75", "message": "cope"})
# print(f"{response.status_code} {response.text}")

print(len(get_online(getMCPort())))
