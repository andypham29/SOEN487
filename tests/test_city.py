import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import City

tested_app.config.from_object(TestConfig)


class TestCity(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(City(id=1, city_name="montreal", country="canada"))
        self.db.session.add(City(id=2, city_name="boston", country="us"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        City.query.delete()
        self.db.session.commit()

    def test_get_all_city(self):
        # send the request and check the response status code
        response = self.app.get("/city")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        city_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(city_list), list)
        self.assertDictEqual(city_list[0], {"id": "1", "name": "Alice"})
        self.assertDictEqual(city_list[1], {"id": "2", "name": "Bob"})

    def test_get_city_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/city/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        city = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(city, {"id": "1", "name": "Alice"})

    def test_get_city_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/city/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this city id."})

    def test_put_city_without_id(self):
        # do we really need to check counts?
        initial_count = City.query.filter_by(name="Amy").count()

        # send the request and check the response status code
        response = self.app.put("/city", data={"name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = City.query.filter_by(name="Amy").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_city_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/city", data={"id": 3, "name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        city = City.query.filter_by(id=3).first()
        self.assertEqual(city.name, "Amy")
