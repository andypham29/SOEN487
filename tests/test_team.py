import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Team, City

tested_app.config.from_object(TestConfig)


class TestTeam(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(City(id=1, city_name="new york", country="us"))
        self.db.session.add(City(id=2, city_name="columbus", country="us"))
        self.db.session.add(Team(id=1, team_name="islanders", association="east", division="metropolitan", city_id=1))
        self.db.session.add(
            Team(id=2, team_name="blue jackets", association="east", division="metropolitan", city_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        City.query.delete()
        Team.query.delete()
        self.db.session.commit()

    def test_get_all_team(self):
        # send the request and check the response status code
        response = self.app.get("/team")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        team_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(team_list), list)
        self.assertDictEqual(team_list[0],
                             {"id": "1", "team_name": "islanders", "association": "east", "division": "metropolitan",
                              "city_id": "1"})
        self.assertDictEqual(team_list[1],
                             {"id": "2", "team_name": "blue jackets", "association": "east",
                              "division": "metropolitan", "city_id": "2"})

    def test_get_team_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/team/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        team = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(team,
                             {"id": "1", "team_name": "islanders", "association": "east", "division": "metropolitan",
                              "city_id": "1"})

    def test_get_team_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/team/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this team id."})

    def test_put_team_without_id(self):
        # do we really need to check counts?
        initial_count = Team.query.filter_by(team_name="islanders").count()

        # send the request and check the response status code
        response = self.app.put("/team", data={"team_name": "islanders", "association": "east",
                                               "city_id": "1", "division": "metropolitan"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Team.query.filter_by(team_name="islanders").count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_put_team_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/team", data={"id": "1", "team_name": "rangers", "association": "east",
                                               "city_id": "1", "division": "metropolitan"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        team = Team.query.filter_by(id=1).first()
        self.assertEqual(team.team_name, "rangers")
