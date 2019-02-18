import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Player, Team, City

tested_app.config.from_object(TestConfig)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(City(id=1, city_name="montreal", country="canada"))
        self.db.session.add(Team(id=2, team_name="canadiens", association="east", division="atlantic", city_id=1))
        self.db.session.add(Player(id=1, name="Maurice Richard", team_id=1))
        self.db.session.add(Player(id=2, name="PK Subban", team_id=1))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Player.query.delete()
        City.query.delete()
        Team.query.delete()
        self.db.session.commit()

    def test_get_all_player(self):
        # send the request and check the response status code
        response = self.app.get("/player")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        player_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(player_list), list)
        self.assertDictEqual(player_list[0], {"id": "1", "name": "Maurice Richard", "team_id": "1"})
        self.assertDictEqual(player_list[1], {"id": "2", "name": "PK Subban", "team_id": "1"})

    def test_get_player_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/player/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        player = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(player, {"id": "1", "name": "Maurice Richard", "team_id": "1"})

    def test_get_player_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/player/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this player id."})

    def test_put_player_without_id(self):
        # do we really need to check counts?
        initial_count = Player.query.filter_by(name="Maurice Richard").count()

        # send the request and check the response status code
        response = self.app.put("/player", data={"name": "Maurice Richard", "team_id": "1"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Player.query.filter_by(name="Maurice Richard").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_player_with_id(self):
        # send the request and check the response status code
        init_val = Player.query.filter_by(id=2).first().name
        response = self.app.put("/player", data={"id": "2", "name": "Shea Weber", "team_id": "1"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        player = Player.query.filter_by(id=2).first()
        self.assertEqual(init_val, "PK Subban")
        self.assertEqual(player.name, "Shea Weber")
