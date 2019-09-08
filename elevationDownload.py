import requests
import json
import time


class location:
    def __init__(self, latitude, longitude, elevation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def toLine(self, separator):
        return separator.join(map(lambda f: str(f), filter(lambda e: e != None, [self.latitude, self.longitude, self.elevation])))

    @staticmethod
    def headerLine(separator):
        return separator.join(['latitude', 'longitude', 'elevation'])

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class postParameter:
    def __init__(self):
        self.locations = []

    def addLocation(self, latitude, longitude):
        self.locations.append(location(latitude, longitude))

    @classmethod
    def from_json(cls, data):
        result = cls()
        result.locations = list(map(location.from_json, data["location"]))
        return result


elevationApiUrl = 'https://api.open-elevation.com/api/v1/lookup'

postPayload = postParameter()
postPayload.addLocation(0, 0)
postPayload.addLocation(45, 0)
postPayload.addLocation(45.2, 3.89)

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
jsonPayload = json.dumps(postPayload, default=lambda o: o.__dict__)

result = None
while result == None:
    try:
        result = requests.post(
            elevationApiUrl, data=jsonPayload, headers=headers)
        if not result.ok:
            result = None
            time.sleep(0.5)
    except:
        result = None
        time.sleep(0.5)

jsonResult = result.json()
resultLocations = map(location.from_json, jsonResult["results"])

resultFile = open("elevations.csv", "w")
resultFile.write(location.headerLine('\t') + '\n')
resultFile.write('\n'.join(map(lambda l: l.toLine('\t'), resultLocations)))
resultFile.close()
