from typing import Dict, List, Tuple, Union
from room import Room
import random
import math

"""
https://docs.python.org/3/library/typing.html#type-aliases
"""

# room coordinates
RoomCoords = Tuple[int, int]
# direction[e, w, n, s] of other room and number of other room
RoomConnections = Dict[str, int]
# graph of rooms
RoomGraph = Dict[int, List[Union[RoomCoords, RoomConnections]]]

class World:
    def __init__(self):
        self.starting_room = None
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
    def load_graph(self, room_graph: RoomGraph):
        # length of the dict/iterable
        num_rooms = len(room_graph)
        # creates a list with None in each index
        # by the number of rooms that exist
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):

            # get the x coordinate
            x = room_graph[i][0][0]
            
            # get the max grid size out of the default grid size, x coordinate,
            # and y coordinate
            grid_size = max(grid_size, room_graph[i][0][0], room_graph[i][0][1])

            # set the room at index of i with a Room object
            self.rooms[i] = Room(
                f"Room {i}", 
                f"({room_graph[i][0][0]},{room_graph[i][0][1]})",
                i, 
                room_graph[i][0][0], 
                room_graph[i][0][1]
            )
            
        self.room_grid = []

        # add 1 to whatever the max grid_size ends up being
        grid_size += 1
        # lock it in
        self.grid_size = grid_size

        for i in range(0, grid_size):
            # create the grid layout
            self.room_grid.append([None] * grid_size)
            
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if 'n' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('n', self.rooms[room_graph[room_id][1]['n']])
            if 's' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('s', self.rooms[room_graph[room_id][1]['s']])
            if 'e' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('e', self.rooms[room_graph[room_id][1]['e']])
            if 'w' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms('w', self.rooms[room_graph[room_id][1]['w']])
        self.starting_room = self.rooms[0]

    def print_rooms(self):
        rotated_room_grid = []
        for i in range(0, len(self.room_grid)):
            rotated_room_grid.append([None] * len(self.room_grid))
        for i in range(len(self.room_grid)):
            for j in range(len(self.room_grid[0])):
                rotated_room_grid[len(self.room_grid[0]) - j - 1][i] = self.room_grid[i][j]
        print("#####")
        str = ""
        for row in rotated_room_grid:
            all_null = True
            for room in row:
                if room is not None:
                    all_null = False
                    break
            if all_null:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")


