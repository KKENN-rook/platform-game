import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        """
        Initialize the game, set up the window, load assets, and create game objects.
        """
        # Pygame window setup
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))  # Window
        self.clock = pygame.time.Clock()
        self.running = True
        self.display = pygame.Surface((320, 240))  # Display to be upscaled

        # Load game assets
        self.assets = {
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
        }

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))  # player is 8x15
        self.tilemap = Tilemap(self, tile_size=16)

        self.movement = [False, False]  # [Left, Right]

    def run(self):
        """
        Main game loop. Handles events, updates game state, and renders the game.
        """
        while self.running:

            # Renders / Position updates
            self.display.fill((14, 219, 248))  # Sky-color background
            self.tilemap.render(self.display)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            # Event handling
            for event in pygame.event.get():
                # Exit window
                if event.type == pygame.QUIT:
                    self.quit()
                # Key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                # Key release
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # Upscale the display and render it on the screen
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )

            # Update the screen
            pygame.display.update()
            self.clock.tick(60)  # 60 FPS

    def quit(self):
        """
        Quit the game and close the window.
        """
        self.running = False
        pygame.quit()
        sys.exit()


Game().run()
