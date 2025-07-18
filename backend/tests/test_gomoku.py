
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_basic_move():
    client.post("/game/reset")

    move = {"player": "black", "x": 0, "y": 0}
    res = client.post("/game/move", json=move)
    assert res.status_code == 200
    assert res.json()["board"]["black"] == [[0, 0]]

    move = {"player": "white", "x": 1, "y": 0}
    res = client.post("/game/move", json=move)
    assert res.status_code == 200
    assert res.json()["board"]["white"] == [[1, 0]]

def test_conflict_move():
    client.post("/game/reset")

    move = {"player": "black", "x": 3, "y": 3}
    res = client.post("/game/move", json=move)
    assert res.status_code == 200

    move = {"player": "white", "x": 3, "y": 3}
    res = client.post("/game/move", json=move)
    assert res.status_code == 400  

def test_win_case():
    client.post("/game/reset")

    for i in range(5):
        move_black = {"player": "black", "x": i, "y": 0}
        res = client.post("/game/move", json=move_black)
        assert res.status_code == 200
        if i < 4:
            move_white = {"player": "white", "x": i, "y": 1}
            res = client.post("/game/move", json=move_white)
            assert res.status_code == 200

    final = client.get("/game/board")
    assert final.status_code == 200
    assert final.json()["winner"] == "black"