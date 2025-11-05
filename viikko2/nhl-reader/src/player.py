import requests

BASE_URL = "https://studies.cs.helsinki.fi/nhlstats"

class PlayerReader:
    def __init__(self, season: str):
        self.season = season
        self.players = []
        self._fetch()

    def _fetch(self):
        url = f"{BASE_URL}/{self.season}/players"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        self.players = [Player(d) for d in data]

    def get_players(self):
        return self.players

class Player:
    def __init__(self, player_dict):
        self.name = player_dict.get('name', '')
        self.nationality = player_dict.get('nationality', '')
        self.assists = int(player_dict.get('assists', 0))
        self.goals = int(player_dict.get('goals', 0))
        self.team = player_dict.get('team', '')
        self.games = int(player_dict.get('games', 0))
        self.id_no = player_dict.get('id')
        self.points = self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.points}"

class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality: str):
        players = [p for p in self.reader.get_players() if p.nationality == nationality]
        players.sort(key=lambda p: (p.points, p.goals), reverse=True)
        return players
