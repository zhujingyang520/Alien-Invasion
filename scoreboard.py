"""Module maintains the scoreboard for Alien Invasion."""

import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize score-keeping attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ai_game = ai_game

        # Font settings for scoring info
        self.text_color = (30, 30, 30)  # (R,G,B)
        self.text_font = pygame.font.SysFont(None, 48)  # Default system font and font size = 48

        # Prepare the initial score and highest score images
        self.score_image, self.score_rect = None, None  # Placeholder
        self.prep_score()
        self.highest_score_image, self.highest_score_rect = None, None  # Placeholder
        self.prep_highest_score()
        # Prepare the level info
        self.level_image, self.level_rect = None, None  # Placeholder
        self.prep_level()
        # Prepare the number of ships left info
        self.ships = None  # Placeholder
        self.prep_ships_left()

    def prep_score(self):
        """Turn the score into the rendered image."""
        rounded_score = round(self.stats.score, -1)  # `-1` means to round to the nearest 10, 100, 1000, and so on
        score_str = f"Score: {rounded_score:,g}"  # Add comma separator for general number display
        self.score_image = self.text_font.render(score_str, True, self.text_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # Leave 20 margins at the right edge
        self.score_rect.top = 20  # Leave 20 margins at the top edge

    def prep_highest_score(self):
        """Turn the highest score into the rendered image."""
        highest_score = round(self.stats.highest_score, -1)
        highest_score_str = f"Highest Score: {highest_score:,g}"
        self.highest_score_image = self.text_font.render(highest_score_str, True, self.text_color)

        # Create the highest score at the top of the screen
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the game level into the rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.text_font.render(level_str, True, self.text_color)
        # Position the level below the current score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  # 10 pixels below current score

    def prep_ships_left(self):
        """Show how many ships are left."""
        self.ships = Group()
        for i in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship.rect.width * i  # 10 pixel margins to the top left corner of the screen
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there is new high score."""
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.prep_highest_score()
