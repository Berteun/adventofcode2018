import sys
import bisect
from collections import Counter

def read_input():
    for l in open("input.txt"):
        x, y = [int(c) for c in l.split(", ")]
        yield x, y

def get_boundaries(coordinates):
    lo_x, lo_y = 1000, 1000
    hi_x, hi_y = 0, 0

    for (x, y) in coordinates:
        lo_x, lo_y = min(lo_x, x), min(lo_y, y)
        hi_x, hi_y = max(hi_x, x), max(hi_y, y)
    return lo_x, lo_y, hi_x, hi_y

def make_grid(boundaries):
    lo_x, lo_y, hi_x, hi_y = boundaries
    return [[None] * (hi_y - lo_y + 1) for _ in range(hi_x - lo_x + 1)]

def find_closest(xc, yc, coordinates):
    point = None
    min_dist = 2000
    for i, (x, y) in enumerate(coordinates):
        dist = abs(x - xc) + abs(y - yc)
        if dist == min_dist:
            point = None
        if dist < min_dist:
            min_dist = dist
            point = i

    return point

def fill_grid(coordinates, grid, boundaries, func):
    lo_x, lo_y, hi_x, hi_y = boundaries
    for x in range(lo_x, hi_x + 1):
        for y in range(lo_y, hi_y + 1):
            grid[x - lo_x][y - lo_y] = func(x, y, coordinates)

def count_areas(grid, exclude=[]):
    count = Counter()
    for row in grid:
        count.update(row)

    for area in exclude:
        del count[area]

    return count

def get_infinite_areas(grid):
    return set(grid[0]) | set(grid[-1]) | set(row[0] for row in grid) | set(row[-1] for row in grid)


def in_region(xc, yc, coordinates, max_dist=10000):
    return sum(abs(x - xc) + abs(y - yc) for (x,y) in coordinates) < max_dist

def run():
    coordinates = list(read_input())
    boundaries = get_boundaries(coordinates)
    grid = make_grid(boundaries)

    # Part 1
    fill_grid(coordinates, grid, boundaries, find_closest)
    infinite = get_infinite_areas(grid)
    count = count_areas(grid, infinite)
    print count.most_common(1)[0][1]

    # Part 2
    fill_grid(coordinates, grid, boundaries, in_region)
    count = count_areas(grid)
    print(count[True])

if __name__ == '__main__':
    run()
