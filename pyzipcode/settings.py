"""
Settings common throughout the pyzipcode package.
"""


import os

# The name of the SQLite database file
db_filename = "zipcodes.db"

# The name of the zipcode CSV file from which the SQLite database is populated
csv_filename = "zipcode.csv"

# The absolute path to the pyzipcode Python package
directory = os.path.dirname(os.path.abspath(__file__))

# The filesystem location of the SQLite database file
db_location = os.path.join(directory, db_filename)

# The filesystem location of the CSV file.
csv_location = os.path.join(directory, csv_filename)
