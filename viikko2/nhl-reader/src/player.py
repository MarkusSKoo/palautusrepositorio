import requests

class PlayerReader:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url).json()
        self.players = []

        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)

    def get_players(self):
        return self.players

class Player:
    def __init__(self, player_dict):
        self.player_dict = player_dict
        self.name = self.player_dict['name']
        self.nationality = self.player_dict['nationality']
        self.assists = self.player_dict['assists']
        self.goals = self.player_dict['goals']
        self.team = self.player_dict['team']
        self.games = self.player_dict['games']
        self.id_no = self.player_dict['id']
        self.points = self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.points}"

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = []

        for player in self.reader.get_players():
            if player.nationality == nationality:
                players.append(player)

        players.sort(key=lambda p: p.points, reverse=True)
        return players
