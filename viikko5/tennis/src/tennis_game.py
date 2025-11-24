class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def tie_score(self, score: int) -> str:
        score_names = {0: "Love-All", 1: "Fifteen-All", 2: "Thirty-All"}
        if score <= 2:
            return score_names[score]
        return "Deuce"

    def endgame_score(self, score_difference: int) -> str:
        if score_difference == 1:
            return "Advantage player1"
        if score_difference == -1:
            return "Advantage player2"
        if score_difference >= 2:
            return "Win for player1"
        else:
            return "Win for player2"

    def non_endgame_score_helper(self, player_score: int) -> str:
        score_names = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}
        return score_names[player_score]

    def non_endgame_score(self, player1_score: int, player2_score: int):
        score = ""
        score += self.non_endgame_score_helper(player1_score)
        score += "-"
        score += self.non_endgame_score_helper(player2_score)
        return score


    def get_score(self):
        score = ""

        if self.player1_score == self.player2_score:
            score = self.tie_score(self.player1_score)

        elif self.player1_score >= 4 or self.player2_score >= 4:
            score = self.endgame_score(self.player1_score - self.player2_score)

        else:
            score = self.non_endgame_score(self.player1_score, self.player2_score)

        return score
