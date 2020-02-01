"""Module maintains the game statistics of alien invasion."""

import json


class GameStats:
    """Track statistics for Alien Invasion."""

    HIGH_SCORE_FILE_NAME = "high_score.json"  # JSON file to record the highest score

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.ship_left = None  # Placeholder to let `ship_left` is defined in `__init__` explicitly
        self.score = None  # Placeholder
        self.level = None  # Placeholder
        self.reset_stats()
        # Start Alien Invasion in an inactive status. Start game after pressing start button.
        self.game_active = False
        # Highest score for game playing
        self.highest_score = None  # Placeholder
        self.load_highest_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1  # Game level

    def store_highest_score(self):
        """Store the highest score to the JSON file."""
        with open(GameStats.HIGH_SCORE_FILE_NAME, "w") as fp:
            json.dump(self.highest_score, fp)

    def load_highest_score(self):
        """Load the highest score from the JSON file."""
        try:
            with open(GameStats.HIGH_SCORE_FILE_NAME, "r") as fp:
                self.highest_score = json.load(fp)
        except FileNotFoundError:
            self.highest_score = 0
