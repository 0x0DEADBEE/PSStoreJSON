from sys import argv
import requests
import json
import os

# Set API search parameters
server = "https://store.playstation.com/store/api"
country = argv[2]
language = argv[3]
serviceIDPrefix = argv[4]
npTitleID = str(argv[5] + "_00")

# Retrieve ContentID by iterating the '*.dlc' files
with open(argv[1], "r") as ContentID:
    for line in ContentID:
        if "ContentID" in line:
            entitlementID = str(line[13:][:16])
            
            # Create folder for files to be saved to
            os.makedirs(str(npTitleID) + "/" + str(entitlementID), exist_ok=True)
            url = (
                server
                + "/chihiro/00_09_000/container/"
                + country
                + "/"
                + language
                + "/999/"
                + serviceIDPrefix
                + "-"
                + npTitleID
                + "-"
                + entitlementID
            )
            # Request data from API
            response = requests.get(url)
            data = response.json()
            # Save the data requested from API
            try:
                # Show current Content ID
                print("\n" + data["id"] + " | " + data["name"])

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
                                    npTitleID
                                    + "/"
                                    + entitlementID
                                    + "/"
                                    + str(v[58:]),
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
                    for i in data['promomedia'][0]['materials'][0]['urls']:
                        if isinstance(i, dict):
                            for k, v in i.items():
                                if k == 'url':
                                    response = requests.get(v).content
                                    with open(
                                        npTitleID
                                        + "/"
                                        + entitlementID
                                        + "/"
                                        + str(v[49:]),
                                        "wb",
                                    ) as file:
                                        print("Saving... " + str(v[49:]))
                                        file.write(response)
                except:
                    pass                           

                ##PLACEHOLDER for 'https://image.api.playstation.com/cdn'


            except:
                os.rmdir(npTitleID + "/" + entitlementID)
                print("Invalid entitlement ID:" + str(entitlementID))
                with open(npTitleID + "/" + "errlog.log", "a") as file:
                    file.write(entitlementID + " | INVALID\n")
                file.close()

