'''
    Generates dungeons like this:
    0 0 0 0 0 0 0 0 
    1 1 1 1 1 1 0 0
    0 0 1 1 1 1 0 0
    0 0 1 1 1 1 1 1 
    0 0 0 0 0 0 0 0
    Where:
    1 = floor tile
    0 = wall tile
'''
import numpy as np
from enum import Enum
import random

class BigRooms(Enum):
    BigRect = 0
    TwoSmall = 1

'''
    createDungeonSnapshot((x, y)) creates a dungeon of size x and y
    based on a predefined generation algorithm.
    Precondition: x and y both greater than 3.
    Returns a 2d numpy array of shape (x, y).
'''
def createDungeonSnapshot(shape):
    # Initialize as all walls
    dungeon = np.zeros(shape)
    # Place one "main" room
    roomType = BigRooms.BigRect
    mainRoom = generateRoom(roomType, shape)
    # Make sure it's placed legally
    xPos = random.randrange(0, shape[0] - mainRoom.shape[0])
    yPos = random.randrange(0, shape[1] - mainRoom.shape[1])
    # Add some padding
    mainRoom = np.pad(mainRoom, [(0, random.randint(0, shape[0] - mainRoom.shape[0])), 
                                 (0, random.randint(0, shape[1] - mainRoom.shape[1]))])
    mainRoom = np.pad(np.flip(mainRoom), [(0, shape[0] - mainRoom.shape[0]), 
                                          (0, shape[1] - mainRoom.shape[1])])
    # Now, the room array and dungeon array should be the same size
    # So, we can add the room by just adding the arrays
    dungeon += mainRoom
    # Generate 2-4 halls out
    for _ in range(random.randint(2, 4)):
        # Find a point to "tunnel" out of
        point = [random.randrange(0, shape[0]), random.randrange(0, shape[1])]
        # Make sure it's a floor
        while dungeon[point[0], point[1]] != 1:
            point = [random.randrange(0, shape[0]), random.randrange(0, shape[1])]
        # Choose a direction for the tunnel
        dir = random.randint(0, 3) # 0 = up, go clockwise
        # TODO: Get python 3.10 already stubborn asshole
        if dir == 0:
            while (point[1] > 0):
                dungeon[point[0], point[1]] = 1
                point[1] -= 1
        elif dir == 1:
            while (point[0] < shape[0]):
                dungeon[point[0], point[1]] = 1
                point[0] += 1
        elif dir == 2:
            while (point[1] < shape[1]):
                dungeon[point[0], point[1]] = 1
                point[1] += 1
        elif dir == 3:
            while (point[0] > 0):
                dungeon[point[0], point[1]] = 1
                point[0] -= 1
    print(dungeon)
    return dungeon  

'''
    addWallResolution(dungeon) takes a SIMPLE dungeon
    (where 1 = floor, 0 = wall) and returns a dungeon with higher-
    resolution walls (corners, etc.)
    Returns a 2d numpy array of shape dungeon.shape
'''
def addWallResolution(dungeon):
    output = np.copy(dungeon)
    (width, height) = dungeon.shape
    for x, y in np.ndindex(dungeon.shape):
        tile = dungeon[x, y]
        '''
            Key (idx -> meaning):
            0: inner wall
            1: floor
            2: wall above adjacent floor 
            3: wall right of adjacent floor
            4: wall below adjacent floor
            5: wall left of adjacent floor
            6: TL corner wall
            7: TR corner wall
            8: BL corner wall
            9: BR corner wall
        '''
        tileValues = [1] * 11
        if tile < 1:
            # Use neighbors to remove illegal value possibilities
            if y + 1 < height and dungeon[x, y + 1] > 0:
                for idx in [0, 1, 3, 4, 5, 8, 9]:
                    tileValues[idx] = 0
            if y - 1 >= 0 and dungeon[x, y - 1] > 0:
                for idx in [0, 1, 3, 2, 5, 6, 7]:
                    tileValues[idx] = 0
            if x + 1 < width and dungeon[x + 1, y] > 0:
                for idx in [0, 1, 2, 3, 4, 7, 9]:
                    tileValues[idx] = 0
            if x - 1 >= 0 and dungeon[x - 1, y] > 0:
                for idx in [0, 1, 2, 4, 5, 6, 8]:
                    tileValues[idx] = 0
            # Set the tile value to the first legal value
            output[x, y] = tileValues.index(1)
    return output
         

'''
    generateRoom(roomType, maxSize) creates an array "room."
    Precondition: maxSize must be bigger than (3, 3).
    Returns a numpy array representing the room
'''
def generateRoom(roomType, maxSize):
    # fallback on the smallest room of All Time: no room
    room = np.zeros([maxSize[0], maxSize[1]])
    if roomType == BigRooms.BigRect:
        room = np.ones([random.randrange(3, maxSize[0]),
                         random.randrange(3, maxSize[1])])
    elif roomType == BigRooms.TwoSmall:
        room = np.ones([random.randrange(3, maxSize[0]),
                         random.randrange(3, maxSize[1])])
    return room

# Test the code
dungeon = createDungeonSnapshot((8, 10))
print(addWallResolution(dungeon))