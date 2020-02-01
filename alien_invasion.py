"""Main routine for alien invasion game."""

import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # Initialize background settings that Pygame needs to work properly
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Full screen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)  # Create an instance to record the game statistics

        self.score_board = Scoreboard(self)  # Create an instance of scoreboard

        self.play_button = Button(self, "Play")  # Create an instance of start button

        self.ship = Ship(self)  # Create an instance of spaceship

        self.bullets = pygame.sprite.Group()  # A group of bullets that have been fired by spaceship

        self.aliens = pygame.sprite.Group()  # A group of aliens that generated by computer
        self._create_fleet()  # Initialize the fleet of aliens

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # Pooling over key and mouse events
            if self.stats.game_active:
                self.ship.update()  # Update ship position
                self._update_bullets()  # Update bullets position
                self._update_aliens()  # Update aliens position
            self._update_screen()  # Update screen display

    def _check_events(self):
        """Helper to respond to the key-presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Get a tuple of mouse position when pressed down
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Helper to respond to key-press events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # Start moving ship to the right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True  # Start moving ship to the left
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()  # Exit games using keypress `Q` or `ESC`
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:  # We can also start game by pressing `p`
            self._start_game()

    def _check_keyup_event(self, event):
        """Helper to respond to key-release events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # Stop moving ship to the right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False  # Stop moving ship to the left

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # Returns True when a point is inside the rect
        if button_clicked and not self.stats.game_active:  # Make sure the click event is valid when game is inactive
            self._start_game()

    def _start_game(self):
        """Helper to start the game by reset game statistics and re-initializes all aliens and ships."""
        self.stats.game_active = True

        # Reset the game statistics and re-initialize all aliens and ship for new game round
        self.stats.reset_stats()
        self.aliens.empty()
        self.bullets.empty()
        self.ship.center_ship()
        self._create_fleet()
        # Reset the game settings to restore the initial game level
        self.settings.initialize_dynamic_settings()
        # Update the scoreboard after reset score statistics
        self.score_board.prep_score()
        self.score_board.prep_level()
        self.score_board.prep_ships_left()

        # Hide the mouse cursor after game starts
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Helper to create a new bullet and add it to the bullets group."""
        if self.stats.game_active and len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Helper to update position of bullets and get rid of bullets shoot out-of-screen."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have been disappeared (off screen)
        for bullet in self.bullets.copy():  # Use copy to avoid modifying `bullets` when iteration
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Handle bullet-alien collision
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens
        # If so, remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:  # Increment scores for bullets hit aliens
            for hit_aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(hit_aliens)
            self.score_board.prep_score()  # Update rendered image of the score
            self.score_board.check_high_score()  # Update the highest score if possible

        if not self.aliens:
            # Destroy existing bullets and create new fleet if we shoot all aliens in a fleet
            self.bullets.empty()
            self._create_fleet()
            # Level-up the difficulty of games
            self.settings.increase_speed()
            # Update the level info on the scoreboard
            self.stats.level += 1
            self.score_board.prep_level()

    def _update_aliens(self):
        """Helper to update the position of all aliens in the fleet."""
        self._check_fleet_hit_edges()  # Update the moving direction if any alien hits either edge
        self.aliens.update()  # Update the position of aliens in the fleet

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_hit_bottom()

    def _update_screen(self):
        """Helper to update images on the screen and flip to new screen."""
        self.screen.fill(self.settings.bg_color)  # Draw screen background color

        self.ship.blitme()  # Draw spaceship to screen

        for bullet in self.bullets.sprites():  # `sprites` returns a list of all sprites in group for iteration
            bullet.draw_bullet()

        self.aliens.draw(self.screen)  # Draw the group of aliens

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        self.score_board.show_score()  # Draw the score board

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _create_fleet(self):
        """Helper to create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row and in a column
        # Space between each alien is equal to one alien width and height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width  # Margin of an alien at left & right edges
        num_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens can fit on the screen
        ship_height = self.ship.rect.height
        # We leave 2 aliens empty space above spaceship so the player has some time to shoot aliens
        available_space_y = self.settings.screen_height - ship_height - 3 * alien_height
        num_aliens_y = available_space_y // (2 * alien_height)

        for alien_idx_y in range(num_aliens_y):  # Iterate over rows of aliens
            for alien_idx_x in range(num_aliens_x):  # Iterate over cols of aliens on the row `alien_idx_y`
                self._create_alien(alien_idx_x, alien_idx_y)

    def _create_alien(self, alien_idx_x, alien_idx_y):
        """Helper to create an alien and place it in the row with the specified index in X and Y coordination."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_idx_x * 2 * alien_width  # Offset of one alien with stride of one alien
        alien.rect.x = alien.x
        alien.rect.y = alien_height + alien_idx_y * 2 * alien_height
        self.aliens.add(alien)

    def _check_fleet_hit_edges(self):
        """Helper to check if any aliens have hit an edge."""
        for alien in self.aliens.sprites():
            if alien.hit_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change the fleet's direction and drop the entire fleet."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1  # Multiply -1 to flip the left to right direction, and vice versa

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ship_left in statistics
            self.stats.ship_left -= 1
            self.score_board.prep_ships_left()
            # Get rid of any remaining aliens and bullets in the group
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet of aliens and re-center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Sleep for 0.5s so that player notices the collision and regroup before new fleet appears
            sleep(0.5)
        else:
            self.stats.game_active = False  # We don't have any spaceship left and game over :-(
            pygame.mouse.set_visible(True)  # Show the mouse cursor after game overs

    def _check_aliens_hit_bottom(self):
        """Check if any alien in the group have reached the bottom edge of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if ship got hit
                self._ship_hit()
                break


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()