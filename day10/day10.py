import re

def read_input():
    coords = []
    for l in open("input.txt"):
        x,y, vx,vy = re.match("position=<(.*?),(.*?)> velocity=<(.*?),(.*?)>", l).group(1,2,3,4)
        coords.append([int(x), int(y), int(vx), int(vy)])
    return coords

def bbox(coords):
    xl = [x for (x,y,_,_) in coords]
    yl = [y for (x,y,_,_) in coords]

    return min(xl),min(yl),max(xl),max(yl)

def area(bb):
    return (bb[2]-bb[0])*(bb[3]-bb[1])

def evolve(coords):
    a = area(bbox(coords))
    b = a + 1

    n = 10000 
    for i in range(len(coords)):
        coords[i][0] += n*coords[i][2]
        coords[i][1] += n*coords[i][3]

    while a <= b:
        b = a
        for i in range(len(coords)):
            coords[i][0] += coords[i][2]
            coords[i][1] += coords[i][3]

        a = area(bbox(coords))
        n += 1

    print n - 1
    for i in range(len(coords)):
        coords[i][0] -= coords[i][2]
        coords[i][1] -= coords[i][3]

def print_coords(coords):
    bb =  bbox(coords)
    grid = [['.'] * (bb[2] - bb[0] + 1) for _ in range(bb[3] - bb[1] + 1)]
    for (x,y,_,_) in coords:
        grid[y - bb[1]][x - bb[0]] = '#'

    for row in grid:
        print ''.join(row)

def run():
    coords = read_input()
    evolve(coords)
    print_coords(coords)

if __name__ == '__main__':
    run()
