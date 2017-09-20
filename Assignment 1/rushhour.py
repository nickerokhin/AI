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

teststate4 = {   'BR': [(3, 0), (4, 0)],
    'DB': [(1, 3), (2, 3), (3, 3)],
    'DG': [(5, 0), (5, 1), (5, 2)],
    'LB': [(4, 1), (4, 2)],
    'LG': [(0, 2), (0, 3)],
    'P': [(0, 0), (1, 0), (2, 0)],
    'R': [(2, 1), (2, 2)],
    'Y': [(2, 5), (3, 5), (4, 5)]}


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

    for key in state:
        x = []
        y = []
        lock = None
        takencoords = []
        tempstate = state.copy()
        tempstate2 = state.copy()
        active = []
        newcoords = []
        newactive = []
        activefwd = []
        activeback = []
        for key2 in state:
            if key2 != key:
                for coords in state[key2]:
                    takencoords.append(coords)
        #print(takencoords)
        for i in state[key]:
            x.append(i[0])
            y.append(i[1])

        if(all(i==x[0] for i in x)):
            active = y
            lock = 0
        if(all(i==y[0] for i in y)):
            active = x
            lock = 1

        if active[0] == 0:
            #cant move back
            newactive = [x + 1 for x in active]
            if lock:
                newcoords = [(newactive[i], y[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(tempstate)
                    #print("Changed:", key, " ", state[key], "to", newcoords )


            elif not lock:

                newcoords = [(x[i], newactive[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(tempstate)
                    #print("Changed:", key, " ", state[key], "to", newcoords )


        elif active[-1] == 5:
            #cant move fwd
            newactive = [x - 1 for x in active]
            if lock:
                newcoords = [(newactive[i], y[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(tempstate)
                    #print("Changed:", key, " ", state[key], "to", newcoords )

            elif not lock:

                newcoords = [(x[i], newactive[i]) for i in range(0, len(active))]
                if coordsavailable(newcoords, takencoords):
                    tempstate[key] = newcoords
                    states.append(tempstate)
                    #print("Changed:", key, " ", state[key], "to", newcoords )

        else:
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
                    states += [tempstate]
                    #if key == "Y":
                    #    print("Cond fwd")
                    #    print(tempstate)
                    #    pp.pprint(states)
                    #pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsfwd )


                if coordsavailable(newcoordsback, takencoords):
                    #print(newcoordsback
                    tempstate2[key] = newcoordsback
                    states.append(tempstate2)

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
                    states += [tempstate]
                    if key == "Y":
                        print("Cond front")
                        pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsfwd )

                if coordsavailable(newcoordsback, takencoords):
                    #print(newcoordsback)
                    tempstate2[key] = newcoordsback
                    states.append(tempstate2)
                    #if key == "Y":
                    #    print("Cond Back")
                    #    pp.pprint(states)
                    #print("Changed:", key, " ", state[key], "to", newcoordsback )
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
    #pp.pprint(states)
    return states

#reatenewstates(teststate)

stateid = 0
graph = {}
nodes = []
goal = [(2,4), (2,5)]

def graphsearch(state):
    frontier = createnewstates(state)
    explored = [state]
    while 1:
        #print(len(explored))
        if len(frontier) == 0:
            print("Frontier exhaused")
            #print("Final set length:", len(explored))
            return False
        #print(len(frontier))
        leaf = frontier.pop()
        

        '''
        mat = [[" " for i in range(6)] for k in range(6)]
        for key in leaf:
            for j in leaf[key]:
                mat[j[0]][j[1]] = key
        mat = np.matrix(mat)
        print(mat)
        '''

        #pp.pprint(leaf)



        #print(leaf["Y"])
        #if leaf["R"] == goal:
            #print("Solution Found!")
            #return True
        explored.append(leaf)
        newfrontier = createnewstates(leaf)
        for i in newfrontier:
            if i not in explored:
                frontier.append(i)


def treesearch(state):
    frontier = createnewstates(state)
    while 1:
        if len(frontier) == 0:
            return False
        leaf = frontier.pop()
        if leaf["R"] == goal:
            return leaf
        frontier += createnewstates(leaf)



graphsearch(initialstate)
#print(board)
#createnewstates(teststate4)

#graphsearch(initialstate)
