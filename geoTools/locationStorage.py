import sqlite3
from geoCoordinates import location


class locationDatabase:
    def __init__(self, databaseFilePath=":memory:"):
        self.connection = sqlite3.connect(databaseFilePath)
        self._initDatabase()

    # create table if it does not exists
    def _initDatabase(self):
        pass

    # Get location from the database
    def getLocation(self, latitude, longitude):
        pass

    # Add the location to the database
    def addLocation(self, location):
        pass

