import requests
import csv
import json
import os

language = ""
country = ""

with open("lbp.csv", "r") as file:
    csvFile = csv.reader(file)
    for entries in csvFile:
        contentID = entries[1]
        serviceIDPrefix = contentID[0:6]
        npTitleID = contentID[7:19]
        entitlementID = contentID[20:36]
        if serviceIDPrefix == "UP9000":
            language = "en"
            country = "us"
        elif serviceIDPrefix == "EP9000":
            language = "en"
            country = "gb"
        elif serviceIDPrefix == "HP9000":
            language = "en"
            country = "hk"
        elif serviceIDPrefix == "JP9000":
            language = "ja"
            country = "jp"

        url = (
            "https://store.playstation.com/store/api/chihiro/00_09_000/container/"
            + country
            + "/"
            + language
            + "/"
            + contentID
        )

        # Create folder for files to be saved to
        os.makedirs(str(npTitleID) + "/" + str(entitlementID), exist_ok=True)

        # Request data from API
        response = requests.get(url)
        print(url)
        data = response.json()

        # Save the data requested from API
        try:
            # Show current Content ID
            print(data["id"] + " | " + data["name"])

            # Output JSON data to file
            json_str = json.dumps(data, indent=4)
            with open(
                npTitleID + "/" + entitlementID + "/" + data["id"] + ".json",
                "w",
            ) as file:
                print("Saving... " + data["id"] + ".json")
                file.write(json_str)

            # Output icon to file(s)
            ## Save icons extracted from JSON
            for i in data["images"]:
                if isinstance(i, dict):
                    for k, v in i.items():
                        if k == "url":
                            response = requests.get(v).content
                            with open(
                                npTitleID + "/" + entitlementID + "/" + str(v[58:]),
                                "wb",
                            ) as file:
                                print("Saving... " + str(v[58:]))
                                file.write(response)

            ## Save icon from official API /image endpoint
            response = requests.get(url + "/image").content
            with open(
                npTitleID + "/" + entitlementID + "/" + data["id"] + ".jpg",
                "wb",
            ) as file:
                print("Saving... " + data["id"] + ".jpg")
                file.write(response)

            ## Save promomedia extracted from JSON
            try:
                for i in data["promomedia"][0]["materials"][0]["urls"]:
                    if isinstance(i, dict):
                        for k, v in i.items():
                            if k == "url":
                                response = requests.get(v).content
                                with open(
                                    npTitleID + "/" + entitlementID + "/" + str(v[49:]),
                                    "wb",
                                ) as file:
                                    print("Saving... " + str(v[49:]))
                                    file.write(response)
            except:
                pass

            print("\n", end="")

        except:
            os.rmdir(npTitleID + "/" + entitlementID)
            with open(npTitleID + "/" + "errlog.log", "a") as file:
                file.write(entitlementID + " | INVALID\n")
            file.close()
