import requests
import json
import time
from geoTools.geoCoordinates import location


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
                raise Exception()
        except:
            result = None
            time.sleep(0.5)

    jsonResult = result.json()
    return list(map(location.from_json, jsonResult["results"]))


def computeFakeAltitude(location):
    latitudeStr = str(location.latitude)
    longitudeStr = str(location.longitude)
    elevationStr = latitudeStr[-1:] + longitudeStr[-2:]
    return int(elevationStr)


def fakeDownloadLocations(locations):
    return map(lambda l: location(l.latitude, l.longitude, computeFakeAltitude(l)), locations)
