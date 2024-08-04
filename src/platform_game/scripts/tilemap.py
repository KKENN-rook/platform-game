import pygame

# Offsets used to calculate neighboring tiles around a given tile position
BORDERING_TILE_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (0, -1),
    (-1, 1),
    (1, -1),
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
]

# Set of tile types that have physics applied (e.g., collision detection)
PHYSICS_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        """
        Initialize the tilemap.

        Args:
            game (Game): Reference to the game object.
            tile_size (int): Size of each tile in pixels.
            tilemap (dict): Grid tiles, key represents location on surf
            offgrid_tiles (list): Non-interactable tiles
        """
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        # Basic tile generation format
        for i in range(10):
            # Keys are strs b/c specific file saving that is incompatible with tuples
            self.tilemap[str(i + 3) + ";10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (i + 3, 10),
            }
            self.tilemap["10;" + str(i + 5)] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, i + 5),
            }

    def _render_tile(self, surface, tile, pos_multiplier=1):
        """
        Helper function to render tile a single tile.
        Args:
            surface(pygame.Surface): The surface to draw the tile on.
            tile(dict): The tile data containing type, variant, and position.
            pos_multiplier(int): Multiplier for the position tile on grid correctly.
        """
        tile_type = tile["type"]
        tile_variant = tile["variant"]
        tile_pos_x = tile["pos"][0] * pos_multiplier
        tile_pos_y = tile["pos"][1] * pos_multiplier
        tile_image = self.game.assets[tile_type][tile_variant]

        surface.blit(tile_image, (tile_pos_x, tile_pos_y))

    def render(self, surface):
        """
        Draws (blits) all tiles onto a surface.
        Args:
            surface(pygame.Surface): The surface to draw the tiles on.
        """
        # Render offgrid tiles in the bg
        for tile in self.offgrid_tiles:
            self._render_tile(surface, tile, pos_multiplier=1)
        # Render grid tiles in the fg
        for tile in self.tilemap.values():
            self._render_tile(surface, tile, pos_multiplier=self.tile_size)

    def border_tiles(self, pos):
        """
        Calculates and returns existing bordering tiles around a given position.
        Args:
            pos(tuple): The position (x, y) to check for bordering tiles.
        Returns:
            list: A list of neighboring tiles.
        """
        # Current position x and y coordinates
        curr_x = int(pos[0] // self.tile_size)
        curr_y = int(pos[1] // self.tile_size)

        # Check the tiles bordering the current position
        b_tiles = []
        for offset in BORDERING_TILE_OFFSETS:
            border_tile = str(curr_x + offset[0]) + ";" + str(curr_y + offset[1])
            if border_tile in self.tilemap:
                b_tiles.append(self.tilemap[border_tile])
        return b_tiles

    def physics_create_rects(self, pos):
        """
        Create Rect objects for tiles with physics enabled around a given position.
        Args:
            pos(tuple): The position (x, y) to check for neighboring tiles with physics.
        Returns:
            list: A list of pygame.Rect objects for collision detection.
        """
        rects = []
        for tile in self.border_tiles(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects
