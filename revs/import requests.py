import requests
import os
import shutil
url = "https://store.playstation.com/store/api/chihiro/00_09_000/container/gb/en/999/EP9000-BCES00141_00-PLITTLEBIG000016"
response = requests.get(url)
data = response.json()
npTitleID = "BOGUS"
os.makedirs(npTitleID, exist_ok=True)
for i in data['images']:
    if isinstance(i, dict):
        for k, v in i.items():
            if k == 'url':
                print(v)
                response = requests.get(v).content
                with open(str(v[58:]), "wb") as file:
                    shutil.copyfileobj(response, file)
                    print(v)
                del response



