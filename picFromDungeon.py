import math
import random
from generateDungeon import Dungeon
from PIL import Image
import numpy as np

groundTilePath = "tiles/test-ground.png"
wallTilePath = "tiles/test-innerwall.png"
LwallTilePath = "tiles/test-Lwall.png"
RwallTilePath = "tiles/test-Rwall.png"
BLwallTilePath = "tiles/test-BLwall.png"
BRwallTilePath = "tiles/test-BRwall.png"
TLwallTilePath = "tiles/test-TLwall.png"
TRwallTilePath = "tiles/test-TRwall.png"
TwallTilePath = "tiles/test-Twall.png"
BwallTilePath = "tiles/test-Bwall.png"
TLcornerWallTilePath = "tiles/test-TLcornerWall.png"
TRcornerWallTilePath = "tiles/test-TRcornerWall.png"
BLcornerWallTilePath = "tiles/test-BLcornerWall.png"
BRcornerWallTilePath = "tiles/test-BRcornerWall.png"

testTileset = "tiles/test.png"


tile_path_from_value = {
    0: wallTilePath,
    1: groundTilePath,
    2: TwallTilePath,
    3: RwallTilePath,
    4: BwallTilePath,
    5: LwallTilePath,
    6: TLwallTilePath,
    7: TRwallTilePath,
    8: BLwallTilePath,
    9: BRwallTilePath,
    10: TLcornerWallTilePath,
    11: TRcornerWallTilePath,
    12: BLcornerWallTilePath,
    13: BRcornerWallTilePath,
    14: groundTilePath,
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
    # TODO: Iterate over the tiles in the dungeon, paste images
    for x, y in np.ndindex(dungeon.shape):
        if dungeon[x, y] != 1:
            tile = Image.open(tile_path_from_value[dungeon[x, y]])
            image.paste(tile, (32 * x, 32 * y))
    # Show the generated image
    image.show()

# Testing:
dungeon = Dungeon([15, 8])
image_from_dungeon(dungeon, testTileset)