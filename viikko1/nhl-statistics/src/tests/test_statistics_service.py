import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_existing_player(self):
        self.assertEqual(self.stats.search("Semenko").name, "Semenko")

    def test_search_nonexisting_player(self):
        self.assertEqual(self.stats.search("Nonexistent"), None)

    def test_search_team(self):
        self.assertEqual(len(self.stats.team("EDM")), 3)

    def test_search_top(self):
        self.assertEqual(len(self.stats.top(4)), 5)
