import numpy as np
from enum import Enum
import random

class BigRooms(Enum):
    BigRect = 0
    TwoSmall = 1

'''
    create_dungeon_snapshot((x, y)) creates a dungeon of size x and y
    based on a predefined generation algorithm.
    Precondition: x and y both greater than 3.
    Returns a 2d numpy array of shape (x, y).

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
def create_dungeon_snapshot(shape):
    # Initialize as all walls
    dungeon = np.zeros(shape)
    # Place one "main" room for every 12 units in width or height
    for _ in range((shape[0] // 12) + (shape[1] // 12) + 1):
        room_type = BigRooms.BigRect
        main_room = generate_room(room_type, shape)
        # Make sure it's placed legally,
        # add some padding
        main_room = np.pad(main_room, [(0, random.randint(0, shape[0] - main_room.shape[0])), 
                                    (0, random.randint(0, shape[1] - main_room.shape[1]))])
        main_room = np.pad(np.flip(main_room), [(0, shape[0] - main_room.shape[0]), 
                                            (0, shape[1] - main_room.shape[1])])
        # Now, the room array and dungeon array should be the same size
        # So, we can add the room by just adding the arrays and maxxing 1
        dungeon += main_room
        dungeon[(1 < dungeon)] = 1
    # Generate 2-4 halls out
    for _ in range(random.randint(4, 8)):
        # Find a point to "tunnel" out of
        point = [random.randrange(0, shape[0]), random.randrange(0, shape[1])]
        # Make sure it's a floor, python really has no do while loop huh
        while dungeon[point[0], point[1]] != 1:
            point = [random.randrange(0, shape[0]), random.randrange(0, shape[1])]
        # Choose a direction for the tunnel
        dir = random.randint(0, 3) # 0 = up, go clockwise
        # TODO: Get python 3.10 already stubborn asshole
        if dir == 0:
            while (point[1] >= 0):
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
            while (point[0] >= 0):
                dungeon[point[0], point[1]] = 1
                point[0] -= 1
    return dungeon  

'''
    add_wall_resolution(dungeon) takes a SIMPLE dungeon
    (where 1 = floor, 0 = wall) and returns a dungeon with higher-
    resolution walls (corners, etc.)
    Returns a 2d numpy array of shape dungeon.shape
'''
def add_wall_resolution(dungeon):
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
            6: TL wall
            7: TR wall
            8: BL wall
            9: BR wall
            10: TL corner wall 
            11: TR corner wall
            12: BL corner wall
            13: BR corner wall
        '''
        tile_values = [1] * 15
        if tile < 1:
            # Use neighbors to remove illegal value possibilities
            corner = True
            if y + 1 < height and dungeon[x, y + 1] > 0:
                corner = False
                for idx in [0, 1, 3, 4, 5, 8, 9, 10, 11, 12, 13]:
                    tile_values[idx] = 0
            if y - 1 >= 0 and dungeon[x, y - 1] > 0:
                corner = False
                for idx in [0, 1, 3, 2, 5, 6, 7, 10, 11, 12, 13]:
                    tile_values[idx] = 0
            if x + 1 < width and dungeon[x + 1, y] > 0:
                corner = False
                for idx in [0, 1, 2, 3, 4, 7, 9, 10, 11, 12, 13]:
                    tile_values[idx] = 0
            if x - 1 >= 0 and dungeon[x - 1, y] > 0:
                corner = False
                for idx in [0, 1, 2, 4, 5, 6, 8, 10, 11, 12, 13]:
                    tile_values[idx] = 0
            if corner:
                for idx in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    tile_values[idx] = 0
                if x - 1 >= 0 and y - 1 >= 0 and dungeon[x - 1, y - 1] > 0:
                    for idx in [10, 11, 12]:
                        tile_values[idx] = 0
                elif x - 1 >= 0 and y + 1 < height and dungeon[x - 1, y + 1] > 0:
                    for idx in [10, 12, 13]:
                        tile_values[idx] = 0
                elif x + 1 < width and y + 1 < height and dungeon[x + 1, y + 1] > 0:
                    for idx in [11, 12, 13]:
                        tile_values[idx] = 0
                elif x + 1 < width and y - 1 >= 0 and dungeon[x + 1, y - 1] > 0:
                    for idx in [10, 11, 13]:
                        tile_values[idx] = 0
                else:
                    tile_values[0] = 1
            # Set the tile value to the first legal value
            output[x, y] = tile_values.index(1)
    return output
         

'''
    generate_room(roomType, maxSize) creates an array "room."
    Precondition: maxSize must be bigger than (3, 3).
    Returns a numpy array representing the room
'''
def generate_room(room_type, max_size):
    # fallback on the smallest room of All Time: no room
    room = np.zeros([max_size[0], max_size[1]])
    if room_type == BigRooms.BigRect:
        room = np.ones([random.randrange(3, min(max_size[0], 5)),
                        random.randrange(3, min(max_size[1], 5))])
    elif room_type == BigRooms.TwoSmall:
        room = np.ones([random.randrange(3, max_size[0]),
                         random.randrange(3, max_size[1])])
    return room

class Dungeon:

    array_rep: np.array
    shape = [10, 8]

    def __init__(self, shape):
        self.shape = shape
        self.generate(self.shape)

    def __repr__(self) -> str:
        return str(self.array_rep)

    def as_array(self) -> np.array:
        return self.array_rep

    def as_tileset_array(self) -> np.array:
        return add_wall_resolution(self.array_rep)

    def generate(self, shape = shape):
        self.array_rep = create_dungeon_snapshot(shape)

# dungeon = Dungeon([10, 10])
# print(dungeon)