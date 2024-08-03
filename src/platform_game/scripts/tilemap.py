class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            # Use string instead of tuple for key bc tuple is not a valid type for later
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
