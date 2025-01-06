import random
import pygame
import os

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
        roomType = 0
        i = random.randint(1, 100)
        if i <= nC:
            roomType = 1
        elif i <= nC + e:
            roomType = 2
        elif i <= nC + e + eC:
            roomType = 3
        elif i <= nC + e + eC + s:
            roomType = 4
        else:
            roomType = 6
        return roomType
    
    for floor in range(2, 9):
        for room in map[floor].keys():
            map[floor][room] = roomAssign()
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
            for room in map[14].keys():
                if map[14][room] == 6:
                    roomType = roomAssign()
                    while roomType == 6:
                        roomType = roomAssign()
                    map[14][room] = roomType
            return map
        
        for type in map[14].values():
            if type == 6:
                map = floor14Camp(map)
                break
        
        def earlyEC(map):
            '''Makes sure there is no elites or campfires below floor 6

            args: 
                map: dictionary with keys that represent the floor with a another dictonary as its value with the keys representing the room number and the value representing the room type
            
            returns
                map: but with the rooms breaking the condition fixed
            '''
            for floor in range(2, 6):
                for room in map[floor].keys():
                    if map[floor][room] == 3 or map[floor][room] == 6:
                        roomType = roomAssign()
                        while roomType == 3 or roomType == 6:
                            roomType = roomAssign()
                        map[floor][room] = roomType
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
    i = 0
    mapDisplay = []
    pathDisplay = [[' ' for _ in range(13)] for _ in range(14)]

    for start, end in path.items():
            startFloor, startRoom = start
            i = startFloor - 1
            for connected in end:
                endRoom = connected[1]
                if startRoom == endRoom:
                    pathDisplay[i][startRoom * 2] = '|'
                elif endRoom < startRoom:
                    pathDisplay[i][startRoom * 2 - 1] = '\\'
                else:
                    pathDisplay[i][startRoom * 2 + 1] = '/'
    for floor, room in map.items():
        floorDisplay = ''
        for i in range(0, 7):
            if i not in room:
                floorDisplay += '  '
            else:
                floorDisplay += f'{room[i]} '
        mapDisplay.append(floorDisplay)
        if floor < 15:
            mapDisplay.append(''.join(pathDisplay[floor - 1]))
    map[16] = {4: 7}
    paths_needed = {i for i in map[15].keys()}
    sorted(paths_needed)
    boss_path = {
        1: [' ' for _ in range(13)],
        2: [' ' for _ in range(13)],
        3: [' ' for _ in range(13)],
        4: [' ' for _ in range(13)],
        5: [' ' for _ in range(13)]
    }
    floor16 = '      7      '
    i = 1
    if 0 in paths_needed:
        for path_boss in boss_path.values():
            path_boss[i] = '/'
            i += 1
    i = 3
    if 1 in paths_needed:
        for path_boss in boss_path.values():
            if i <= 5:
                path_boss[i] = '/'
                i += 1
            else:
                path_boss[6] = '|'
    i = 5
    if 2 in paths_needed:
        for path_boss in boss_path.values():
            if i <= 5:
                path_boss[i] = '/'
                i += 1
            else:
                path_boss[6] = '|'
    if 3 in paths_needed:
        for path_boss in boss_path.values():
            path_boss[6] = '|'
    i = 7
    if 4 in paths_needed:
        for path_boss in boss_path.values():
            if i > 6:
                path_boss[i] = '\\'
                i -= 1
            else:
                path_boss[6] = '|'
    i = 9
    if 5 in paths_needed:
        for path_boss in boss_path.values():
            if i > 6:
                path_boss[i] = '\\'
                i -= 1
            else:
                path_boss[6] = '|'
    i = 11
    if 6 in paths_needed:
        for path_boss in boss_path.values():
            path_boss[i] = '\\'
            i -= 1
    for pathDis in boss_path.values():
        path_boss = ''.join(pathDis)
        mapDisplay.append(path_boss)
    # Adding paths to the boss room to map display
    mapDisplay.append(floor16)
    for room_num in map[15].keys():
        path[(15, room_num)] = [[16, 4]]
    i = 1
    for j in range(0, 30, 2):
        if i < 10:
            mapDisplay[j] = f'{i}:  ' + mapDisplay[j]
        else:
            mapDisplay[j] = f'{i}: ' + mapDisplay[j]
        i += 1
    for j in range(1, 30, 2):
        mapDisplay[j] = f'    ' + mapDisplay[j]
        i += 1
    for j in range(30, 35):
        mapDisplay[j] = f'    ' + mapDisplay[j]
    return map, path, mapDisplay

class Map:
    def __init__(self, asc):
        self.map, self.path, self.mapDisplay = createMap(asc)
        self.rooms = []
        for floor, room in self.map.items():
            for room_num, room_type in room.items():
                self.rooms.append(Room(room_type, floor, room_num))
        for room in self.rooms:
            for connection in self.path[(room.floor, room.room_num)]:
                room.add_connection(connection)
    
    

class Room:
    def __init__(self, room_type, floor, room_num):
        self.room_type = room_type
        self.floor = floor
        self.room_num = room_num
        self.connections = []
        room_type_to_sprite = {
            1: 'assets/icons/combat.png',
            2: 'assets/icons/event.png',
            3: 'assets/icons/elite.png',
            4: 'assets/icons/shop.png',
            5: 'assets/icons/chest.png',
            6: 'assets/icons/campfire.png',
            7: 'assets/icons/boss.png'
        }
        self.sprite = pygame.image.load(room_type_to_sprite[room_type])

    def add_connection(self, connection):
        self.connections.append(connection)

    def draw(self, screen, x, y):
        screen.blit(self.sprite, (x, y))

