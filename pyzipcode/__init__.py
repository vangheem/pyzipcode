"""The pyzipcode package"""


import sqlite3
import time
from collections.abc import Mapping

from pyzipcode.settings import db_location


class ConnectionManager:
    """
    Assumes a database that will work with cursor objects
    """

    def __init__(self):
        # test out the connection...
        conn = sqlite3.connect(db_location)
        conn.close()

    def query(self, sql, params=None):
        """
        Query the database using the supplied SQL. The SQL should follow the
        formatting rules defined in :pep:`249` for SQLite, whos `paramstyle` is
        `qmark`. Doing so will protect against SQL injection attacks.

        For example::

           sql = "SELECT * FROM ZipCodes WHERE zip=?"
           params = ('94949',)

        """
        conn = None
        retry_count = 0
        while not conn and retry_count <= 10:
            # If there is trouble reading the file, retry for 10 attempts
            # then just give up...
            try:
                conn = sqlite3.connect(db_location)
            except sqlite3.OperationalError:
                retry_count += 1
                time.sleep(0.001)

        if not conn and retry_count > 10:
            raise sqlite3.OperationalError(
                f"Can't connect to sqlite database: {db_location!r}."
            )

        cursor = conn.cursor()
        if params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        res = cursor.fetchall()
        conn.close()
        return res


ZIP_QUERY = "SELECT * FROM ZipCodes WHERE zip=?"
ZIP_RANGE_QUERY = (
    "SELECT * FROM ZipCodes "
    "WHERE longitude >= ? "
    "  AND longitude <= ? "
    "  AND latitude >= ? "
    "  AND latitude <= ?"
)
ZIP_FIND_QUERY = "SELECT * FROM ZipCodes WHERE city LIKE ? AND state LIKE ?"
ZIP_ALL_QUERY = "SELECT zip FROM ZipCodes ORDER BY zip ASC"
ZIP_ALL_REVERSED_QUERY = "SELECT zip FROM ZipCodes ORDER BY zip DESC"
ZIP_LEN_QUERY = "SELECT COUNT(*) FROM ZipCodes"


class ZipCode:
    """
    Represents one zipcode record from the database.
    """

    def __init__(self, zip, city, state, longitude, latitude, timezone, dst):
        self.zip = zip
        self.city = city
        self.state = state
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.dst = dst

    def __repr__(self):
        attrs = ["zip", "city", "state", "longitude", "latitude", "timezone", "dst"]
        attrs = ', '.join(f'{a}={repr(getattr(self, a))}' for a in attrs)
        return f"{self.__class__.__name__}({attrs})"


def format_result(zips):
    """
    Helper function to format the display of zipcode[s].
    Returns a list of ZipCode objects.
    """
    if len(zips) > 0:
        return [ZipCode(*zc) for zc in zips]
    else:
        return None


class ZipNotFoundException(Exception):
    """
    Exception that is raised when a zipcode is not found in the database
    """

    pass


class ZipCodeDatabase(Mapping):
    """
    Interface to the zipcode lookup functionality
    """

    def __init__(self, conn_manager=None):
        if conn_manager is None:
            conn_manager = ConnectionManager()
        self.conn_manager = conn_manager

    def get_zipcodes_around_radius(self, zipcode, radius):
        """
        Returns a list of ZipCode objects within radius miles of the zipcode.
        """
        zipcode = self.get(zipcode)
        if zipcode is None:
            raise ZipNotFoundException(
                f"Could not find zipcode '{zipcode}' within radius {radius}"
            )

        radius = float(radius)

        long_range = (
            zipcode.longitude - (radius / 69.0),
            zipcode.longitude + (radius / 69.0),
        )
        lat_range = (
            zipcode.latitude - (radius / 49.0),
            zipcode.latitude + (radius / 49.0),
        )

        return format_result(
            self.conn_manager.query(
                ZIP_RANGE_QUERY,
                (long_range[0], long_range[1], lat_range[0], lat_range[1]),
            )
        )

    def find_zip(self, city=None, state=None):
        """
        Returns a list of ZipCode objects, optionally filtered by city and
        state. The filters are case-insensitive.
        """
        if city is None:
            city = "%"
        else:
            city = city.upper()

        if state is None:
            state = "%"
        else:
            state = state.upper()

        return format_result(self.conn_manager.query(ZIP_FIND_QUERY, (city, state)))


    def get(self, zipcode, default=None):
        """
        Returns the ZipCode object representing the given zipcode, or `default` if
        one can't be found.
        """
        result = format_result(self.conn_manager.query(ZIP_QUERY, (zipcode,)))
        if result:
            return result[0]
        return default

    def __getitem__(self, zipcode):
        data = self.get(str(zipcode).zfill(5))
        if data is None:
            raise KeyError(f"Couldn't find zipcode: '{zipcode}'")
        else:
            return data

    def __iter__(self):
        for zip in self.conn_manager.query(ZIP_ALL_QUERY):
            yield zip[0]

    def __reversed__(self):
        for zip in self.conn_manager.query(ZIP_ALL_REVERSED_QUERY):
            yield zip[0]

    def __len__(self):
        return self.conn_manager.query(ZIP_LEN_QUERY)[0][0]
