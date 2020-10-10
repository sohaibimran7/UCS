def ucs(start, goal, cities):
    """
    Given a start location, goal location and a dictionary of cities, finds the shortest route from start to goal.


    Iterates through the keys to find key corresponding to the city and iterates through its values in the following manner:

    If the value is:

                    - Does nothing                                   - Removes the corresponding node from frontier,
                  /                                               /    appends to frontier, sorts and prints frontier
               Y /                                             Y /
                /                                               /
     Explored?                           - Has lower path cost
                \                      /                        \
               N \                  Y /                        N \
                  \                  /                            \
                    - In frontier?                                  - Do nothing
                                     \
                                    N \
                                       \
                                         - Appends to frontier, sorts and prints frontier


    If city not found in keys then iterates through all values of all keys to find city in values instead.


    Args:
        start: The start city as string.
        goal: The goal city as string.
        cities: The json object containing the cities and their distances to each other.
    Returns:
        cities: list of cities in shortest path from start of goal as list of strings.
        total distance: the total distance of shortest path as int.

        if start or goal not in cities, returns -1.

    """

    node = (start, 0, [start])
    frontier = [node]
    explored = []
    # print('frontier: {}\n'.format(frontier))
    # print('explored: {}\n'.format(explored))

    # Main loop runs until solution or 'failure' returned
    while True:

        # returns 'failed' if frontier is empty before node with shortest path cost is to be extracted from frontier.
        # This will happen if it fails to find a path to the goal state.
        if len(frontier) == 0:
            return -1, -1

        # Sorts the frontier by path cost and then pops the node, to extract out the node with the smallest path cost.
        # If that is the goal state, then the algorithm has successfully found the least cost path to goal state.
        frontier.sort(key=lambda a: a[1], reverse=True)
        # print('frontier: {}\n'.format(frontier))
        node = frontier.pop()
        if goal == node[0]:
            return node[2], node[1]

        # Append that node to explored and then start exploring the node.
        explored.append(node[0])
        # print('explored: {}\n'.format(explored))

        for city in cities:
            if city == node[0]:
                for child in cities[city]:
                    if child not in explored:
                        for i, v in enumerate(frontier):
                            if v[0] == child:
                                if cities[city][child]['weight'] + node[1] < v[1]:
                                    new_node = (child, cities[city][child]['weight'] + node[1], node[2] + [child])
                                    del frontier[i]
                                    frontier.insert(i, new_node)
                                break
                        else:
                            new_node = (child, cities[city][child]['weight'] + node[1], node[2] + [child])
                            frontier.append(new_node)

        # Same as above, but accounting for cities that may be in values and not in keys.
        # Iterate through the values(for all keys) to find value corresponding to the city and
        # runs the above tree algorithm on its key:
        else:
            for city in cities:
                for child in cities[city]:
                    if child == node[0]:
                        if city not in explored:
                            for i, v in enumerate(frontier):
                                if v[0] == city:
                                    if cities[city][child]['weight'] + node[1] < v[1]:
                                        new_node = (city, cities[city][child]['weight'] + node[1], node[2] + [city])
                                        del frontier[i]
                                        frontier.insert(i, new_node)
                                    break
                            else:
                                new_node = (city, cities[city][child]['weight'] + node[1], node[2] + [city])
                                frontier.append(new_node)
