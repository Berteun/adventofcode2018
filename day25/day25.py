import re
import sys
from collections import defaultdict

def read_input(input_file):
    coordinates = []
    f = open(input_file)
    for l in f:
        w,x,y,z = l.strip().split(",")
        coordinates.append((int(w),int(x),int(y),int(z)))
    return coordinates

def dist(c1, c2):
    return sum(abs(a-b) for a,b in zip(c1,c2))

def find_constellations(coordinates):
    graph = defaultdict(list)

    for i,c1 in enumerate(coordinates):
        for j in range(i + 1, len(coordinates)):
            c2 = coordinates[j]
            if dist(c1, c2) <= 3:
                graph[c1].append(c2)
                graph[c2].append(c1)

    count = 0
    coordinates = set(coordinates)
    while coordinates:
        count += 1
        queue = [coordinates.pop()]
        while queue:
            nb = queue.pop(0)
            if nb in graph:
                queue.extend(graph[nb])
                del graph[nb]
            coordinates.discard(nb)

    return count

def run(input_file):
    coordinates = read_input(input_file)
    result = find_constellations(coordinates)
    print(result)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_file = "input.txt"
    else:
        input_file = sys.argv[1]
    run(input_file)
