##Rules
#Two 40 quart cans, both full, one empty 5 quart, one empty 4 quart
#Transfer milk between cans without spilling until there are two quarts in each of the smaller cans
#state = [40 quart, 40 quart, 5 quart, 4 quart]
#goal state[2] == state[4] == 2
#can only empty one can or fully fill one can


#Returns possible states
limits = [40, 40, 5, 4]
start = [40, 40, 0, 0]


def expandfrontier(state):
    states = []
    newstate = list(state)
    newstate2 = list(state)
    for i in range(0,len(state)):
        if state[i] == limits[i]:
            #i can only fill
            for k in range(0, len(state)):
                if i == k:
                    #can cant fill itself
                    continue

                if state[k] == limits[k]:
                    #can't be filled
                    continue

                else:
                    #now the fun begins
                    maxpour = limits[k] - state[k]
                    possiblepour = state[k]
                    if maxpour < possiblepour:
                        pour = maxpour
                    else:
                        pour = possiblepour

                    newstate[i] = state[i] - pour
                    newstate[k] = state[k] + pour
                    states.append(list(newstate))
                    newstate = list(state)


        if state[i] == 0:
            #i can only be filled
            for k in range(0, len(state)):
                if i == k:
                    continue

                if state[k] == 0:
                    #k cant fill
                    continue

                else:
                    maxfill = limits[i] - state[i]
                    possiblefillk = state[k]
                    if maxfill < possiblefillk:
                        fill = maxfill
                        newstate[k] = newstate[k] - fill
                        newstate[i] = newstate[i] + fill
                        states.append(list(newstate))
                        newstate = list(state)
                    else:
                        fill = possiblefillk
                        newstate[k] =  newstate[k] - fill
                        newstate[i] = newstate[i] + fill
                        states.append(list(newstate))
                        newstate = list(state)

        else:
            #I can be filled or fill
            for k in range(0, len(state)):

                if i == k:
                    continue

                if state[k] < limits[k]:
                    #i can fill k
                    maxfill = limits[k] - state[k]
                    possiblefilli = state[i]
                    if possiblefilli > maxfill:
                        fill = maxfill
                    else:
                        fill = possiblefilli
                    newstate[i] = newstate[i] - fill
                    newstate[k] = newstate[k] + fill
                    states.append(list(newstate))
                    newstate = list(state)

                if state[i] < limits[i]:
                    #k can also fill i
                    maxfill = limits[i] - state[i]
                    possiblefillk = state[k]
                    if possiblefillk > maxfill:
                        fill = maxfill
                    else:
                        fill = possiblefillk
                    newstate[i] = newstate[i] + fill
                    newstate[k] = newstate[k] - fill
                    states.append(list(newstate))
                    newstate = list(state)

    return states

#print(expandfrontier(start))

def graphsearch(state):

    frontier = expandfrontier(state)
    explored = [state]
    while 1:

        if len(frontier) == 0:
            print("Frontier exhaused")
            print("Final set length:", len(explored))
            return False

        leaf = frontier.pop()
        print(leaf)
        #Solution found
        if state[2] == state[3] == 2:
            print("Solution Found!")
            #return True
        explored.append(leaf)
        newfrontier = expandfrontier(leaf)
        for i in newfrontier:
            if i not in explored:
                frontier.append(i)

graphsearch(start)
