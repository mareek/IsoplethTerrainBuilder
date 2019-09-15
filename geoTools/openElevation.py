import requests
import json
import time
from geoCoordinates import location


class postParameter:
    def __init__(self):
        self.locations = []

    def addLocation(self, location):
        self.locations.append(location)


def downloadLocations(locations):
    postPayload = postParameter()
    for location in locations:
        postPayload.addLocation(location)

    elevationApiUrl = 'https://api.open-elevation.com/api/v1/lookup'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    jsonPayload = json.dumps(postPayload, default=lambda o: o.__dict__)

    result = None
    while result == None:
        try:
            result = requests.post(elevationApiUrl, data=jsonPayload, headers=headers)
            if not result.ok:
                result = None
                time.sleep(0.5)
        except:
            result = None
            time.sleep(0.5)

    jsonResult = result.json()
    return list(map(location.from_json, jsonResult["results"]))