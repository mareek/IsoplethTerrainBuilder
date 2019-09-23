import sqlite3
from geoCoordinates import location


class locationDatabase:
    def __init__(self, databaseFilePath=":memory:"):
        self.connection = sqlite3.connect(databaseFilePath)
        self._initDatabase()

    # create table if it does not exists
    def _initDatabase(self):
        cur = self.connection.cursor()
        cur.execute("create table if not exists location(latitude real not null, longitude real not null, elevation int not null, primary key(latitude, longitude))")
        cur.execute("create index if not exists idx_location_latitude on location(latitude)")
        cur.execute("create index if not exists idx_location_longitude on location(longitude)")
        cur.close()

    # Get location from the database
    def getLocation(self, latitude, longitude):
        cur = self.connection.cursor()
        cur.execute("select elevation from location where latitude = ? and longitude = ?", (latitude, longitude))
        elevationTuple = cur.fetchone()
        cur.close()
        if elevationTuple == None:
            return None
        else:
            return location(latitude, longitude, elevationTuple[0])

    # Add the location to the database
    def addLocation(self, location):
        row = (location.latitude, location.longitude, location.elevation)
        self.connection.execute("insert into location (latitude, longitude, elevation) values (?,?,?)", row)
