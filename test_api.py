from app import app


def test_create_teams():
    client = app.test_client()

    # Team A creation
    data = {"team_name": "Team A", "team_captain": "CA"}
    response = client.post("/public/teams", json=data)

    assert response.status_code == 201

    # Team B creation
    data = {"team_name": "Team B", "team_captain": "CB"}
    response = client.post("/public/teams", json=data)

    assert response.status_code == 201


def test_get_teams():
    client = app.test_client()

    response = client.get("/public/teams")

    assert response.status_code == 200


def test_match_addition():
    client = app.test_client()

    # Match 1
    data = {
        "date": "2024-05-29",
        "team_1": 1,
        "team_2": 2,
        "venue": "ZZZ stadium",
        "player_of_the_match": "Z",
        "won": 2,
        "status": "played",
    }

    response = client.post("/public/matches", json=data)

    assert response.status_code == 201

    # Match 2
    data = {
        "date": "2024-05-30",
        "team_1": 2,
        "team_2": 1,
        "venue": "YYY stadium",
        "player_of_the_match": "Y",
        "won": 1,
        "status": "played",
    }

    response = client.post("/public/matches", json=data)

    assert response.status_code == 201


def test_get_matches():
    client = app.test_client()

    response = client.get("/public/matches")

    assert response.status_code == 200


def test_get_match_by_date():
    client = app.test_client()

    response = client.get("/public/matches?date=2024-05-30")

    assert response.status_code == 200


def test_get_match_by_id():
    client = app.test_client()

    response = client.get("/public/matches/1")

    assert response.status_code == 200


def test_update_match_by_id():
    client = app.test_client()

    data = {
        "date": "2024-05-29",
        "team_1": 1,
        "team_2": 2,
        "venue": "ZZZ stadium",
        "player_of_the_match": "Z",
        "won": 2,
        "status": "played",
    }

    response = client.put("/public/matches/1", json=data)

    assert response.status_code == 200


def test_performance():
    client = app.test_client()

    response = client.get("/public/performance/1")

    assert response.status_code == 200
