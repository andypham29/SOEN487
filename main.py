from flask import Flask, jsonify, make_response, request, render_template, redirect
from config import DevConfig
from config import Config

import sqlalchemy

# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, Player, Team, City

app.config.from_object(Config)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    json = {"title": "SOEN487 Assignment 1",
            "student": {"id": "40006071", "name": "Andy Pham"}}
    players = Player.query.all()
    teams = Team.query.all()
    cities = City.query.all()

    return render_template("index.html", json=json, players=players, teams=teams, cities=cities)


# ----------------------------------------------Player Routes-----------------------------------------------------------
@app.route("/player")
def get_all_player():
    player_list = Player.query.all()
    return jsonify([row2dict(player) for player in player_list])


@app.route("/player/<player_id>")
def get_player(player_id):
    # id is a primary key, so we'll have max 1 result row
    player = Player.query.filter_by(id=player_id).first()
    if player:
        return jsonify(row2dict(player))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this player id."}), 404)


@app.route("/player", methods={"POST"})
def post_player():
    name = request.form.get("name")
    team_id = request.form.get("team_id")
    player = Player(name=name, team_id=team_id)

    db.session.add(player)
    db.session.commit()

    return jsonify({"code": 200, "msg": "success"})


@app.route("/player", methods={"PUT"})
def put_player():
    # get the name first, if no name then fail
    name = request.form.get("name")
    team_id = request.form.get("team_id")
    if not name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put player. Missing mandatory fields."}), 403)
    player_id = request.form.get("id")
    if not player_id:
        p = Player(name=name, team_id=team_id)
    else:
        p = Player(id=player_id, name=name, team_id=team_id)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put player. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": player_id})


@app.route("/player/<player_id>", methods={"DELETE"})
def delete_player(player_id):
    player = Player.query.filter_by(id=player_id).first()
    if player:
        db.session.delete(player)
        db.session.commit()
        return make_response(jsonify({"code": 200, "msg": "Deletion successful."}), 200)
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this player id."}), 404)


# ----------------------------------------------Team Routes------------------------------------------------------------

@app.route("/team")
def get_all_team():
    team_list = Team.query.all()
    return jsonify([row2dict(team) for team in team_list])


@app.route("/team/<team_id>")
def get_team(team_id):
    # id is a primary key, so we'll have max 1 result row
    team = Team.query.filter_by(id=team_id).first()
    if team:
        return jsonify(row2dict(team))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this team id."}), 404)


@app.route("/team", methods={"POST"})
def post_team():
    team_name = request.form.get("team_name")
    association = request.form.get("association")
    division = request.form.get("division")
    city_id = request.form.get("city_id")
    team = Team(team_name=team_name, association=association, division=division, city_id=city_id)

    db.session.add(team)
    db.session.commit()

    return jsonify({"code": 200, "msg": "success"})


@app.route("/team", methods={"PUT"})
def put_team():
    # get the name first, if no name then fail
    team_name = request.form.get("team_name")
    association = request.form.get("association")
    division = request.form.get("division")
    city_id = request.form.get("city_id")
    if not team_name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put team. Missing mandatory fields."}), 403)
    team_id = request.form.get("id")
    if not team_id:
        p = Team(team_name=team_name, association=association, division=division, city_id=city_id)
    else:
        p = Team(id=team_id, team_name=team_name, association=association, division=division, city_id=city_id)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put team. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": team_id})


@app.route("/team/<team_id>", methods={"DELETE"})
def delete_team(team_id):
    team = Team.query.filter_by(id=team_id).first()
    if team:
        db.session.delete(team)
        db.session.commit()
        return make_response(jsonify({"code": 200, "msg": "Deletion successful."}), 200)
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this team id."}), 404)


# ----------------------------------------------City Routes------------------------------------------------------------

@app.route("/city")
def get_all_city():
    city_list = City.query.all()
    return jsonify([row2dict(city) for city in city_list])


@app.route("/city/<city_id>")
def get_city(city_id):
    # id is a primary key, so we'll have max 1 result row
    city = City.query.filter_by(id=city_id).first()
    if city:
        return jsonify(row2dict(city))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this city id."}), 404)


@app.route("/city", methods={"POST"})
def post_city():
    city_name = request.form.get("city_name")
    country = request.form.get("country")
    city = City(city_name=city_name, country=country)

    db.session.add(city)
    db.session.commit()

    return jsonify({"code": 200, "msg": "success"})


@app.route("/city", methods={"PUT"})
def put_city():
    # get the name first, if no name then fail
    name = request.form.get("name")
    team_id = request.form.get("team_id")
    if not name:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put city. Missing mandatory fields."}), 403)
    city_id = request.form.get("id")
    if not city_id:
        p = City(name=name, team_id=team_id)
    else:
        p = City(id=city_id, name=name, team_id=team_id)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put city. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": city_id})


@app.route("/city/<city_id>", methods={"DELETE"})
def delete_city(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city:
        db.session.delete(city)
        db.session.commit()
        return make_response(jsonify({"code": 200, "msg": "Deletion successful."}), 200)
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this city id."}), 404)


if __name__ == '__main__':
    app.run()
