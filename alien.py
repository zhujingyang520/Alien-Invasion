"""Module maintains the alien."""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, *groups):
        """Initialize the alien and set its starting position."""
        super().__init__(*groups)
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and get its associated rectangle
        self.image = pygame.image.load("images/alien.bmp")  # Returns a surface representing the alien
        self.rect = self.image.get_rect()

        # Initialize new alien near the top left of the screen
        # It will later be overwritten by `_create_alien` in `alien_invasion`
        self.rect.x = self.rect.width  # Leave offset of (width x height) for easy observation
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self, *args):
        """Move the alien left or right based on the fleet direction."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction  # Move alien left or right
        self.rect.x = self.x  # Update the rect position for further surface rendering

    def hit_edges(self):
        """Return True if alien hits the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True
        else:
            return False
