import sys

def read_input():
    f = open("input.txt")
    grid = [list(l.strip('\n')) for l in f]
    carts = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in ('^', 'v'):
                carts.append((y, x, grid[y][x], 0))
                grid[y][x] = '|'
            if grid[y][x] in ('<', '>'):
                carts.append((y, x, grid[y][x], 0))
                grid[y][x] = '-'
    return grid, carts

def print_state(track, carts):
    c = {}
    for (y, x, d, s) in carts:
        c[(y,x)] = d
    for y in range(len(track)):
        for x in range(len(track[y])):
            if (y,x) in c:
                sys.stdout.write(c[(y,x)])
            else:
                sys.stdout.write(track[y][x])
        sys.stdout.write("\n")
    sys.stdout.write("\n")

def evaluate(track, carts):
    adjust = {
            '^' : (-1, 0),
            '<' : ( 0,-1),
            '>' : ( 0, 1),
            'v' : ( 1, 0),
    }

    while True:
        carts.sort()
        print carts
        new_carts = []
        old_locations = set((y,x) for (y,x,_,_) in carts)
        new_locations = set()
        crashed = set()
        for (y, x, direction, state) in carts:
            if (y,x) in crashed:
                continue
            new_y = y + adjust[direction][0]
            new_x = x + adjust[direction][1]
            new_state = state
            new_direction = direction
            if track[new_y][new_x] == '\\':
                new_direction = {
                    '^' : '<',
                    '<' : '^',
                    '>' : 'v',
                    'v' : '>',
                }[direction]
            elif track[new_y][new_x] == '/':
                new_direction = {
                    '^' : '>',
                    '<' : 'v',
                    '>' : '^',
                    'v' : '<',
                }[direction]
            elif track[new_y][new_x] == '+':
                new_direction = {
                    ('^',0) : ('<'),
                    ('^',1) : ('^'),
                    ('^',2) : ('>'),
                    ('<',0) : ('v'),
                    ('<',1) : ('<'),
                    ('<',2) : ('^'),
                    ('>',0) : ('^'),
                    ('>',1) : ('>'),
                    ('>',2) : ('v'),
                    ('v',0) : ('>'),
                    ('v',1) : ('v'),
                    ('v',2) : ('<'),
                }[direction,state]
                new_state = (state + 1) % 3

            if (new_y, new_x) in old_locations:
                crashed.add((new_y, new_x))
                old_locations.remove((new_y,new_x))
            elif (new_y, new_x) in new_locations:
                new_carts = [(cy,cx,cd,cs) for (cy,cx,cd,cs) in new_carts if (cy,cx) != (new_y,new_x)] 
                new_locations.remove((new_y,new_x))
            else:
                old_locations.remove((y,x))
                new_locations.add((new_y, new_x))
                new_carts.append((new_y, new_x, new_direction, new_state))

        carts = new_carts
        if len(carts) == 1:
            print "{},{}".format(carts[0][1],carts[0][0])
            return
        #print_state(track, carts)

def run():
    track, carts = read_input()
    evaluate(track, carts)

if __name__ == '__main__':
    run()
