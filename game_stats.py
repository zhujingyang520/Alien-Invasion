"""Module maintains the game statistics of alien invasion."""


class GameStats:
    """Track statistics for Alien Invasion."""

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
        self.highest_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1  # Game level
