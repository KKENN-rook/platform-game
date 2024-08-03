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


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}  # Grid Tiles
        self.offgrid_tiles = []  # Non-interactable tiles

        for i in range(10):
            # Use string for key for easier comparisons later
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
        tile_type = tile["type"]
        tile_variant = tile["variant"]
        tile_pos_x = tile["pos"][0] * pos_multiplier
        tile_pos_y = tile["pos"][1] * pos_multiplier

        tile_image = self.game.assets[tile_type][tile_variant]
        surface.blit(tile_image, (tile_pos_x, tile_pos_y))

    def render(self, surface):
        # Render offgrid tiles in the bg
        for tile in self.offgrid_tiles:
            self._render_tile(surface, tile, pos_multiplier=1)

        # Render grid tiles in the fg, pos_multiplier as the the tile must sit on grid
        for tile in self.tilemap.values():
            self._render_tile(surface, tile, pos_multiplier=self.tile_size)

    def border_tiles(self, pos):
        """Calculates and returns existing bordering tiles around current position"""

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
