import sys
from collections import defaultdict

def evaluate(regex):
    grid = defaultdict(lambda: '#')
    coor = (0, 0)
    
    grid[coor] = 'X'
    stack = [coor]

    for token in regex:
        x,y = coor
        if token in ('^', '$'):
            continue
        if token == '(':
            stack.append(coor)
        elif token == '|':
            coor = stack[-1]
        elif token == ')':
            stack.pop()
        elif token == 'N':
            grid[(x,y-1)] = '-'
            grid[(x,y-2)] = '.'
            coor = (x,y-2)
        elif token == 'S':
            grid[(x,y+1)] = '-'
            grid[(x,y+2)] = '.'
            coor = (x,y+2)
        elif token == 'W':
            grid[(x-1,y)] = '|'
            grid[(x-2,y)] = '.'
            coor = (x-2,y)
        elif token == 'E':
            grid[(x+1,y)] = '|'
            grid[(x+2,y)] = '.'
            coor = (x+2,y)
    return grid

def print_grid(grid):
    minx,maxx,miny,maxy = 0,0,0,0
    for (x,y) in grid:
        minx = min(minx,x)
        miny = min(miny,y)
        maxx = max(maxx,x)
        maxy = max(maxy,y)
    
    for y in range(miny-1,maxy+2):
        for x in range(minx-1,maxx+2):
            sys.stdout.write(grid[(x,y)])
        sys.stdout.write("\n")

def find_furthest(grid):
    queue = [((0,0), 0)]
    seen  = set([(0,0)])
    maxd = 0
    onek = 0
    while queue:
        (x,y),d = queue.pop(0)
        if d >= 1000:
            onek += 1
        if grid[(x-1,y)] == '|' and grid[(x-2,y)] == '.':
            if (x-2,y) not in seen:
                queue.append(((x-2,y), d+1))
            seen.add((x-2,y))
        if grid[(x+1,y)] == '|' and grid[(x+2,y)] == '.':
            if (x+2,y) not in seen:
                queue.append(((x+2,y), d+1))
            seen.add((x+2,y))
        if grid[(x,y-1)] == '-' and grid[(x,y-2)] == '.':
            if (x,y-2) not in seen:
                queue.append(((x,y-2), d+1))
            seen.add((x,y-2))
        if grid[(x,y+1)] == '-' and grid[(x,y+2)] == '.':
            if (x,y+2) not in seen:
                queue.append(((x,y+2), d+1))
            seen.add((x,y+2))
        maxd = max(d,maxd)
    return maxd,onek
def read_input():
    return open("input.txt").readline().rstrip()

def run():
    regex = read_input()
    #regex = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
    grid = evaluate(regex)
    #print_grid(grid)
    print(find_furthest(grid))

if __name__ == '__main__':
    run()
