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
createDungeonSnapshot((8, 10))