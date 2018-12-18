import time
import sys
from collections import defaultdict

def read_input(input_file):
    f = open(input_file)
    section = defaultdict(lambda : '.')

    miny, maxy = None, None
    minx, maxx = None, None

    for line in f:
        left,right = line.split(', ')
        cl = left[0]
        cr = right[0]

        cc = int(left[2:])
        cfrom, cto = tuple(int(n) for n in right[2:].split('..'))

        if cl == 'y':
            y = cc
            if miny is None or y < miny:
                miny = y
            if maxy is None or y > maxy:
                maxy = y

            for x in range(cfrom, cto + 1):
                section[(y,x)] = '#'
                if minx is None or x < minx:
                    minx = x
                if maxx is None or x > maxx:
                    maxx = x
        else:
            x = cc
            if minx is None or x < minx:
                minx = x
            if maxx is None or x > maxx:
                maxx = x
            for y in range(cfrom, cto + 1):
                section[(y,x)] = '#'
                if miny is None or y < miny:
                    miny = y
                if maxy is None or y > maxy:
                    maxy = y

    section[(0,500)] = '|'
    return (miny,maxy,minx,maxx), section

def print_section(boundaries, section,really=False):
    if not really:
        return
    miny,maxy,minx,maxx = boundaries

    for y in range(miny, maxy + 1):
        for x in range(minx - 1, maxx + 2):
            sys.stdout.write(section[(y,x)])
        print("")
    print("")

def flood_fill_right(boundaries, section, start):
    y,x = start
    print_section(boundaries, section)
    if section[(y+1,x)] == '#' or section[(y+1,x)] == '~':
        right = section[(y,x+1)]
        if right == '.' or (right == '|' and section[(y+1,x+1)] in ('#','~')):
            section[(y,x+1)] = '|'
            return flood_fill_right(boundaries, section, (y,x+1))
        elif right == '#':
            return "stable"
        elif right == '|':
            return "overflow"
    return "overflow"

def flood_fill_left(boundaries, section, start):
    y,x = start
    print_section(boundaries, section)
    if section[(y+1,x)] == '#' or section[(y+1,x)] == '~':
        left = section[(y,x-1)]
        if left == '.' or (left == '|' and section[(y+1,x-1)] in ('#','~')):
            section[(y,x-1)] = '|'
            return flood_fill_left(boundaries, section, (y,x-1))
        elif left == '#':
            return "stable"
        elif left == '|':
            return "overflow"
    return "overflow"

def flood_fill(boundaries, section, start):
    y,x = start
    miny,maxy,minx,maxx = boundaries
    if (y > maxy):
        return "overflow"
    print_section(boundaries, section)
    if section[(y+1,x)] == '#' or section[(y+1,x)] == '~':
        if section[(y,x-1)] != '.' and section[(y,x+1)] != '.':
            if section[(y,x-1)] == '#' and section[(y,x+1)] == '#':
                result = 'stable'
            else:
                result = "overflow"
        else:
            result = "stable"
        if section[(y,x-1)] == '.':
            section[(y,x-1)] = '|'
            if flood_fill_left(boundaries, section, (y,x-1)) == "overflow":
                result = "overflow"
        if section[(y,x+1)] == '.':
            section[(y,x+1)] = '|'
            if flood_fill_right(boundaries, section, (y,x+1)) == "overflow":
                result = "overflow"
        if result == "stable":
            lx = x - 1
            while section[(y,lx)] == '|':
                section[(y,lx)] = '~'
                lx -= 1
            rx = x + 1
            while section[(y,rx)] == '|':
                section[(y,rx)] = '~'
                rx += 1
            section[(y,x)] = '~'
        return result
    elif section[(y+1,x)] == '.':
        section[(y+1,x)] = '|'
        flood_fill(boundaries, section, (y+1,x))
    return "overflow"

def evolve(boundaries, section):
    for cycle in range(1000):
        for (y,x),k in list(section.items()):
            if k == '|':
                flood_fill(boundaries, section, (y,x)) 
    print_section(boundaries,section,True)

def count_water(boundaries, section):
    miny,maxy,minx,maxx = boundaries
    count,count2 = 0,0
    for (y,x),k in section.items():
        if miny <= y <= maxy and k in ('|','~'):
            count += 1
        if miny <= y <= maxy and k in ('~'):
            count2 += 1
    return count,count2

def run(inp):
    boundaries, section = read_input(input_file)
    evolve(boundaries, section)
    print(count_water(boundaries,section))

if __name__ == '__main__':
    input_file = "input.txt" if not sys.argv[1:] else sys.argv[1]
    run(input_file)
