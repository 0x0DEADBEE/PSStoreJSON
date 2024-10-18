from sys import argv
import requests
import json
import shutil
import os

# Set API search parameters
server = "https://store.playstation.com/store/api"
serviceIDPrefix = argv[2]
npTitleID = str(argv[3]+"_00")
country = "gb"
language = "en"
os.makedirs(npTitleID, exist_ok=True)
# Retrieve all entitlementID from
counter = 0
with open(argv[1], "r") as ContentID:
    while counter < 171:
        for line in ContentID:
            if "ContentID" in line:
                entitlementID = str(line[13:][:16])

                url = (
                    server
                    + "/chihiro/00_09_000/container/"
                    + country
                    + "/"
                    + language
                    +"/999/"
                    + serviceIDPrefix
                    + "-"
                    + npTitleID
                    + "-"
                    + entitlementID
                )
                icon_url = url + "/image"

                # Request data from API
                response = requests.get(url)
                data = response.json()
                try:
                    # Show current Content ID (format: Service ID[hyphen]NP Title ID (format: XXXXYYYYY_00)[hyphen]Entitlement label) 
                    print(data["id"])

                    # Output JSON data to file
                    json_str = json.dumps(data, indent=4)
                    with open(str(str(npTitleID)+"/"+str(data["id"])) + ".json", "w") as file:
                        file.write(json_str)

                    # Request and output icon to file
                    response = requests.get(icon_url, stream=True)
                    with open(str(str(npTitleID)+"/"+str(data["id"])) + ".jpg", "wb") as file:
                        shutil.copyfileobj(response.raw, file)
                    del response
                except:
                    print("Invalid entitlement ID:" + str(entitlementID))
    ContentID.close()