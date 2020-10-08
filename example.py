import json
from UCS import ucs

# Reads Json file and loads it into cities as a dictionary.
filename = 'UK_cities.json'
with open(filename, 'r') as f:
    cities = json.load(f)

# Runs th ucs function above with start: 'london', goal: 'aberdeen' and cities: cities
# Prints the return value('failure' or solution)

cities, total_distance = ucs('london', 'aberdeen', cities)
if not cities == -1:
    print("Solution: {}, total distance: {}".format(' -> '.join([city for city in cities]), total_distance))
else:
    print("UCS failed to find the shortest distance between given cities in {}".format(filename))
