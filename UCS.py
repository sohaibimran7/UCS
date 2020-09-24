import json


def ucs(start, goal, cities):
    """Given a start location, goal location and a dictionary of cities, find the shortest route from start to goal."""
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
            return 'failure'

        # Sorts the frontier by path cost and then pops the node, to extract out the node with the smallest path cost.
        # If that is the goal state, then the algorithm has successfully found the least cost path to goal state.
        frontier.sort(key=lambda a: a[1], reverse=True)
        node = frontier.pop()
        # print('frontier: {}\n'.format(frontier))
        if goal == node[0]:
            return node[2], node[1]

        # Append that node to explored and then start exploring the node.
        explored.append(node[0])
        # print('explored: {}\n'.format(explored))

        """
        Iterate through the keys to find key corresponding to the city and iterates through its values in the following manner:
        
        If the value is:

                        - Do nothing                                   - Remove the corresponding node from frontier,
                      /                                               /    append to frontier, sort and print frontier
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
                                             - Append to frontier, sort and print frontier
        """
        for city in cities:
            if city == node[0]:
                for child in cities[city]:
                    if child not in explored:
                        found = False
                        for i, v in enumerate(frontier):
                            if v[0] == child:
                                found = True
                                if cities[city][child]['weight'] + node[1] < v[1]:
                                    frontier.remove(v)
                                    new_node = (child, cities[city][child]['weight'] + node[1], node[2] + [child])
                                    frontier.append(new_node)
                                    frontier.sort(key=lambda a: a[1], reverse=True)
                                    # print('frontier: {}\n'.format(frontier))
                                    break
                                break
                        if not found:
                            new_node = (child, cities[city][child]['weight'] + node[1], node[2] + [child])
                            frontier.append(new_node)
                            frontier.sort(key=lambda a: a[1], reverse=True)
                            # print('frontier: {}\n'.format(frontier))

            # Same as above, but accounting for cities that may be in values and not in keys.
            # Iterate through the values(for all keys) to find value corresponding to the city and
            # runs the above tree algorithm on its key:
            else:
                for child in cities[city]:
                    if child == node[0]:
                        if city not in explored:
                            found = False
                            for i, v in enumerate(frontier):
                                if v[0] == city:
                                    found = True
                                    if cities[city][child]['weight'] + node[1] < v[1]:
                                        frontier.remove(v)
                                        new_node = (city, cities[city][child]['weight'] + node[1], node[2] + [city])
                                        frontier.append(new_node)
                                        frontier.sort(key=lambda a: a[1], reverse=True)
                                        # print('frontier: {}\n'.format(frontier))
                                        break
                                    break
                            if not found:
                                new_node = (city, cities[city][child]['weight'] + node[1], node[2] + [city])
                                frontier.append(new_node)
                                frontier.sort(key=lambda a: a[1], reverse=True)
                                # print('frontier: {}\n'.format(frontier))


# Reads Json file and loads it into cities as a dictionary.
with open('UK_cities.json', 'r') as f:
    cities = json.load(f)

# Runs th ucs function above with start: 'london', goal: 'aberdeen' and cities: cities
# Prints the return value('failure' or solution)
cities, total_distance = ucs('london', 'aberdeen', cities)
print("Solution: {}, total distance {}".format(' -> '.join([city for city in cities]), total_distance))
