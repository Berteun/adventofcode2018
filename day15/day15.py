import sys
import time

colors = {
    '#': '\x1b[1;33;40m#\x1b[0m', 
    '.': '\x1b[0;37;40m.\x1b[0m',
    'G': '\x1b[1;31;40mG\x1b[0m', 
    'E': '\x1b[1;32;40mE\x1b[0m',
    '@': '\x1b[0;34;40m@\x1b[0m',
    '?': '\x1b[0;34;40m?\x1b[0m',
    '+': '\x1b[1;34;40m+\x1b[0m',
    '!': '\x1b[1;34;40m!\x1b[0m',
    'X': '\x1b[0;37;40mX\x1b[0m',
}

HP_REDUCE = {
        'E' : 3,
        'G' : 12,
}


PRINT_BOARDS = False

def walk(board, filter=None):
    for y in range(len(board)):
        for x in range(len(board[y])): 
            if filter is None or board[y][x] in filter:
                yield (y,x,board[y][x])

def print_board(board):
    if not PRINT_BOARDS:
        return
    for row in board:
        for cell in row:
            sys.stdout.write(colors[cell])
        sys.stdout.write("\n")

def print_board_attack(board, hitpoints, unit, target):
    if not PRINT_BOARDS:
        return
    uy,ux = unit
    ty,tx = target
    for (y,x,cell) in walk(board):
        if (y,x) == unit:
            sys.stdout.write('\x1b[1;37;42m{}\x1b[0m'.format(board[uy][ux]))
            #sys.stdout.write(colors[cell])
        elif (y,x) == target:
            sys.stdout.write('\x1b[1;37;41m{}\x1b[0m'.format(board[ty][tx]))
            #sys.stdout.write(colors[cell])
        else:
            sys.stdout.write(colors[cell])
        if (y == ty and x == len(board[y]) - 1):
            hp = hitpoints[(ty,tx)]
            sys.stdout.write(" HP {} -> {}".format(hp, hp - HP_REDUCE[board[ty][tx]]))
        if (x == len(board[y]) - 1):
            sys.stdout.write("\n")
    #time.sleep(0.2)

def print_reachable_board(board, start, range_list, reachable):
    if not PRINT_BOARDS:
        return
    assert board[start[0]][start[1]] in ('E','G')
    if reachable:
        shortest = min(len(p) for p in reachable.values())
        chosen = min(pos for pos in reachable if len(reachable[pos]) == shortest)
    else:
        chosen = None
        shortest = None
    for (y,x,cell) in walk(board):
        if (y,x) in reachable:
            assert (y,x) in range_list, "Inconsistency in reachable targets detected"
            assert board[y][x] == '.', "Invalid cell marked reachable"
            if (y,x) == chosen:
                sys.stdout.write(colors["+"])
            elif len(reachable[(y,x)]) == shortest:
                sys.stdout.write(colors["!"])
            else:
                sys.stdout.write(colors["@"])
        elif (y,x) in range_list:
            assert board[y][x] == '.', "Invalid cell marked in range"
            sys.stdout.write(colors["?"])
        elif (y,x) == start:
            sys.stdout.write(colors["X"])
        else:
            sys.stdout.write(colors[cell])
        if (x == len(board[y]) - 1):
            sys.stdout.write("\n")
    #time.sleep(0.2)

def read_input():
    return [list(l.strip('\n')) for l in open("input.txt")]

def get_units(board):
    return list(walk(board, ('E','G')))

def get_neighbours(board, y, x):
    neighbours = []
    for (dy, dx) in (-1, 0), (0, -1), (0, 1), (1, 0):
        cy, cx = y + dy, x + dx
        if 0 <= cy < len(board) and 0 <= cx < len(board[y]):
            neighbours.append((cy, cx))
    return neighbours

def get_ranges(board, target):
    enemies = walk(board, target)
    ranges = []
    for (y, x, _) in enemies:
        nbs = get_neighbours(board, y, x)
        for nb_y, nb_x in nbs:
            if board[nb_y][nb_x] == '.':
                ranges.append((nb_y,nb_x))
    ranges.sort()
    return ranges

def get_reachable(board, start, goals):
    seen = set()
    queue = [(start, [])]
    reachable = dict()
    while queue:
        ((y,x), path) = queue.pop(0)
        for nb in get_neighbours(board, y, x):
            if nb in seen:
                continue
            if board[nb[0]][nb[1]] != '.':
                continue
            seen.add(nb)
            queue.append((nb, path + [nb]))
            if nb in goals:
                assert nb not in reachable
                reachable[nb] = path + [nb]
    return reachable

def get_step(board, (y,x), range_list, reachable):
    shortest = min(len(p) for p in reachable.values())
    chosen = min(pos for pos in reachable if len(reachable[pos]) == shortest)
    if reachable[chosen]:
        return reachable[chosen][0]
    else:
        return None

def evolve(board,hitpoints):
    combat_continues = True
    round_no = 0
    while combat_continues:
        print "Round {} starts!".format(round_no + 1)
        units = get_units(board)
        deaths = set()
        for (y, x, u) in units:
            if (y,x) in deaths:
                continue

            # Enemies
            enemy = 'G' if u == 'E' else 'E'
            for n_y,n_x in get_neighbours(board, y, x):
                if board[n_y][n_x] == enemy:
                    break
            else:
                if not len(list(walk(board, enemy))):
                    combat_continues = False
                    break

                range_list = get_ranges(board, enemy)

                if (y,x) not in range_list:
                    reachable = get_reachable(board, (y,x), range_list)
                    print_reachable_board(board, (y,x), range_list, reachable)

                    if reachable:
                        step = get_step(board, (y,x), range_list, reachable)
                        #print (y,x), "->", step

                        if step is not None:
                            ny, nx = step
                            board[ny][nx] = board[y][x]
                            board[y][x] = '.'
                            hitpoints[(ny,nx)] = hitpoints[(y,x)]
                            del hitpoints[(y,x)]
                            y, x = ny, nx
            
            # Enemies
            enemy = 'G' if u == 'E' else 'E'
            enemies = [(n_y,n_x) for n_y,n_x in get_neighbours(board, y, x) if board[n_y][n_x] == enemy]
            if enemies:
                enemies.sort(key=lambda (y,x) : (hitpoints[(y,x)], y, x))
                target = enemies[0]
                ty,tx = target
                print_board_attack(board, hitpoints, (y,x), (ty,tx))
                hitpoints[target] -= HP_REDUCE[enemy] 
                if hitpoints[target] <= 0:
                    deaths.add(target)
                    board[ty][tx] = '.'
                    del hitpoints[target]

        if combat_continues:
            round_no += 1 
    
    print "Rounds completed:", round_no
    print "Units left:", len(hitpoints)
    print "Points:", sum(hitpoints.values()) * round_no

def init_hp(board):
    hitpoints = {}
    for (y,x,unit) in walk(board, ('E','G')):
        hitpoints[(y,x)] = 200
    return hitpoints

def run():
    board = read_input()
    hitpoints = init_hp(board)
    print_board(board)
    evolve(board,hitpoints)

if __name__ == '__main__':
    run()
