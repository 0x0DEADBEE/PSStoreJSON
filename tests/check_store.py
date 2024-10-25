import csv
import requests
import json

with open("lang_store.csv", "r") as file:
    csvFile = csv.reader(file)
    for entries in csvFile:
        country = entries[1]
        language = entries[0]
        url = (
            "https://store.playstation.com/store/api/chihiro/00_09_000/container/"
            + country
            + "/"
            + language
            + "/999/"
            + "EP9000-NPEA00241_00-GLITTLEBIG000001"
        )

        # Request data from API
        print(url)
        response = requests.get(url)
        data = response.json()
        # print(response)

        # Save the data requested from API
        try:
            # Show current Content ID
            print(data["name"])
        except:
            pass
