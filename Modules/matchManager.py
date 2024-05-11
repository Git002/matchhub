from flask import request, jsonify
import json
from datetime import datetime

from models import db, MatchesTable, TeamsTable, PlayersTable
from Modules.validator import validate_schema, INVALID_SCHEMA_MESSAGE
from schemas import addMatchSchema, addTeamSchema, addPlayersSchema

ERROR_MSG = ""


def validate_match_data(req_body):
    global ERROR_MSG
    if "won" not in req_body:
        ERROR_MSG = "Match must have a winner"
        return False

    if "player_of_the_match" not in req_body:
        ERROR_MSG = "Match must have a player of the match"
        return False

    if req_body["won"] not in [req_body["team_1"], req_body["team_2"]]:
        ERROR_MSG = "Invalid team won"
        return False

    if req_body["team_1"] == req_body["team_2"]:
        ERROR_MSG = "Invalid teams"
        return False

    return True


class MatchManager:
    def __init__(self, sql, flask_instance):
        self.sql = sql
        self.flask_instance = flask_instance

    def add_match(self):
        req_body = json.loads(request.data)

        if not validate_schema(req_body, addMatchSchema):
            return INVALID_SCHEMA_MESSAGE, 400

        if req_body["status"] == "played":
            if not validate_match_data(req_body):
                return jsonify({"message": ERROR_MSG, "data": []}), 400

            with self.flask_instance.app_context():
                db.session.add(
                    MatchesTable(
                        date=datetime.strptime(req_body["date"], "%Y-%m-%d"),
                        team_1=req_body["team_1"],
                        team_2=req_body["team_2"],
                        venue=req_body["venue"],
                        player_of_the_match=req_body["player_of_the_match"],
                        won=req_body["won"],
                        status=req_body["status"],
                    )
                )
                db.session.commit()

        else:
            with self.flask_instance.app_context():
                db.session.add(
                    MatchesTable(
                        date=datetime.strptime(req_body["date"], "%Y-%m-%d"),
                        team_1=req_body["team_1"],
                        team_2=req_body["team_2"],
                        venue=req_body["venue"],
                        status=req_body["status"],
                    )
                )
                db.session.commit()

        return jsonify({"message": "Match added successfully", "data": []}), 201

    def get_matches(self):
        if "date" in request.args:
            matches = MatchesTable.query.filter_by(
                date=datetime.strptime(request.args.get("date"), "%Y-%m-%d").date()
            ).all()
        else:
            matches = MatchesTable.query.all()

        match_list = []

        for match in matches:
            team_1_name = TeamsTable.query.filter_by(id=match.team_1).first().team_name
            team_2_name = TeamsTable.query.filter_by(id=match.team_2).first().team_name
            match_list.append(
                {
                    "date": match.date.strftime("%Y-%m-%d"),
                    "team_1": team_1_name,
                    "team_2": team_2_name,
                    "venue": match.venue,
                    "player_of_the_match": match.player_of_the_match,
                    "won": match.won,
                    "status": match.status,
                }
            )

        return (
            jsonify({"message": "Matches fetched successfully", "data": match_list}),
            200,
        )

    def get_match_by_id(self, match_id):
        match = MatchesTable.query.filter_by(match_id=match_id).first()

        if not match:
            return jsonify({"message": "Match not found", "data": []}), 404

        return (
            jsonify(
                {
                    "message": "Match fetched successfully",
                    "data": {
                        "date": match.date.strftime("%Y-%m-%d"),
                        "team_1": match.team_1,
                        "team_2": match.team_2,
                        "venue": match.venue,
                        "player_of_the_match": match.player_of_the_match,
                        "won": match.won,
                        "status": match.status,
                    },
                }
            ),
            200,
        )

    def update_match(self, match_id):
        req_body = json.loads(request.data)

        if not validate_schema(req_body, addMatchSchema):
            return INVALID_SCHEMA_MESSAGE, 400

        if req_body["status"] == "played":
            if not validate_match_data(req_body):
                return jsonify({"message": ERROR_MSG, "data": []}), 400

            with self.flask_instance.app_context():
                match = MatchesTable.query.filter_by(match_id=match_id).first()
                match.date = datetime.strptime(req_body["date"], "%Y-%M-%d")
                match.team_1 = req_body["team_1"]
                match.team_2 = req_body["team_2"]
                match.venue = req_body["venue"]
                match.player_of_the_match = req_body["player_of_the_match"]
                match.won = req_body["won"]
                match.status = req_body["status"]
                db.session.commit()

        else:
            with self.flask_instance.app_context():
                match = MatchesTable.query.filter_by(id=match_id).first()
                match.date = datetime.strptime(req_body["date"], "%Y-%M-%d")
                match.team_1 = req_body["team_1"]
                match.team_2 = req_body["team_2"]
                match.venue = req_body["venue"]
                match.status = req_body["status"]
                db.session.commit()

        return jsonify({"message": "Match updated successfully", "data": []}), 200

    def get_performance(self, team_id):
        matches = MatchesTable.query.filter(
            (MatchesTable.team_1 == team_id) | (MatchesTable.team_2 == team_id),
            MatchesTable.status == "played",
        ).all()

        if not matches:
            return (
                jsonify(
                    {
                        "message": "No matches found for the team",
                        "data": [],
                    }
                ),
                404,
            )

        total_matches = 0
        won_matches = 0

        for match in matches:
            total_matches += 1
            if match.won == team_id:
                won_matches += 1

        # Formula to calculate win percentage
        win_percentage = (won_matches / total_matches) * 100

        return (
            jsonify(
                {
                    "message": "Performance fetched successfully",
                    "data": [
                        {
                            "total_matches": total_matches,
                            "won_matches": won_matches,
                            "lost_matches": total_matches - won_matches,
                            "win_percentage": win_percentage,
                        }
                    ],
                }
            ),
            200,
        )

    def add_team(self):
        req_body = json.loads(request.data)

        if not validate_schema(req_body, addTeamSchema):
            return INVALID_SCHEMA_MESSAGE, 400

        with self.flask_instance.app_context():
            db.session.add(
                TeamsTable(
                    team_name=req_body["team_name"],
                    team_captain=req_body["team_captain"],
                )
            )
            db.session.commit()

        return jsonify({"message": "Team added successfully", "data": []}), 201

    def get_teams(self):
        teams = TeamsTable.query.all()

        team_list = []

        for team in teams:
            team_list.append(
                {
                    "team_name": team.team_name,
                    "team_captain": team.team_captain,
                }
            )

        return (
            jsonify({"message": "Teams fetched successfully", "data": team_list}),
            200,
        )

    def get_players(self):
        players = PlayersTable.query.all()

        player_list = []

        for player in players:
            player_list.append(
                {
                    "player_name": player.player_name,
                }
            )

        return (
            jsonify({"message": "Players fetched successfully", "data": player_list}),
            200,
        )

    def add_players(self):
        req_body = json.loads(request.data)

        if not validate_schema(req_body, addPlayersSchema):
            return INVALID_SCHEMA_MESSAGE, 400

        with self.flask_instance.app_context():
            for player in req_body["players"]:
                db.session.add(
                    PlayersTable(
                        team_id=req_body["team_id"],
                        player_name=player,
                    )
                )
            db.session.commit()

        return jsonify({"message": "Players added successfully", "data": []}), 201
