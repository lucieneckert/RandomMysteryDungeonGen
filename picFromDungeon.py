from generateDungeon import createDungeonSnapshot, addWallResolution
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



getTileFromValue = {
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
    10: groundTilePath,
}

def imageFromDungeon(dungeon):
    # Load ground and wall tiles
    wall = Image.open(wallTilePath)
    ground = Image.open(groundTilePath)
    # Each tile is 32x32
    image = Image.new("RGB", (32 * dungeon.shape[0], 32 * dungeon.shape[1]))
    # TODO: Iterate over the tiles in the dungeon, paste images
    for x, y in np.ndindex(dungeon.shape):
        tile = Image.open(getTileFromValue[dungeon[x, y]])
        image.paste(tile, (32 * x, 32 * y))
    # Show the generated image
    image.show()

# Testing:
dungeon = addWallResolution(createDungeonSnapshot([10, 8]))
imageFromDungeon(dungeon)