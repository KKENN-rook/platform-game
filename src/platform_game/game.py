import pygame
import sys
import random
import math
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle


class Game:
    def __init__(self):
        """
        Initialize the game, set up the window, load assets, and create game objects.
        """
        # Pygame window setup
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.screen = pygame.display.set_mode((640, 480))  # Game window
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
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("entities/player/idle"), img_dur=6),
            "player/run": Animation(load_images("entities/player/run"), img_dur=4),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/slide": Animation(load_images("entities/player/slide")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
            "particle/leaf": Animation(load_images("particles/leaf"), img_dur=20, loop=False),
        }
        # Game Environment
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")
        self.clouds = Clouds(self.assets["clouds"], count=16)
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13))
        self.particles = []
        # Player initialization
        self.player = Player(self, (50, 50), (8, 15))
        self.movement = [False, False]  # [Left, Right]
        # Essentially tracks the game world coordinates, top-left corner of screen is cam pos [x, y].
        self.cam_pos = [0, 0]

    def generate_leaf_particles(self):
        """Generate leaf particles from spawners. Chance based, larger the object higher chance."""
        for rect in self.leaf_spawners:
            if random.random() * 50000 < rect.width * rect.height:
                pos = (rect.x + (random.random() * rect.width), rect.y + (random.random() * rect.height))
                self.particles.append(Particle(self, "leaf", pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

    def update_particles(self, render_offset):
        """Update and render particles."""
        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_offset)
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

    def update_cam(self):
        """
        Calc target camera position needed to center player and update its position.
        """
        # Calculate the target camera position
        target_cam_x = self.player.rect().centerx - self.display.get_width() / 2
        target_cam_y = self.player.rect().centery - self.display.get_height() / 2
        # Update the camera pos to target pos
        cam_speed = 30  # value = how many frames it takes to reach destination
        self.cam_pos[0] += (target_cam_x - self.cam_pos[0]) / cam_speed
        self.cam_pos[1] += (target_cam_y - self.cam_pos[1]) / cam_speed

    def handle_events(self):
        """
        Handle input from hardware.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # "X" on Window
                self.quit()
            if event.type == pygame.KEYDOWN:  # Key press
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.velocity[1] = -3
            if event.type == pygame.KEYUP:  # Key release
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

    def quit(self):
        """
        Quit the game and close the window.
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def run(self):
        """
        Main game loop. Handles events, updates game state, and renders the game.
        """
        while self.running:

            # Render BG
            self.display.blit(self.assets["background"], (0, 0))

            # Update cam pos
            self.update_cam()

            # If player position and camera position are both floats, could cause jitter
            render_offset = (int(self.cam_pos[0]), int(self.cam_pos[1]))

            # Particle generation
            self.generate_leaf_particles()

            # Render entities onto the display
            self.clouds.update()
            self.clouds.render(self.display, offset=render_offset)
            self.tilemap.render(self.display, offset=render_offset)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_offset)
            self.update_particles(render_offset)

            # Handle input
            self.handle_events()

            # Upscale the display and render it on the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Display the screen
            pygame.display.update()

            # 60 FPS
            self.clock.tick(60)


Game().run()
