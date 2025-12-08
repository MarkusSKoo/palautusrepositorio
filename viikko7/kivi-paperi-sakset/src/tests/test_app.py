import pytest

from app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        client.get("/reset")
        yield client


def test_play_round_updates_scoreboard_and_shows_moves(client):
    response = client.post("/", data={"siirto": "k", "ai": "easy"})
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert any(msg in body for msg in ["Voitit!", "Hävisit.", "Tasapeli!"])
    assert "Pelitilanne:" in body
    assert "Sinä: k" in body
    assert "Tekoäly:" in body


def test_invalid_move_shows_error_and_keeps_score(client):
    response = client.post("/", data={"siirto": "x", "ai": "easy"})
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Virheellinen siirto" in body
    assert "Pelitilanne: 0 - 0" in body


def test_game_ends_when_player_reaches_three_wins(client):
    winning_moves = ["s", "k", "p"]  # beats AI cycle p, s, k

    last_body = ""
    for move in winning_moves:
        resp = client.post("/", data={"siirto": move, "ai": "easy"})
        last_body = resp.get_data(as_text=True)
        assert resp.status_code == 200

    assert "Pääsit viiteen voittoon!" in last_body
    assert "Pelitilanne: 3 - 0" in last_body

    # Additional move should not change score and should keep end-of-game message
    resp_after = client.post("/", data={"siirto": "k", "ai": "easy"})
    after_body = resp_after.get_data(as_text=True)
    assert "Pääsit viiteen voittoon!" in after_body
    assert "Pelitilanne: 3 - 0" in after_body


def test_switching_ai_resets_score(client):
    # Play one round with easy AI to change the score
    resp_easy = client.post("/", data={"siirto": "k", "ai": "easy"})
    body_easy = resp_easy.get_data(as_text=True)
    assert resp_easy.status_code == 200
    assert "Pelitilanne:" in body_easy

    # Switch to better AI and play a round; score should start from zero again
    resp_switch = client.post("/", data={"siirto": "k", "ai": "better"})
    body_switch = resp_switch.get_data(as_text=True)
    assert resp_switch.status_code == 200
    assert "Pelitilanne: 0 - 0" in body_switch or "Pelitilanne: 1 - 0" in body_switch or "Pelitilanne: 0 - 1" in body_switch
    assert "Parempi tekoäly" in body_switch

