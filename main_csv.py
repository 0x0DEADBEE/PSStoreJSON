import requests
import csv
import json
import os
from pathlib import Path

#Empty placeholder values for url as they need to exist before they can be replaced within a for-loop
language = ""
country = ""


counter=0

with open("csv/lbp.csv", "r") as file:
    csvFile = csv.reader(file)
    next(csvFile)
    for entries in csvFile:
        counter+=1
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
            + "/999/"
            + contentID
        )

        # Request data from API
        response = requests.get(url)
        data = response.json()

        # Save the data requested from API
        try:
            if Path("downloads/" + str(npTitleID) + "/" + str(entitlementID)).is_dir() == True:
                try:
                    print(str(counter) + " | " + str(contentID) + " | " + data["name"] + " | Already exists")
                except:
                    print(str(counter) + " | No available data")
                    continue
            else:
                #Create folders for entitlement ID that do not currently exist
                os.makedirs(
                    "downloads/"
                    + str(npTitleID)
                    + "/" 
                    + str(entitlementID),
                    exist_ok=True
                    )

                # Show current Content ID
                print(str(counter) 
                + " | " 
                + data["id"] 
                + " | " 
                + data["name"]
                )

                # Output JSON data to file
                json_str = json.dumps(data, indent=4)
                with open(
                    "downloads/"
                    + npTitleID
                    + "/"
                    + entitlementID
                    + "/"
                    + data["id"]
                    + ".json",
                    "w",
                ) as file:
                    print("Saving... " + data["id"] + ".json")
                    file.write(json_str)
                file.close()

                # Output icon to file(s)
                ## Save icons extracted from JSON
                for i in data["images"]:
                    if isinstance(i, dict):
                        for k, v in i.items():
                            if k == "url":
                                response = requests.get(v).content
                                with open(
                                    "downloads/"
                                    + npTitleID
                                    + "/"
                                    + entitlementID
                                    + "/"
                                    + str(v[58:]),
                                    "wb",
                                ) as file:
                                    print("Saving... " + str(v[58:]))
                                    file.write(response)
                                file.close()

                ## Save icon from official API /image endpoint
                response = requests.get(url + "/image").content
                with open(
                    "downloads/"
                    + npTitleID
                    + "/"
                    + entitlementID
                    + "/"
                    + data["id"]
                    + ".jpg",
                    "wb",
                ) as file:
                    print("Saving... " + data["id"] + ".jpg")
                    file.write(response)
                file.close()

                ## Save promomedia extracted from JSON
                try:
                    for i in data["promomedia"][0]["materials"][0]["urls"]:
                        if isinstance(i, dict):
                            for k, v in i.items():
                                if k == "url":
                                    response = requests.get(v).content
                                    with open(
                                        "downloads/"
                                        + npTitleID
                                        + "/"
                                        + entitlementID
                                        + "/"
                                        + str(v[49:]),
                                        "wb",
                                    ) as file:
                                        print("Saving... " + str(v[49:]))
                                        file.write(response)
                                    file.close()
                except:
                    pass

                print("\n", end="")
                counter+=1

        except:
            os.rmdir("downloads/" + npTitleID + "/" + entitlementID)
            with open("downloads/" + "errlog.log", "a") as file:
                file.write(url+"\n")
            file.close()