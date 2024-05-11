addMatchSchema = {
    "type": "object",
    "properties": {
        "date": {"type": "string"},
        "team_1": {"type": "number"},
        "team_2": {"type": "number"},
        "venue": {"type": "string"},
        "player_of_the_match": {"type": "string"},
        "won": {"type": "number"},
        "status": {"type": "string", "enum": ["cancel", "played", "draw", "upcoming"]},
    },
    "required": [
        "date",
        "team_1",
        "team_2",
        "venue",
        "status",
    ],
    "additionalProperties": False,
}

addTeamSchema = {
    "type": "object",
    "properties": {
        "team_name": {"type": "string"},
        "team_captain": {"type": "string"},
    },
    "required": ["team_name", "team_captain"],
    "additionalProperties": False,
}

addPlayersSchema = {
    "type": "object",
    "properties": {
        "players": {"type": "array", "items": {"type": "string"}},
        "team_id": {"type": "number"},
    },
    "required": ["players", "team_id"],
    "additionalProperties": False,
}
