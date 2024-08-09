import pygame
import sys
from scripts.utils import load_images, Animation
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0


class Editor:
    def __init__(self):
        """
        Initialize the game, set up the window, load assets, and create game objects.
        """
        # Pygame window setup
        pygame.init()
        pygame.display.set_caption("Level Editor")
        self.screen = pygame.display.set_mode((640, 480))  # Game window
        self.clock = pygame.time.Clock()
        self.running = True
        self.display = pygame.Surface((320, 240))  # Display to be upscaled
        # Load game assets
        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
        }
        self.tilemap = Tilemap(self, tile_size=16)
        self.movement = [False, False, False, False]  # [Left, Right, Up, Down]
        self.cam_pos = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.left_click = False
        self.right_click = False
        self.shift = False
        self.ongrid = True

    def handle_events(self, mouse_pos):
        """
        Handle input from hardware.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # "X" on Window
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                    if not self.ongrid:
                        self.tilemap.offgrid_tiles.append(
                            {
                                "type": self.tile_list[self.tile_group],
                                "variant": self.tile_variant,
                                "pos": (mouse_pos[0] + self.cam_pos[0], mouse_pos[1] + self.cam_pos[1]),
                            }
                        )
                        print(
                            f"Added off-grid tile at: {(mouse_pos[0] + self.cam_pos[0], mouse_pos[1] + self.cam_pos[1])}"
                        )
                if event.button == 3:
                    self.right_click = True
                if self.shift:
                    if event.button == 4:  # Scroll up
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.button == 5:  # Scroll down
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                else:
                    if event.button == 4:  # Scroll up
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.button == 5:  # Scroll down
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_click = False
                if event.button == 3:
                    self.right_click = False
            if event.type == pygame.KEYDOWN:  # Key press
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_w:
                    self.movement[2] = True
                if event.key == pygame.K_s:
                    self.movement[3] = True
                if event.key == pygame.K_g:
                    self.ongrid = not self.ongrid
                if event.key == pygame.K_LSHIFT:
                    self.shift = True
            if event.type == pygame.KEYUP:  # Key release
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False
                if event.key == pygame.K_w:
                    self.movement[2] = False
                if event.key == pygame.K_s:
                    self.movement[3] = False
                if event.key == pygame.K_LSHIFT:
                    self.shift = False

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
            self.display.fill((0, 0, 0))

            self.cam_pos[0] += (self.movement[1] - self.movement[0]) * 2
            self.cam_pos[1] += (self.movement[3] - self.movement[2]) * 2

            render_offset = (int(self.cam_pos[0]), int(self.cam_pos[1]))
            self.tilemap.render(self.display, offset=render_offset)

            curr_tile_group = self.assets[self.tile_list[self.tile_group]]
            curr_tile = curr_tile_group[self.tile_variant].copy()
            curr_tile.set_alpha(100)  # Semi-transparent

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + self.cam_pos[0]) // self.tilemap.tile_size),
                int((mpos[1] + self.cam_pos[1]) // self.tilemap.tile_size),
            )

            if self.ongrid:
                self.display.blit(
                    curr_tile,
                    (
                        tile_pos[0] * self.tilemap.tile_size - self.cam_pos[0],
                        tile_pos[1] * self.tilemap.tile_size - self.cam_pos[1],
                    ),
                )
            else:
                self.display.blit(curr_tile, (mpos[0], mpos[1]))

            if self.left_click and self.ongrid:  # Place tile
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }
            if self.right_click:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(
                        tile["pos"][0] - self.cam_pos[0],
                        tile["pos"][1] - self.cam_pos[1],
                        tile_img.get_width(),
                        tile_img.get_height(),
                    )
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(curr_tile, (5, 5))

            # Handle input
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            self.handle_events(mouse_pos=mpos)

            # Upscale the display and render it on the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Display the screen
            pygame.display.update()

            # 60 FPS
            self.clock.tick(60)


Editor().run()
