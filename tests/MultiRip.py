import requests
import csv
import json
import os

language = ""
country = ""

with open("lbp.csv", "r") as file:
    csvFile = csv.reader(file)
    next(csvFile)
    for entries in csvFile:
        contentID = entries[1]
        serviceIDPrefix = contentID[0:6]
        npTitleID = contentID[7:19]
        entitlementID = contentID[20:36]
        if serviceIDPrefix == "UP9000":
            language = "en"
            country = "hu"
            print('"' + entries[0] + '"' + "," + '"' + contentID + '"')
            with open("UP9000.csv", "a") as file:
                file.write(
                    str(
                        '"'
                        + str(entries[0])
                        + '"'
                        + ","
                        + '"'
                        + str(contentID)
                        + '"'
                        + "\n"
                    )
                )
            file.close()
        elif serviceIDPrefix == "EP9000":
            language = "en"
            country = "hu"
            print('"' + entries[0] + '"' + "," + '"' + contentID + '"')
            with open("EP9000.csv", "a") as file:
                file.write(
                    str(
                        '"'
                        + str(entries[0])
                        + '"'
                        + ","
                        + '"'
                        + str(contentID)
                        + '"'
                        + "\n"
                    )
                )
            file.close()
            print('"' + entries[0] + '"' + "," + '"' + contentID + '"')
        elif serviceIDPrefix == "HP9000":
            language = "en"
            country = "hk"
        elif serviceIDPrefix == "JP9000":
            language = "ja"
            country = "jp"
