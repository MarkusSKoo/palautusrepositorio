from flask import Flask, render_template_string, request, redirect, url_for

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)

# Shared instances keep score and AI state between requests.
tuomari = Tuomari()
tekoaly = Tekoaly()
current_ai_type = "easy"

WIN_THRESHOLD = 3

VALID_MOVES = {
  "k": "kivi",
  "p": "paperi",
  "s": "sakset",
}

AI_CHOICES = {
  "easy": "Helppo tekoäly",
  "better": "Parempi tekoäly",
}


def _set_ai(ai_type: str):
    global current_ai_type, tekoaly, tuomari
    if ai_type not in AI_CHOICES:
        ai_type = "easy"
    current_ai_type = ai_type
    tuomari = Tuomari()
    tekoaly = Tekoaly() if ai_type == "easy" else TekoalyParannettu(10)


def _ai_move(player_move: str) -> str:
    # Both AIs support aseta_siirto; for the simple AI it's a no-op.
    tekoaly.aseta_siirto(player_move)
    return tekoaly.anna_siirto()

TEMPLATE = """
<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <title>Kivi-Paperi-Sakset</title>
  <style>
    body { font-family: "Segoe UI", sans-serif; background: #f7f7f7; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: #ffffff; padding: 24px 28px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 380px; }
    h1 { margin: 0 0 12px; font-size: 22px; }
    form { display: flex; gap: 12px; align-items: center; margin: 12px 0 16px; }
    select, button { padding: 10px 12px; border: 1px solid #d0d0d0; border-radius: 8px; font-size: 15px; }
    button { background: #0f766e; color: white; border: none; cursor: pointer; }
    button:hover { background: #0d5f58; }
    .result { margin: 10px 0; font-weight: 600; }
    .score { color: #444; line-height: 1.4; }
    .meta { color: #555; font-size: 14px; }
    .moves { margin: 6px 0; font-size: 14px; }
    .reset { margin-top: 10px; display: inline-block; color: #0f766e; text-decoration: none; font-size: 14px; }
    .disabled { opacity: 0.6; pointer-events: none; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Kivi-Paperi-Sakset</h1>
    <div class="meta">Valitse siirto ja pelaa tekoälyä vastaan.</div>
    <div class="meta">Vastustaja: {{ ai_choices[current_ai_type] }}</div>
    <form method="post" class="{% if game_over %}disabled{% endif %}">
      <label for="ai" class="meta">Valitse tekoäly</label>
      <select id="ai" name="ai">
        {% for key, label in ai_choices.items() %}
          <option value="{{ key }}" {% if key == current_ai_type %}selected{% endif %}>{{ label }}</option>
        {% endfor %}
      </select>
      <label for="siirto" class="meta">Siirto</label>
      <select id="siirto" name="siirto">
        {% for key, label in valid_moves.items() %}
          <option value="{{ key }}" {% if key == user_move %}selected{% endif %}>{{ key }} — {{ label }}</option>
        {% endfor %}
      </select>
      <button type="submit">Pelaa</button>
    </form>

    {% if message %}
      <div class="result">{{ message }}</div>
    {% endif %}

    {% if ai_move and user_move %}
      <div class="moves">Sinä: {{ user_move }} ({{ valid_moves[user_move] }}) &nbsp;|&nbsp; Tekoäly: {{ ai_move }} ({{ valid_moves[ai_move] }})</div>
    {% endif %}

    <div class="score">{{ score_text }}</div>
    <a class="reset" href="{{ url_for('reset') }}">Nollaa pistetilanne</a>
  </div>
</body>
</html>
"""


def _result_message(player_move: str, ai_move: str) -> str:
    if tuomari._tasapeli(player_move, ai_move):
        return "Tasapeli!"
    if tuomari._eka_voittaa(player_move, ai_move):
        return "Voitit!"
    return "Hävisit."


def _game_winner():
    if tuomari.ekan_pisteet >= WIN_THRESHOLD:
        return "Pääsit kolmeen voittoon! Voitit pelin."
    if tuomari.tokan_pisteet >= WIN_THRESHOLD:
        return "Tekoäly saavutti kolme voittoa. Hävisit pelin."
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    ai_move = None
    user_move = None
    selected_ai = current_ai_type
    game_over = _game_winner() is not None

    if request.method == "POST":
        selected_ai = (request.form.get("ai") or current_ai_type).strip().lower()
        if selected_ai != current_ai_type:
            _set_ai(selected_ai)
            game_over = False
            selected_ai = current_ai_type

        if game_over:
            message = _game_winner()
        else:
            user_move = (request.form.get("siirto") or "").strip().lower()
            if user_move not in VALID_MOVES:
                message = "Virheellinen siirto. Käytä k, p tai s."
            else:
                ai_move = _ai_move(user_move)
                tuomari.kirjaa_siirto(user_move, ai_move)
                message = _result_message(user_move, ai_move)
                game_over = _game_winner() is not None
                if game_over:
                    message = _game_winner()

    score_text = str(tuomari)
    return render_template_string(
        TEMPLATE,
        message=message,
        ai_move=ai_move,
        user_move=user_move,
        score_text=score_text,
        valid_moves=VALID_MOVES,
        game_over=game_over,
        ai_choices=AI_CHOICES,
        current_ai_type=selected_ai,
    )


@app.get("/reset")
def reset():
    _set_ai(current_ai_type)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
