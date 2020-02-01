"""Basic settings of alien invasion game."""


class Settings:
    """A class to store all settings for Alien Invasion."""

    # Handy alias for left and right directions
    LEFT = -1  # Moving left involves subtracting from x coordination
    RIGHT = 1  # Moving right involves adding to x coordination

    def __init__(self):
        """Initialize game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # (R,G,B)

        # Ship settings
        self.ship_speed = None  # Placeholder for dynamic settings
        self.ship_limit = 3  # Number of spaceships for the player

        # Bullet settings
        self.bullet_speed = None  # Placeholder for dynamic settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # (R,G,B)
        self.bullet_allowed = 3  # Max number of allowed bullets to be used by spaceship

        # Alien settings
        self.alien_speed = None  # Placeholder for dynamic settings
        self.fleet_drop_speed = 10  # How quickly the fleet drops down the screen when an alien hits either edge
        self.fleet_direction = None  # Placeholder for dynamic settings
        self.alien_points = None  # Placeholder for dynamic settings

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien points increase
        self.score_point_scale = 1.5

        self.initialize_dynamic_settings()

    def increase_speed(self):
        """Increase the speed settings to increase the game difficulty."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_point_scale)  # Make sure alien point is integer

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5  # Initial speed of spaceship: shift 1.5 pixel per LEFT/RIGHT press
        self.bullet_speed = 1  # Initial speed of bullet move up screen
        self.alien_speed = 1  # Initial speed of aliens of move left and right
        self.fleet_direction = Settings.RIGHT  # Initial moving direction of fleet of aliens
        self.alien_points = 50  # Initial points for each alien
