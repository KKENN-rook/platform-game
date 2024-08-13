import pygame
import json
import copy

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

# If neighbors exist at position(key) use variant(value)
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,  # If tile exists on the R and below, use variant 0
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
# Variants to support autotiling
AUTOTILE_TYPES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        """
        Initialize the tilemap.

        Args:
            game (Game): Reference to the game object.
            tile_size (int): Size of each tile in pixels.
        """
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}  # Grid tiles; keys represent location in world
        self.offgrid_tiles = []  # Non-interactable tiles

        # Basic tile generation format
        for i in range(10):
            # Keys are strs b/c JSON does not support tuples
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

    def extract(self, id_pairs, keep=False):
        """
        Extracts tiles that match the given (type, variant) pairs from both 
        off-grid tiles and the grid-based tilemap.
        Args:
            id_pairs (set of tuples): A set of (type, variant) pairs to match tiles against.
            keep (bool): If False, removes matched tiles from the map. Defaults to False.
        Returns:
            matches (list): A list of matched tile dictionaries, with their positions adjusted for off-grid tiles.
        """
        matches = []
        # Iterate over off-grid tiles
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        
        # Iterate over the grid-based tilemap
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                copied_tile = copy.deepcopy(tile)
                # Convert grid coordinates to pixel coords
                copied_tile['pos'][0] *= self.tile_size
                copied_tile['pos'][1] *= self.tile_size
                matches.append(copied_tile)
                if not keep:
                    del self.tilemap[loc]

        return matches
    
    def render(self, surf, offset=(0, 0)):
        """
        Draws (blits) all tiles onto a surface.
        Args:
            surf (pygame.Surface): The surface to draw the tiles on.
            offset (tuple): Coordinates to offset for center camera.
        """
        # Render off-grid tiles
        for tile in self.offgrid_tiles:
            self._draw_tile(surf, tile, offset, grid_aligned=False)

        # Determine the portion of the tile grid that is visible on the screen
        start_x = offset[0] // self.tile_size
        end_x = (offset[0] + surf.get_width()) // self.tile_size + 1  # +1 to full render end tiles.
        start_y = offset[1] // self.tile_size
        end_y = (offset[1] + surf.get_height()) // self.tile_size + 1

        # If a tile is located within the screen, render it
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_coords = f"{x};{y}"
                if tile_coords in self.tilemap:
                    tile = self.tilemap[tile_coords]
                    self._draw_tile(surf, tile, offset, grid_aligned=True)

    def _draw_tile(self, surf, tile, offset, grid_aligned):
        """
        Blit a tile onto the surface with the given offset.
        Args:
            surf (pygame.Surface): The surface to draw the tile on.
            tile (dict): The tile data.
            offset (tuple): Coordinates to offset for center camera.
            grid_aligned (bool): Whether the tile is grid-aligned or off-grid.
        """
        tile_type = tile["type"]
        tile_variant = tile["variant"]

        if grid_aligned:
            tile_pos_x = tile["pos"][0] * self.tile_size
            tile_pos_y = tile["pos"][1] * self.tile_size
        else:
            tile_pos_x = tile["pos"][0]
            tile_pos_y = tile["pos"][1]

        tile_image = self.game.assets[tile_type][tile_variant]
        surf.blit(tile_image, (tile_pos_x - offset[0], tile_pos_y - offset[1]))

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

    def autotile(self):
        """
        Automatically adjust tiles to its proper variant based on their neighboring tiles.
        """
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()

            # Check neighboring tiles in the four cardinal directions
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = f"{tile['pos'][0] + shift[0]};{tile['pos'][1] + shift[1]}"

                # If a neighboring tile exists and is of the same type, add its direction to neighbors
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)

            # Convert neighbors to a sorted tuple to create a consistent key
            neighbors = tuple(sorted(neighbors))

            # If the tile type supports autotiling and the neighbors pattern is in the map,
            # update the tile's variant to match the appropriate variant from the autotile map.
            if tile["type"] in AUTOTILE_TYPES and neighbors in AUTOTILE_MAP:
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def save(self, path):
        """Save a tilemap to a json file."""
        file = open(path, "w")
        json.dump({"tilemap": self.tilemap, "tile_size": self.tile_size, "offgrid": self.offgrid_tiles}, file)
        file.close()

    def load(self, path):
        """Load a tilemap from a json file."""
        file = open(path, "r")
        map_data = json.load(file)
        file.close()

        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]
