import pygame
import sys
from scripts.utils import load_images, Animation
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0
CAM_SPEED = 3  # Higher = Faster


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

        # Initial editor state
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.movement = [False, False, False, False]  # [Left, Right, Up, Down]
        self.cam_pos = [0, 0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.left_click = False
        self.right_click = False
        self.shift = False
        self.ongrid = True
        self.mpos = (0, 0)  # Initialize mouse position

    def update_mouse_position(self):
        """Get mouse screen position and scale it to match display position"""
        mpos = pygame.mouse.get_pos()
        self.mpos = ((int(mpos[0] / RENDER_SCALE), int(mpos[1] / RENDER_SCALE)))

    def handle_events(self):
        """
        Handle input from hardware.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # "X" on Window
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            if event.type == pygame.KEYDOWN:  # Key press
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:  # Key release
                self.handle_key_up(event)

    def quit(self):
        """
        Quit the game and close the window.
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def handle_mouse_down(self, event):
        """Handle mouse button down events."""
        if event.button == 1:  # Left click
            self.left_click = True
            if not self.ongrid:
                self.add_offgrid_tile()

        elif event.button == 3:  # Right click
            self.right_click = True

        elif event.button in {4, 5}:  # Scroll up/down
            self.change_tile_selection(event)

    def handle_mouse_up(self, event):
        """Handle mouse button up events."""
        if event.button == 1:  # Left click
            self.left_click = False
        elif event.button == 3:  # Right click
            self.right_click = False

    def handle_key_down(self, event):
        """Handle key press events."""
        if event.key == pygame.K_a:
            self.movement[0] = True
        elif event.key == pygame.K_d:
            self.movement[1] = True
        elif event.key == pygame.K_w:
            self.movement[2] = True
        elif event.key == pygame.K_s:
            self.movement[3] = True
        elif event.key == pygame.K_g:
            self.ongrid = not self.ongrid
        elif event.key == pygame.K_LSHIFT:
            self.shift = True
        elif event.key == pygame.K_o:
            self.tilemap.save('map.json')
        elif event.key == pygame.K_t:
            self.tilemap.autotile()

    def handle_key_up(self, event):
        """Handle key release events."""
        if event.key == pygame.K_a:
            self.movement[0] = False
        elif event.key == pygame.K_d:
            self.movement[1] = False
        elif event.key == pygame.K_w:
            self.movement[2] = False
        elif event.key == pygame.K_s:
            self.movement[3] = False
        elif event.key == pygame.K_LSHIFT:
            self.shift = False

    def change_tile_selection(self, event):
        """Change the selected tile type or variant based on mouse scroll."""
        if self.shift:
            if event.button == 4:  # Scroll up
                self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
            elif event.button == 5:  # Scroll down
                self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
        else:
            if event.button == 4:
                self.tile_group = (self.tile_group - 1) % len(self.tile_list)
            elif event.button == 5:
                self.tile_group = (self.tile_group + 1) % len(self.tile_list)
            self.tile_variant = 0

    def add_offgrid_tile(self):
        """Add a tile at the current mouse position in off-grid mode."""
        tile_data = {
            "type": self.tile_list[self.tile_group],
            "variant": self.tile_variant,
            "pos": (self.mpos[0] + self.cam_pos[0], self.mpos[1] + self.cam_pos[1]),
        }
        self.tilemap.offgrid_tiles.append(tile_data)
        print(f"Added off-grid tile at: {tile_data['pos']}")
        print(f"Cam pos: {self.cam_pos}")

    def update_camera_pos(self):
        """Update the camera position based on user input."""
        self.cam_pos[0] += (self.movement[1] - self.movement[0]) * CAM_SPEED
        self.cam_pos[1] += (self.movement[3] - self.movement[2]) * CAM_SPEED

    def render_tile(self, curr_tile, tile_pos):
        """Render the current tile at the correct position."""
        # On-grid tiles 
        if self.ongrid:
            self.display.blit(
                curr_tile,
                (
                    tile_pos[0] * self.tilemap.tile_size - self.cam_pos[0],
                    tile_pos[1] * self.tilemap.tile_size - self.cam_pos[1],
                ),
            )
        # Off-grid tiles
        else:
            self.display.blit(curr_tile, self.mpos)

    def place_grid_tile(self, tile_pos):
        """Place a tile on the grid."""
        if self.left_click and self.ongrid:  # Place on grid
            self.tilemap.tilemap[f"{tile_pos[0]};{tile_pos[1]}"] = {
                "type": self.tile_list[self.tile_group],
                "variant": self.tile_variant,
                "pos": tile_pos,
            }

    def delete_tile(self, tile_pos):
        """Delete a tile from the grid or off-grid."""
        if self.right_click:  # Delete
            # Delete on-grid tile
            tile_loc = f"{tile_pos[0]};{tile_pos[1]}"
            if tile_loc in self.tilemap.tilemap:
                del self.tilemap.tilemap[tile_loc]

            # Delete off-grid tile
            for tile in self.tilemap.offgrid_tiles.copy():
                tile_img = self.assets[tile["type"]][tile["variant"]]
                tile_r = pygame.Rect(
                    tile["pos"][0] - self.cam_pos[0],
                    tile["pos"][1] - self.cam_pos[1],
                    tile_img.get_width(),
                    tile_img.get_height(),
                )
                if tile_r.collidepoint(self.mpos):
                    self.tilemap.offgrid_tiles.remove(tile)

    def run(self):
        """
        Main game loop. Handles events, updates game state, and renders the game.
        """
        while self.running:
            # Render BG
            self.display.fill((0, 0, 0))
            self.update_camera_pos()
            render_offset = (int(self.cam_pos[0]), int(self.cam_pos[1]))
            self.tilemap.render(self.display, offset=render_offset)

            # Update mouse position
            self.update_mouse_position()

            # Fetch current tile to be placed
            curr_tile_group = self.assets[self.tile_list[self.tile_group]]
            curr_tile = curr_tile_group[self.tile_variant].copy()
            curr_tile.set_alpha(100)  # Semi-transparent
            self.display.blit(curr_tile, (5, 5))  # Display selected tile in the top-left corner

            # Get the tile's grid coordinates
            tile_pos = (
                int((self.mpos[0] + self.cam_pos[0]) // self.tilemap.tile_size),
                int((self.mpos[1] + self.cam_pos[1]) // self.tilemap.tile_size),
            )

            self.render_tile(curr_tile, tile_pos)
            self.place_grid_tile(tile_pos)
            self.delete_tile(tile_pos)
            self.handle_events()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()