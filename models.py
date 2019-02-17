from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return "<Player {}: {}>".format(self.id, self.name)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(20), nullable=False)
    association = db.Column(db.String(20), nullable=False)
    division = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    players = db.relationship('Player', backref='player', lazy=True)

    def __repr__(self):
        return "<Team {}: {} {} {}>".format(self.id, self.team_name, self.association, self.division)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    teams = db.relationship('Team', backref='team', lazy=True)

    def __repr__(self):
        return "<City {}: {}, {}>".format(self.id, self.city_name, self.country)
