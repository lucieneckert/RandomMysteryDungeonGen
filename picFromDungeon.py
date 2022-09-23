import math
import random
from generateDungeon import Dungeon
from PIL import Image
import numpy as np

testTileset = "tiles/test.png"


tile_crop_from_value : dict[int, tuple[int, int, int, int]] = {
    0: (5 * 32, 0, 6 * 32, 32),
    2: (384, 0, 416, 32),
    3: (7 * 32, 0, 8 * 32, 32),
    4: (128, 0, 160, 32),
    5: (6 * 32, 0, 7 * 32, 32),
    6: (9 * 32, 0, 10 * 32, 32),
    7: (11 * 32, 0, 12 * 32, 32),
    8: (32, 0, 64, 32),
    9: (3 * 32, 0, 4 * 32, 32),
    10: (8 * 32, 0, 9 * 32, 32),
    11: (10 * 32, 0, 11 * 32, 32),
    12: (0, 0, 32, 32),
    13: (2 * 32, 0, 3 * 32, 32),
    14: (0, 32, 32, 64),
}

def get_random_ground(tileset):
    random_inc = math.floor(random.random() * 3)
    return tileset.crop((32 * random_inc, 32, 32 * (random_inc + 1), 64))

def image_from_dungeon(dungeon, tileset):
    # open tileset
    tileset = Image.open(tileset)
    # Access the dungeon's array
    dungeon = dungeon.as_tileset_array()
    # Each tile is 32x32
    image = Image.new("RGB", (32 * dungeon.shape[0], 32 * dungeon.shape[1]))
    # Paste floors on the ground
    for x, y in np.ndindex(dungeon.shape):
        image.paste(get_random_ground(tileset), (32 * x, 32 * y))
    # Iterate over the tiles in the dungeon, paste images
    for x, y in np.ndindex(dungeon.shape):
        if dungeon[x, y] != 1:
            tile = tileset.crop(
                tile_crop_from_value[dungeon[x, y]]
            )
            image.paste(tile, (32 * x, 32 * y))
    # Show the generated image
    image.show()

# Testing:
dungeon = Dungeon([15, 15])
image_from_dungeon(dungeon, testTileset)