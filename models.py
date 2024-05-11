from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EmployeeTable(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.Text())
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    role = db.Column(db.String(10))


class MatchesTable(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    team_1 = db.Column(db.Integer)
    team_2 = db.Column(db.Integer)
    venue = db.Column(db.String(50))
    player_of_the_match = db.Column(db.String(50))
    won = db.Column(db.Integer)
    status = db.Column(db.String(20))


class TeamsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(50))
    team_captain = db.Column(db.String(50))


class PlayersTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer)
    player_name = db.Column(db.String(50))
