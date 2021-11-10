from generateDungeon import createDungeonSnapshot
from PIL import Image
import numpy as np

groundTilePath = "tiles/test-ground.png"
wallTilePath = "tiles/test-wall.png"

def imageFromDungeon(dungeon):
    # Load ground and wall tiles
    wall = Image.open(wallTilePath)
    ground = Image.open(groundTilePath)
    # Each tile is 32x32
    image = Image.new("RGB", (32 * dungeon.shape[0], 32 * dungeon.shape[1]))
    # TODO: Iterate over the tiles in the dungeon, paste images
    for x, y in np.ndindex(dungeon.shape):
        tile = wall if dungeon[x, y] == 0 else ground
        image.paste(tile, (32 * x, 32 * y))
    # Show the generated image
    image.show()

# Testing:
dungeon = createDungeonSnapshot([10, 8])
imageFromDungeon(dungeon)