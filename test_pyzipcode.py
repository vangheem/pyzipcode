import unittest
import pyzipcode

db = pyzipcode.ZipCodeDatabase()

def test_retrieves_zip_code_information():
    zip = db["54115"]
    assert zip.zip == "54115"
    assert zip.city == "De Pere"
    assert zip.state == "WI"

def test_correct_longitude_value():
    zip = db[54115]
    assert zip.latitude > 44.42041 and zip.latitude < 44.42043

def test_correct_latitude_value():
    zip = db[54115]
    assert zip.longitude > -88.07897 and zip.longitude < -88.07895

def test_correct_timezone():
    zip = db[54115]
    assert zip.timezone == -6

def test_correct_dst():
    zip = db[54115]
    assert zip.dst == 1

def test_radius():
    zips = db.get_zipcodes_around_radius("54115", 30)
    assert "54304" in [zip.zip for zip in zips]

def test_find_zip_by_city():
    zip = db.find_zip(city="De Pere")[0]
    assert "54115" == zip.zip

def test_find_zip_by_city_with_multiple_zips():
    zips = db.find_zip(city="Green Bay")
    assert "54302" in [zip.zip for zip in zips]

def test_find_zips_in_state():
    zips = db.find_zip(state="WI")
    assert "54304" in [zip.zip for zip in zips]
    assert "54901" in [zip.zip for zip in zips]

def test_data():
    assert len(db) == len(list(db.values())) == len(list(db.items())) == len(list(db.keys()))

    for zip, zip_obj in db.items():
        assert zip == zip_obj.zip
        assert zip.isdigit()
