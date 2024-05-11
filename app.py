from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from models import db
from Modules.helperFunctions import Helper
from Modules.matchManager import MatchManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "LsVQV5TiTTyONXK93eIlY3EF62ghFRUL1"
app.config["WTF_CSRF_ENABLED"] = False

CORS(app, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///support.db/"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 2
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 10

db.init_app(app)

helper = Helper(flask_instance=app)
match_mgr = MatchManager(sql=db, flask_instance=app)


@app.before_request
def middleware():
    if request.endpoint is None:
        return jsonify({"message": "Endpoint not found", "data": []}), 404

    elif request.endpoint.startswith("public") and request.method in [
        "POST",
        "PUT",
        "DELETE",
    ]:
        try:
            json.loads(request.data)
        except (ValueError, json.JSONDecodeError):
            return jsonify({"message": "JSON is invalid", "data": []}), 400


# added '/public' prefix as said by the interviewer...


@app.route("/public", methods=["GET"])
def public():
    return jsonify({"message": "This is a public endpoint", "data": []}), 200


@app.route("/public/matches", methods=["GET", "POST"])
def matches():
    if request.method == "GET":
        return match_mgr.get_matches()
    elif request.method == "POST":
        return match_mgr.add_match()


@app.route("/public/matches/<int:match_id>", methods=["GET", "PUT"])
def match(match_id):
    if request.method == "GET":
        return match_mgr.get_match_by_id(match_id)
    elif request.method == "PUT":
        return match_mgr.update_match(match_id)


@app.route("/public/performance/<int:team_id>", methods=["GET"])
def performance(team_id):
    return match_mgr.get_performance(team_id)


@app.route("/public/teams", methods=["GET", "POST"])
def teams():
    if request.method == "GET":
        return match_mgr.get_teams()
    elif request.method == "POST":
        return match_mgr.add_team()


@app.route("/public/players", methods=["GET", "POST"])
def players():
    if request.method == "GET":
        return match_mgr.get_players()
    elif request.method == "POST":
        return match_mgr.add_players()


if __name__ == "__main__":
    # create tables if not existed
    with app.app_context():
        db.create_all()

    if helper.is_table_empty():
        helper.add_dummy_user()

    app.run(host="0.0.0.0", port=5555, debug=False)
