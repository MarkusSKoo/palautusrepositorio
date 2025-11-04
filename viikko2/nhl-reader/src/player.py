class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.games = dict['games']
        self.id = dict['id']

    def __str__(self):
        return f"Name: {self.name}, nationality: {self.nationality}, assists: {self.assists}, goals: {self.goals}, team: {self.team}, games: {self.games}, id: {self.id}"