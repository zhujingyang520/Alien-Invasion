"""Module maintains the button for Alien Invasion."""

import pygame


class Button:
    """Press button for game."""

    def __init__(self, ai_game, msg):
        """
        Initialize button attributes.
        :param ai_game: Reference to the current instance of `AlienInvasion` class.
        :param msg: String of message to be shown on the button.
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimension and property of the button and its text
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # (R,G,B)
        self.text_color = (255, 255, 255)  # (R,G,B)
        self.text_font = pygame.font.Font(None, 48)  # Use system default font and font size = 48

        # Build the button's rect object and center it to the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Initialize at (0, 0) with width x height
        self.rect.center = self.screen_rect.center

        # Prepare the surface of button text
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn specified message into a rendered image and center text on the button."""
        self.msg_image = self.text_font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
