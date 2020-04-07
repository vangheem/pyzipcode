"""
A script to create the SQLite database of zipcode data from a CSV file
======================================================================

The pyzipcode package includes zipcode data that has already been imported.
This module should not normally need to be run unless the source of zipcode
data changes and/or needs to be reimported.

The code in this module will drop the ZipCodes table and recreate it from the
data in the ``zipcodes.csv`` data file.

Example usage::

   # Assumes the file ./zipcode.csv exists and contains zipcode data
   python import_zipcodes.py

"""

import sqlite3

import csv

try:
    from settings import db_location, csv_location
except ImportError:
    from pyzipcode.settings import db_location, csv_location


def run_import():
    """Run the import code."""
    conn = sqlite3.connect(db_location)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS ZipCodes;")
    c.execute(
        "CREATE TABLE ZipCodes("
        "  zip VARCHAR(5), city TEXT, state TEXT, longitude DOUBLE, "
        "  latitude DOUBLE, timezone INT, dst INT"
        ");"
    )
    c.execute("CREATE INDEX zip_index ON ZipCodes(zip);")
    c.execute("CREATE INDEX city_index ON ZipCodes(city);")
    c.execute("CREATE INDEX state_index ON ZipCodes(state);")

    reader = csv.reader(open(csv_location, "rb"))
    reader.next()  # prime it

    for row in reader:
        zip, city, state, lat, longt, timezone, dst = row

        c.execute(
            'INSERT INTO ZipCodes values("%s", "%s", "%s", %s, %s, %s, %s)'
            % (zip, city, state, float(longt), float(lat), timezone, dst)
        )

    conn.commit()

    # We can also close the cursor if we are done with it
    c.close()


if __name__ == "__main__":
    run_import()
