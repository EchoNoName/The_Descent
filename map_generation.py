import random
import pygame
import os
import math

def createMap(asc):
    '''Generates a Map with 15 floors with unique events for each room generated, the rooms are also connected with no crossing paths, the map is a 15 x 7 grid of dots that are connected with unused dots being removes, the x locations ranges from [0, 6] while the floors have a y value ranging from [1, 15]

    args: 
        asc: Ascension level of the map being generated represented by an int, effects room chances

    returns:
        map: A dictonary that contains a dictonary with the main key representing the floor and the secondary key representing the room and the value being the type of room
        path: A dictonary that has a key representing the location of a room (floor, room) and the value is a list of all the rooms it is connected to
        mapDisplay: A visualization of the map made of 28 strings
    '''
    # Initialized the Map
    # The map is a dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type
    # room type: 0 = placeholder, 1 = normal combat, 2 = event, 3 = elite combat, 4 = shop, 5 = chest, 6 = campfire
    nC = 45
    eC = 16
    if asc == 0:
        nC = 53
        eC = 8
    def compPathGen():
        map = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        8: {},
        9: {},
        10: {},
        11: {},
        12: {},
        13: {},
        14: {},
        15: {},
    }
        '''Generates the complete paths that determains which rooms are connected with which

        args: 
            none
        
        returns:
            map: dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type
        '''
        path = {}
        def nonOverlapPath(path, room, floor):
            '''Generates a value that makes sure the path that either foes left, straight or right doesn't crosses over with any existing paths
            
            args: 
                path: All current generated paths represented by a dictonary with a tuple (floor, room x value) as the key and a list [room1, room2...] of lists [floor, room x value] representing all the rooms it connects to
                room: The current room location ranging from 0 - 6
                floor: The current floor ranging from 1 - 14
            
            returns:
                connection: The variation is the x value that determains whether the path goes left, straight or right
            '''
            while True:
                if room == 0:
                    connection = random.randint(0, 1)
                elif room == 6:
                    connection = random.randint(-1, 0)
                else:
                    connection = random.randint(-1, 1)
                # Creates a random connection to the rooms above and makes sure connection doesn't go outside the map
                if connection == 0:
                    break
                # If it goes straight up, doesn't need to check for crossing paths
                else:
                    if (floor, room + connection) not in path:
                        break
                    else:
                        if [floor + 1, room] not in path[floor, room + connection]:
                            break
                # Checks for crossing paths
            return connection
        start = [0, 1, 2, 3, 4, 5, 6]
        for i in range(0, 6):
            # Repeat the a process six times
            floor = 1
            if i < 2:
                room = random.choice(start)
                start.remove(room)
                # For the first 2 rooms selected, it makes sure its 2 different starting rooms
            else:
                room = random.randint(0, 6)
                # If not first 2 rooms than duplicate starting rooms are fine
            while floor < 15:
                connection = nonOverlapPath(path, room, floor)
                # Create a connection
                if room not in map[floor]:
                    if floor == 1:
                        map[floor][room] = 1
                    elif floor == 9:
                        map[floor][room] = 5
                    elif floor == 15:
                        map[floor][room] = 6
                    else:
                        map[floor][room] = 0
                    # Certain floors have fixed room types
                if (room + connection) not in map[floor + 1]:
                    if floor + 1 == 9:
                        map[floor + 1][room + connection] = 5
                    elif floor + 1 == 15:
                        map[floor + 1][room + connection] = 6
                    else:
                        map[floor + 1][room + connection] = 0
                    # Certain floors have fixed room types
                if (floor, room) in path:
                    if [floor + 1, room + connection] not in path[floor, room]:
                        path[floor, room].append([floor + 1, room + connection])
                else: 
                    path[floor, room] = []
                    path[floor, room].append([floor + 1, room + connection])
                # Adds connected rooms coordinates to a rooms list in path dictonary for determaining whether a room connects to another room
                floor += 1
                room = room + connection
                # Change the room to the newly generated and connected room
        
        return path, map
    
    path, map = compPathGen()

    def roomAssign(nC = nC, e = 22, eC = eC, s = 5):
        '''Randomly determains a room type based on percentages (53% normal combat, 22% random event, 8% Elite combat, 12% Campfire, 5% shop) or (45% normal combat, 22% random event, 16% Elite combat, 12% Campfire, 5% shop)
        '''
        roomType = 0 # Initialize the room type to 0
        i = random.randint(1, 100) # Generate a random number between 1 and 100
        if i <= nC: # If the random number is less than or equal to nC
            roomType = 1 # Set the room type to 1
        elif i <= nC + e:
            roomType = 2 # Set the room type to 2
        elif i <= nC + e + eC: # If the random number is less than or equal to nC + e + eC
            roomType = 3 # Set the room type to 3
        elif i <= nC + e + eC + s: # If the random number is less than or equal to nC + e + eC + s
            roomType = 4 # Set the room type to 4
        else:
            roomType = 6 # Set the room type to 6
        return roomType
    
    for floor in range(2, 9):
        for room in map[floor].keys():
            map[floor][room] = roomAssign() # Assign a random room type to the room
    for floor in range(10, 15):
        for room in map[floor].keys():
            map[floor][room] = roomAssign()
    # Assign Room type

    def nonValidMapFix(map):

        def floor14Camp(map):
            '''Makes sure there are no campfires at floor 14

            args:
                map: dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type

            returns: 
                map: but with the above fixes
            '''
            for room in map[14].keys(): # Loop through all the rooms in floor 14
                if map[14][room] == 6: # If the room type is 6
                    roomType = roomAssign() # Assign a random room type to the room
                    while roomType == 6: # While the room type is 6
                        roomType = roomAssign() # Assign a random room type to the room
                    map[14][room] = roomType # Assign the room type to the room
            return map
        
        for type in map[14].values(): # Loop through all the room types in floor 14
            if type == 6: # If the room type is 6
                map = floor14Camp(map) # Fix the map
                break # Break the loop
        
        def earlyEC(map):
            '''Makes sure there is no elites or campfires below floor 6

            args: 
                map: dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type
            
            returns
                map: but with the rooms breaking the condition fixed
            '''
            for floor in range(2, 6): # Loop through all the floors from 2 to 6
                for room in map[floor].keys(): # Loop through all the rooms in the floor
                    if map[floor][room] == 3 or map[floor][room] == 6: # If the room type is 3 or 6
                        roomType = roomAssign() # Assign a random room type to the room
                        while roomType == 3 or roomType == 6: # While the room type is 3 or 6
                            roomType = roomAssign() # Assign a random room type to the room
                        map[floor][room] = roomType # Assign the room type to the room
            return map

        map = earlyEC(map)

        def uniquePaths(map):
            '''Fixes crossroads (rooms that can lead to multiple rooms) all have unique options and consequtive elites, shops, or campfires and assigns them new room types, done by checking the rooms that a room is connected to

            args:
                map: dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type
            
            returns: 
                map: but with all the room types fixed
            '''
            def otherConnectionCheck(i):
                a = [0]
                # Initilized a as a holder for the room type of other rooms that are connected to the room connected to the key room
                if connections[i][1] - 1 in map[floor] and connections[i][1] - 1 != room:
                # If the room to the left and 1 floor lower to the connected room exists
                    if connections[i] in path[(floor, connections[i][1] - 1)]:
                    # If that room is connected to the connected room who is connected to the key room
                        a.append(map[floor][connections[i][1] - 1])
                        # append the roomtype to a
                if connections[i][1] + 1 in map[floor] and connections[i][1] + 1 != room:
                # If the room to the right and 1 floor lower to the connected room exists and if its a different room from the key room
                    if connections[i] in path[(floor, connections[i][1] + 1)]:
                    # If that room is connected to the connected room who is connected to the key room
                        a.append(map[floor][connections[i][1] + 1])
                        # append the roomtype to a
                if connections[i][1] in map[floor] and connections[i][1] != room:
                # If the room to the right and 1 floor lower to the connected room exists and if its a different room from the key room
                    if connections[i] in path[(floor, connections[i][1])]:
                    # If that room is connected to the connected room who is connected to the key room
                        a.append(map[floor][connections[i][1]])
                        # append the roomtype to a
                return a
            for location, connections in path.items():
                # loops through all the keys and values of path, keys represents the location of a room, value represents all the locations of the rooms the key connects to
                # for referance I will refer to the room that have paths leading to other rooms as the ket rooms, its location is the key of path
                floor, room = location
                # Unpacks the location of the room into its floor and room location
                if floor == 8 or floor == 14:
                    # if it's floor 8 or 14
                    continue
                    # if it is, since all the rooms in floor 9 and 15 are predetermained and always the same, it moves on to the next room as no changes need to be made
                numOfConnections = len(connections)
                # Finds the # of rooms the key room connects to
                valid = {1, 2, 3, 4, 5, 6}
                # Initializes a set of all the types of rooms that represents the valid types of rooms, will be modified later
                if numOfConnections == 1:
                    # If it only connects to 1 room, will only check for consecutive elites, shops, or campfires in this case
                    if map[floor][room] == 1 or map[floor][room] == 2:
                        # If the key room is a normal combat or event
                        continue
                        # continues to next room because consequtive normal combats and events are allowed
                    else:
                        if map[floor][room] == map[connections[0][0]][connections[0][1]]:
                            # If the 2 consecutive rooms are the same
                            if floor + 1 < 6:
                                # If the floor is below 6
                                valid = {1, 2, 4}
                                # Set valid rooms to exclude elites and campfire
                            if floor == 13:
                            # If its the 13th floor
                                valid.remove(6)
                                # Remove campfires from the valid pool as floor 14 can't have campfires
                            a = otherConnectionCheck(0)
                            # Checks if other rooms connects to the same room that the key room connects 
                            for i in a:
                            # Goes through every room type of rooms that are also connected the room the key room connects to
                                if i in valid and i != 1 and i != 2:
                                # if its in valid and its not a normal combat/event
                                    valid.remove(i)
                                    # remove it from valid
                            roomType = roomAssign()
                            # Uses the roomAssign function to get a room type
                            while roomType not in valid:
                                # If its not a valid room
                                roomType = roomAssign()
                                # Do it again
                            map[connections[0][0]][connections[0][1]] = roomType
                            # Change the connected room to a new room type that is different from the current room
                else:
                # If there are more than 1 room connected
                    if numOfConnections == 2:
                        # In the case of 2 choices of rooms 
                        typesOfRooms = [map[connections[0][0]][connections[0][1]], map[connections[1][0]][connections[1][1]]]
                        # A list of 2 numbers that represents the room type of the 2 connected room
                        if (map[floor][room] not in typesOfRooms or map[floor][room] in {1, 2}) and typesOfRooms[0] != typesOfRooms[1]:
                            # if the key room is not the same as either of the 2 connected room or if its a normal combat/enent and the 2 rooms are not the same
                            continue
                            # The rooms are valid and continue to the next room
                        if floor + 1 < 6:
                            # if the floor is below 6
                            valid.remove(3)
                            valid.remove(6)
                            # remove elites and campfires from the valid room pool
                        if map[floor][room] not in {1, 2}:
                            # If the key room isn't a normal combat or event
                            valid.remove(map[floor][room])
                            # Remove the key room room type from valid room types set
                        if floor == 13 and 6 in valid:
                            # If its the 13th floor and campfires hasn't already been removed
                                valid.remove(6)
                                # Remove campfires from the valid pool as floor 14 can't have campfires
                        validA = valid
                        a = otherConnectionCheck(0)
                        # Checks if other rooms connects to the same room that the key room connects 
                        for i in a:
                        # Goes through every room type of rooms that are also connected the room the key room connects to
                            if i in validA and i != 1 and i != 2:
                            # if its in valid and its not a normal combat/event
                                validA.remove(i)
                                # remove it from valid
                        validB = valid
                        a = otherConnectionCheck(1)
                        # Checks if other rooms connects to the same room that the key room connects 
                        for i in a:
                        # Goes through every room type of rooms that are also connected the room the key room connects to
                            if i in validB and i != 1 and i != 2:
                            # if its in valid and its not a normal combat/event
                                validB.remove(i)
                                # remove it from valid
                        roomAType = roomAssign()
                        roomBType = roomAssign()
                        # For the 2 rooms that are connected the key room determain a random room type using roomAssign function
                        while roomAType not in validA or roomBType not in validB or roomBType == roomAType:
                            # While roomAType is not a valid room type for the map or roomBType is not a valid room type for the map or the same as roomAType (Unique crossroads are required)
                            roomAType = roomAssign()
                            roomBType = roomAssign()
                            # Redo the roomAssign function until it is valid
                        map[connections[0][0]][connections[0][1]] = roomAType
                        map[connections[1][0]][connections[1][1]] = roomBType
                        # Reassign the room types value for the connected rooms
                    else:
                    # The only case that can reach here is if there care 3 rooms that are connected to the key room
                        typesOfRooms = [map[connections[0][0]][connections[0][1]], map[connections[1][0]][connections[1][1]], map[connections[2][0]][connections[2][1]]]
                        # A list of 3 numbers that represents the room type of the 3 connected room
                        if (map[floor][room] not in typesOfRooms or map[floor][room] in {1, 2}) and typesOfRooms[0] != typesOfRooms[1] and typesOfRooms[0] != typesOfRooms[2] and typesOfRooms[1] != typesOfRooms[2]:
                            # if the key room is not the same as either of the 3 connected room or if its a normal combat/enent and all 3 of the connected rooms are not the same
                            continue
                            # The rooms are valid and continue to the next room
                        if floor + 1 < 6:
                        # if the floor is below 6
                            valid.remove(3)
                            valid.remove(6)
                            # remove elites and campfires from the valid room pool
                        if map[floor][room] not in {1, 2}:
                        # If the key room isn't a normal combat or event
                            valid.remove(map[floor][room])
                            # Remove the key room room type from valid room types set
                        if floor == 13 and 6 in valid:
                            # If its the 13th floor and campfires hasn't already been removed
                                valid.remove(6)
                                # Remove campfires from the valid pool as floor 14 can't have campfires
                        validA = valid
                        a = otherConnectionCheck(0)
                        # Checks if other rooms connects to the same room that the key room connects 
                        for i in a:
                        # Goes through every room type of rooms that are also connected the room the key room connects to
                            if i in validA and i != 1 and i != 2:
                            # if its in valid and its not a normal combat/event
                                validA.remove(i)
                                # remove it from valid
                        validB = valid
                        a = otherConnectionCheck(1)
                        # Checks if other rooms connects to the same room that the key room connects 
                        for i in a:
                        # Goes through every room type of rooms that are also connected the room the key room connects to
                            if i in validB and i != 1 and i != 2:
                            # if its in valid and its not a normal combat/event
                                validB.remove(i)
                                # remove it from valid
                        validC = valid
                        a = otherConnectionCheck(2)
                        # Checks if other rooms connects to the same room that the key room connects 
                        for i in a:
                        # Goes through every room type of rooms that are also connected the room the key room connects to
                            if i in validC and i != 1 and i != 2:
                            # if its in valid and its not a normal combat/event
                                validC.remove(i)
                                # remove it from valid
                        roomAType = roomAssign()
                        roomBType = roomAssign()
                        roomCType = roomAssign()
                        # For the 3 rooms that are connected the key room determain a random room type using roomAssign function
                        while roomAType not in validA or roomBType not in validB or roomBType == roomAType or roomCType not in validC or roomCType == roomAType or roomCType == roomBType:
                        # While roomAType is not a valid room type for the map or roomBType is not a valid room type for the map or the same as roomAType (Unique crossroads are required) or roomCType is not a valid room type for the map or the same as roomAType or roomBType (Unique crossroads are required)
                            roomAType = roomAssign()
                            roomBType = roomAssign()
                            roomCType = roomAssign()
                            # Redo the roomAssign function until it is valid
                        map[connections[0][0]][connections[0][1]] = roomAType
                        map[connections[1][0]][connections[1][1]] = roomBType
                        map[connections[2][0]][connections[2][1]] = roomCType
                        # Reassign the room types value for the connected rooms
            return map
        
        map = uniquePaths(map)

        return map
    
    map = nonValidMapFix(map)
    i = 0 # Initialize i to 0
    mapDisplay = [] # Initialize mapDisplay to an empty list
    pathDisplay = [[' ' for _ in range(13)] for _ in range(14)] # Initialize pathDisplay to a list of 14 lists of 13 empty strings

    for start, end in path.items(): # Loop through all the items in path
            startFloor, startRoom = start # Unpack the start floor and room
            i = startFloor - 1 # Set i to the start floor minus 1
            for connected in end: # Loop through all the connected rooms
                endRoom = connected[1]
                if startRoom == endRoom: # If the start room is the same as the end room
                    pathDisplay[i][startRoom * 2] = '|' # Set the pathDisplay to a vertical line
                elif endRoom < startRoom: # If the end room is less than the start room
                    pathDisplay[i][startRoom * 2 - 1] = '\\' # Set the pathDisplay to a backslash
                else: # If the end room is greater than the start room
                    pathDisplay[i][startRoom * 2 + 1] = '/' # Set the pathDisplay to a forward slash
    for floor, room in map.items(): # Loop through all the items in map
        floorDisplay = '' # Initialize floorDisplay to an empty string
        for i in range(0, 7): # Loop through all the items in the room
            if i not in room:
                floorDisplay += '  '
            else:
                floorDisplay += f'{room[i]} ' # Add the room type to the floorDisplay
        mapDisplay.append(floorDisplay) # Add the floorDisplay to the mapDisplay
        if floor < 15: # If the floor is less than 15
            mapDisplay.append(''.join(pathDisplay[floor - 1])) # Add the pathDisplay to the mapDisplay
    map[16] = {4: 7} # Set the 16th floor to have a room with a room type of 7
    paths_needed = {i for i in map[15].keys()} # Set paths_needed to the keys of the 15th floor
    sorted(paths_needed) # Sort paths_needed
    boss_path = { # Initialize boss_path to a dictionary with 5 keys and 13 values
        1: [' ' for _ in range(13)], # Initialize the 1st key to a list of 13 empty strings
        2: [' ' for _ in range(13)], # Initialize the 2nd key to a list of 13 empty strings
        3: [' ' for _ in range(13)], # Initialize the 3rd key to a list of 13 empty strings
        4: [' ' for _ in range(13)], # Initialize the 4th key to a list of 13 empty strings
        5: [' ' for _ in range(13)] # Initialize the 5th key to a list of 13 empty strings
    }
    floor16 = '      7      ' # Initialize floor16 to a string with a room type of 7
    i = 1 # Initialize i to 1
    if 0 in paths_needed: # If 0 is in paths_needed
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            path_boss[i] = '/'
            i += 1
    i = 3
    if 1 in paths_needed: # If 1 is in paths_needed
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            if i <= 5: # If i is less than or equal to 5
                path_boss[i] = '/' # Set the path_boss to a forward slash
                i += 1 # Increment i by 1
            else:
                path_boss[6] = '|'
    i = 5
    if 2 in paths_needed: # If 2 is in paths_needed
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            if i <= 5: # If i is less than or equal to 5
                path_boss[i] = '/' # Set the path_boss to a forward slash
                i += 1
            else:
                path_boss[6] = '|' # Set the path_boss to a vertical line
    if 3 in paths_needed: # If 3 is in paths_needed
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            path_boss[6] = '|' # Set the path_boss to a vertical line
    i = 7 # Initialize i to 7
    if 4 in paths_needed:
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            if i > 6: # If i is greater than 6
                path_boss[i] = '\\' # Set the path_boss to a backslash
                i -= 1 # Decrement i by 1
            else:
                path_boss[6] = '|' # Set the path_boss to a vertical line
    i = 9
    if 5 in paths_needed:
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            if i > 6: # If i is greater than 6
                path_boss[i] = '\\' # Set the path_boss to a backslash
                i -= 1 # Decrement i by 1
            else:
                path_boss[6] = '|' # Set the path_boss to a vertical line
    i = 11 # Initialize i to 11
    if 6 in paths_needed: # If 6 is in paths_needed
        for path_boss in boss_path.values(): # Loop through all the values in boss_path
            path_boss[i] = '\\' # Set the path_boss to a backslash
            i -= 1 # Decrement i by 1
    for pathDis in boss_path.values(): # Loop through all the values in boss_path
        path_boss = ''.join(pathDis) # Join the pathDis to a string
        mapDisplay.append(path_boss)
    # Adding paths to the boss room to map display
    mapDisplay.append(floor16)
    for room_num in map[15].keys(): # Loop through all the keys in the 15th floor
        path[(15, room_num)] = [[16, 4]] # Set the path to the boss room
    i = 1 # Initialize i to 1
    for j in range(0, 30, 2): # Loop through all the items in mapDisplay
        if i < 10:
            mapDisplay[j] = f'{i}:  ' + mapDisplay[j] # Add the floor number to the mapDisplay
        else:
            mapDisplay[j] = f'{i}: ' + mapDisplay[j] # Add the floor number to the mapDisplay
        i += 1 # Increment i by 1
    for j in range(1, 30, 2): # Loop through all the items in mapDisplay
        mapDisplay[j] = f'    ' + mapDisplay[j] # Add the floor number to the mapDisplay
        i += 1
    for j in range(30, 35): # Loop through all the items in mapDisplay
        mapDisplay[j] = f'    ' + mapDisplay[j] # Add the floor number to the mapDisplay
    return map, path, mapDisplay

class Map:
    def __init__(self, asc = 0, map_info = None):
        if map_info == None: # If map_info is None
            self.map, self.path, self.mapDisplay = createMap(asc) # Create the map, path, and mapDisplay
            self.entered_rooms = [] # Initialize entered_rooms to an empty list
        else:
            self.map, self.path, self.mapDisplay, self.entered_rooms = map_info # Set the map, path, mapDisplay, and entered_rooms to the map_info
            map_copy = {} # Initialize map_copy to an empty dictionary
            for i in range(1, 16): # Loop through all the items in map_copy
                map_copy[i] = {} # Set the map_copy to a dictionary with the floor number as the key
                if str(i) in self.map:  # Check if floor exists as string key
                    for key, value in self.map[str(i)].items(): # Loop through all the items in self.map
                        map_copy[i][int(key)] = int(value) # Set the map_copy to a dictionary with the floor number as the key and the room number as the value
            self.map = map_copy # Set the map to the map_copy
        self.rooms = [] # Initialize rooms to an empty list
        self.map[16] = {4: 7} # Set the 16th floor to have a room with a room type of 7
        for floor, room in self.map.items(): # Loop through all the items in self.map
            for room_num, room_type in room.items(): # Loop through all the items in room
                self.rooms.append(Room(int(room_type), int(floor), int(room_num))) # Add the room to the rooms list
        for room in self.rooms: # Loop through all the items in self.rooms
            if room.floor != 16: # If the floor is not 16
                for connection in self.path[(room.floor, room.room_num)]: # Loop through all the items in self.path
                    room.add_connection(connection) # Add the connection to the room
        # Connect floor 0,0 to all rooms in floor 1
        self.path[(0, 0)] = [] # Set the path to the start room
        if '1' in self.map: # If the 1st floor exists
            self.map[1] = self.map['1']
        for room_num in self.map[1].keys(): # Loop through all the items in self.map
            self.path[(0, 0)].append([1, int(room_num)]) # Add the connection to the path
        self.y = 0 # Initialize y to 0
        for id in self.entered_rooms: # Loop through all the items in self.entered_rooms
            for room in self.rooms: # Loop through all the items in self.rooms
                if room.floor == id[0] and room.room_num == id[1]: # If the room is the entered room
                    room.entered = True # Set the room to entered
        

    def draw(self, screen, x, y):
        """Draw the map with rooms and connections"""
        # Create scrollable surface that matches screen dimensions
        map_surface = pygame.Surface((1600, 1800), pygame.SRCALPHA)  # Double height to fit full map

        # Calculate spacing between rooms
        x_spacing = 100
        y_spacing = 100
        
        # Calculate starting x position to center map horizontally
        map_width = 6 * x_spacing  # 6 spaces between 7 rooms
        start_x = (1600 - map_width) // 2
        x = start_x

        # Draw connections first so they appear behind rooms
        for floor in range(1, 16):
            for room_num in self.map[floor].keys():
                # Get source room position
                src_x = x + (room_num - 1) * x_spacing + 22  # Added offset to center connections
                src_y = floor * y_spacing + 65  # Increased y offset to lower connections
                
                # Draw connection lines to each connected room
                for dest_floor, dest_room in self.path[(floor, room_num)]:
                    dest_x = x + (dest_room - 1) * x_spacing + 22  # Added offset to center connections
                    dest_y = dest_floor * y_spacing + 65  # Increased y offset to lower connections
                    
                    # Calculate angle and position for connection sprite
                    angle = -math.atan2(dest_y - src_y, dest_x - src_x)  # Negated angle to flip horizontally
                    distance = math.sqrt((dest_x - src_x)**2 + (dest_y - src_y)**2)
                    
                    # Create dotted line connection
                    dot_spacing = 15  # Space between dots
                    dot_size = 4  # Size of each dot
                    num_dots = int(distance / dot_spacing)
                    
                    # Calculate step sizes for x and y
                    dx = (dest_x - src_x) / num_dots
                    dy = (dest_y - src_y) / num_dots
                    
                    # Draw dots along the connection path
                    for i in range(num_dots):
                        dot_x = src_x + dx * i
                        dot_y = src_y + dy * i
                        pygame.draw.circle(map_surface, (102, 6, 6), (int(dot_x), int(dot_y)), dot_size)

        # Draw all rooms
        for room in self.rooms:
            # Calculate room position
            room_x = x + (room.room_num - 1) * x_spacing
            room_y = room.floor * y_spacing + 50  # Changed to normal orientation
            
            # Update room's collision rect to match its position on the scrollable surface
            # Adjust y position by scroll offset to match actual screen position
            room.rect = pygame.Rect(room_x, room_y, room.rect.width, room.rect.height)  # Subtract scroll offset from y position
            
            # Draw the room
            room.draw(map_surface, room_x, room_y)
            # draw the rect
            
        # Draw visible portion of map with scroll offset
        visible_portion = pygame.Rect(0, -self.y, 1600, 900)
        screen.blit(map_surface, (0, 0), visible_portion)

class Room:
    def __init__(self, room_type, floor, room_num):
        self.room_type = room_type # Set the room_type to the room_type
        self.floor = floor # Set the floor to the floor
        self.room_num = room_num # Set the room_num to the room_num
        self.connections = [] # Initialize connections to an empty list
        self.entered = False # Initialize entered to False
        self.entered_circle = pygame.image.load('assets/icons/map/circled.png') # Load the entered_circle image
        room_type_to_sprite = { # Initialize room_type_to_sprite to a dictionary with the room_type as the key and the sprite as the value
            1: 'assets/icons/map/combat.png', # Set the sprite to the combat image
            2: 'assets/icons/map/event.png', # Set the sprite to the event image
            3: 'assets/icons/map/elite.png', # Set the sprite to the elite image
            4: 'assets/icons/map/shop.png', # Set the sprite to the shop image
            5: 'assets/icons/map/chest.png', # Set the sprite to the chest image
            6: 'assets/icons/map/campfire.png', # Set the sprite to the campfire image
            7: 'assets/icons/map/boss.png' # Set the sprite to the boss image
        }
        self.sprite = pygame.image.load(room_type_to_sprite[room_type]) # Load the sprite
        self.rect = self.sprite.get_rect() # Get the rect of the sprite

    def enter(self):
        self.entered = True # Set the room to entered
    
    def update_rect(self, x, y):
        self.rect.topleft = (x, y) # Set the rect to the x and y

    def completed(self, run, map):
        run.room = [self.floor, self.room_num] # Set the room to the floor and room_num
        run.roomInfo = self.room_type # Set the roomInfo to the room_type
        map.entered_rooms.append([self.floor, self.room_num]) # Add the room to the entered_rooms list

    def add_connection(self, connection):
        self.connections.append(connection) # Add the connection to the connections list

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (x, y)) # Draw the sprite
        if self.entered: # If the room is entered
            screen.blit(self.entered_circle, (x - 5, y - 5)) # Draw the entered_circle


