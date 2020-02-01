"""Module maintains the spaceship."""

import pygame
from pygame.sprite import Sprite  # Facilitate to maintain a list of ships


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game, *groups):
        """
        Initialize the ship and set its start location.
        :param ai_game: Reference to the current instance of `AlienInvasion` class.
        """
        super().__init__(*groups)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()  # Get the associated rectangle of screen

        # Load the ship image and get its associated rectangle
        self.image = pygame.image.load("images/ship.bmp")  # Returns a surface representing the ship
        self.rect = self.image.get_rect()

        # Place the spaceship to the middle bottom of screen
        self.x = 0  # Floating value to record the horizontal position of spaceship
        self.center_ship()

        # Movement flag
        self.moving_right = False  # Moving right flag
        self.moving_left = False  # Moving left flag

    def update(self, *args):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect directly
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # Update `rect.x` from `self.x`
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the spaceship on the screen."""
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a float value of the ship's horizontal position because `rect.x` is an integer
        self.x = float(self.rect.x)
