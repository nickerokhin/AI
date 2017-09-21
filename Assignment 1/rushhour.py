# Color, (Row, Column)
#Rules
#----------------------
#Blocks may not overlap, each set of coordinates must be unique
#Each block has a locked axis that cannot be broken
#Neither X nor Y may exceed a value of 5
#Each "decision" is one block moving one direction -1 or +1 on the free axis,
#resulting in up to 16 child nodes for every parent node
#If a decision breaks a rule, that state is discarded and not counted
#If a state already exists in the list of computed states, don't add it to the graph
#Goal state (R: (2,4), (2,5))
#(stateID, State)

import pprint
import numpy as np
pp = pprint.PrettyPrinter(indent=4)

initialstate = {"LG": [(0,0), (0,1)],
          "Y": [(0,5), (1,5), (2,5)],
          "P": [(1,0),(2,0),(3,0)],
          "BR": [(4,0), (5,0)],
          "DG": [(5, 2), (5, 3), (5, 4)],
          "LB": [(4, 3), (4, 4)],
          "DB": [(1,3), (2, 3), (3,3)],
          "R": [(2,1), (2,2)]}



teststate = {"LG": [(0,1), (0,2)],
          "Y": [(0,5), (1,5), (2,5)],
          "P": [(1,0),(2,0),(3,0)],
          "BR": [(4,0), (5,0)],
          "DG": [(5, 2), (5, 3), (5, 4)],
          "LB": [(4, 4), (4, 5)],
          "DB": [(1,3), (2, 3), (3,3)],
          "R": [(2,1), (2,2)]}

teststate2 = {"LG": [(0,1), (0,2)],
          "Y": [(0,5), (1,5), (2,5)],
          "R": [(1,0),(2,0),(3,0)],
          "BR": [(4,0), (5,0)],
          "DG": [(5, 2), (5, 3), (5, 4)],
          "LB": [(4, 3), (4, 4)],
          "DB": [(1,3), (2, 3), (3,3)],
          "R": [(2,1), (2,2)]}


teststate3 = {"LG": [(0,1), (0,2)],
          "Y": [(1,5), (2,5), (3,5)],
          "P": [(1,0),(2,0),(3,0)],
          "BR": [(4,0), (5,0)],
          "DG": [(5, 2), (5, 3), (5, 4)],
          "LB": [(4, 3), (4, 4)],
          "DB": [(1,3), (2, 3), (3,3)],
          " R": [(2,1), (2,2)]}

teststate4 = {'BR': [(3, 0), (4, 0)],
    'DB': [(1, 3), (2, 3), (3, 3)],
    'DG': [(5, 0), (5, 1), (5, 2)],
    'LB': [(4, 1), (4, 2)],
    'LG': [(0, 2), (0, 3)],
    'P': [(0, 0), (1, 0), (2, 0)],
    'R': [(2, 1), (2, 2)],
    'Y': [(2, 5), (3, 5), (4, 5)]}

def makedictfromtup(i):
    statedict = dict()
    statedict["LG"] = list(i[0])
    statedict["Y"] = list(i[1])
    statedict["P"] = list(i[2])
    statedict["BR"] = list(i[3])
    statedict["DG"] = list(i[4])
    statedict["LB"] = list(i[5])
    statedict["DB"] = list(i[6])
    statedict["R"] = list(i[7])
    return statedict

def maketupfromdict(statedict):

    tup1 = tuple(statedict["LG"])
    tup2 = tuple(statedict["Y"])
    tup3 = tuple(statedict["P"])
    tup4 = tuple(statedict["BR"])
    tup5 = tuple(statedict["DG"])
    tup6 = tuple(statedict["LB"])
    tup7 = tuple(statedict["DB"])
    tup8 = tuple(statedict["R"])
    return (tup1, tup2, tup3, tup4, tup5, tup6, tup7, tup8)

def coordsavailable(newcoords, coords):
    if newcoords == []:
        return False
    #print(coords)
    for i in newcoords:
        if i in coords:
            return False
    return True

def createnewstates(state):
    states = []
    state = makedictfromtup(state)

    for key in state:
        x = []
        y = []
        lock = None
        takencoords = []
        #Two tempstates necessary because overwriting would occur when same
        #Variable is manipulated and used again
        #Initializing key variables for state
        tempstate = state.copy()
        tempstate2 = state.copy()
        active = []
        newcoords = []
        newactive = []
        activefwd = []
        activeback = []
        #All coordinates used by blocks that aren't the current block
        for key2 in state:
            if key2 != key:
                for coords in state[key2]:
                    takencoords.append(coords)
        #Creating two arrays
        for i in state[key]:
            x.append(i[0])
            y.append(i[1])

        #Checking which axis is locked
        if(all(i==x[0] for i in x)):
            #All values the same in X axis
            active = y
            lock = 0
        if(all(i==y[0] for i in y)):
            #All values the same in Y axis
            active = x
            lock = 1
        #At "Left" edge
        if active[0] == 0:
            #cant move back
            newactive = [x + 1 for x in active]
            if lock:
                newcoords = [(newactive[i], y[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(maketupfromdict(tempstate))
                    #print("Changed:", key, " ", state[key], "to", newcoords )


            elif not lock:

                newcoords = [(x[i], newactive[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(maketupfromdict(tempstate))
                    #print("Changed:", key, " ", state[key], "to", newcoords )

        #At "Right" edge
        elif active[-1] == 5:
            #cant move fwd
            newactive = [x - 1 for x in active]
            if lock:
                newcoords = [(newactive[i], y[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(maketupfromdict(tempstate))
                    #print("Changed:", key, " ", state[key], "to", newcoords )

            elif not lock:

                newcoords = [(x[i], newactive[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(maketupfromdict(tempstate))
                    #print("Changed:", key, " ", state[key], "to", newcoords )

        else:
            #At neither edge
            activeback = [x - 1 for x in active]
            activefwd = [x + 1 for x in active]
            #if key == "Y":
            #    print(activeback)
            #    print(activefwd)
            if lock:
                #y axis is locked
                newcoordsfwd = [(activefwd[i], y[i]) for i in range(0, len(active))]
                newcoordsback = [(activeback[i], y[i]) for i in range(0, len(active))]
                #if key == "Y":
                #    print(newcoordsfwd)
                #    print(newcoordsback)
                if coordsavailable(newcoordsfwd, takencoords):
                    tempstate[key] = newcoordsfwd
                    states += [maketupfromdict(tempstate)]
                    #if key == "Y":
                    #    print("Cond fwd")
                    #    print(tempstate)
                    #    pp.pprint(states)
                    #pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsfwd )


                if coordsavailable(newcoordsback, takencoords):
                    #print(newcoordsback
                    tempstate2[key] = newcoordsback
                    states.append(maketupfromdict(tempstate2))

                    #if key == "Y":
                    #    print("Cond back")
                    #    print(tempstate)
                        #pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsback )


            elif not lock:
                #x axis is locked
                newcoordsfwd = [(x[i], activefwd[i]) for i in range(0, len(active))]
                newcoordsback = [(x[i], activeback[i]) for i in range(0, len(active))]

                if coordsavailable(newcoordsfwd, takencoords):
                    #print(newcoordsfwd)
                    tempstate[key] = newcoordsfwd
                    states += [maketupfromdict(tempstate)]
                    #print("Changed:", key, " ", state[key], "to", newcoordsfwd )

                if coordsavailable(newcoordsback, takencoords):
                    #print(newcoordsback)
                    tempstate2[key] = newcoordsback
                    states.append(maketupfromdict(tempstate2))
                    #More Debug
                    #if key == "Y":
                    #    print("Cond Back")
                    #    pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsback )
    #Debug
    '''
        if key == "Y":
            print(lock)
            print(newcoordsback)
            print(newcoordsfwd)
            pp.pprint(tempstate)
            print(takencoords)

    print(len(states))
    #pp.pprint(initialstate)
    mat = [[" " for i in range(6)] for k in range(6)]
    for i in states:
        for key in i:
            for j in i[key]:
                mat[j[0]][j[1]] = key
        matr = np.matrix(mat)
        print(matr)
        print("\n")
        mat = [[" " for i in range(6)] for k in range(6)]
    '''

    return states





def graphsearch(state):
    goal = [(2,4), (2,5)]
    frontier = createnewstates(state)
    explored = set([state])
    while 1:

        if len(frontier) == 0:
            print("Frontier exhaused")
            print("Final set length:", len(explored))
            return False

        leaf = frontier.pop()
        leafdict = makedictfromtup(leaf)
        #Used to visualize the state
        #Uncomment this to visualize the board via a matrix
        '''
        mat = [[" " for i in range(6)] for k in range(6)]
        for key in leafdict:
            for j in leafdict[key]:
                mat[j[0]][j[1]] = key
        mat = np.matrix(mat)
        print(mat)
        '''


        #pp.pprint(leaf)

        #Solution found
        #Uncomment this to find solution asap
        #if leafdict["R"] == goal:
            #print("Solution Found!")
            #return True
        explored.add(leaf)
        newfrontier = createnewstates(leaf)
        for i in newfrontier:
            if i not in explored:
                frontier.append(i)


def treesearch(state):
    goal = [(2,4), (2,5)]
    frontier = createnewstates(state)
    while 1:
        if len(frontier) == 0:
            return False
        leaf = frontier.pop()
        if leaf["R"] == goal:
            print("Success")
            return leaf

        frontier += createnewstates(leaf)

#pp.pprint(initialstate)
#tatetuple = maketupfromdict(initialstate)
#print(statetuple)
#statedict = makedictfromtup(statetuple)
#pp.pprint(statedict)
#graphsearch(initialstate)
#print(board)
#createnewstates(teststate4)
#treesearch(initialstate)
initialstate = maketupfromdict(initialstate)
graphsearch(initialstate)
