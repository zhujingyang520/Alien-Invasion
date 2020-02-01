"""
Module maintains the bullet.
Note: Sprite in Pygame is handy to maintain a group of related objects. A group is like a list with extra functionality
like collision detection for building games. It can facilitate to perform the same operation on all grouped elements.
"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullet fired from the spaceship."""

    def __init__(self, ai_game, *groups):
        """
        Create a bullet object at the ship's current position.
        :param ai_game: Reference to the current instance of `AlienInvasion` class.
        """
        super().__init__(*groups)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # Make bullet emerges from the top of ship

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self, *args):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed  # Decrease y coordination to move the bullet up
        self.rect.y = self.y  # Update the rect position for further surface rendering

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
