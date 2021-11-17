import json
import requests

#Read .json-File
def readJson(read):
    with open(read) as json_file:
        return json.load(json_file)

#Empty a given JSON-File
def emptyJsonFile(empty):
    with open(empty, "w") as outfile:
        outfile.write('')

#Store a given JSON Object in a File
def storeOutputJsonData(toStore):
    with open("currentValues.json", "a") as outfile: 
        outfile.write(toStore)