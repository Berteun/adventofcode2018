import sys

def read_input(input_file):
    f = open(input_file)
    area = [list(l.strip()) for l in f]
    return area

def print_area(area):
    for l in area:
        sys.stdout.write(''.join(l) + '\n')
    print("")

def get_str(area):
    return ''.join(''.join(l) for l in area)

def neighbours(area, y, x):
    nb = []
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy == 0 and dx == 0:
                continue
            if 0 <= y + dy and 0 <= x + dx:
                try:
                    nb.append(area[y + dy][x + dx])
                except IndexError:
                    pass
    return nb

def evolve(area):
    new_area = [l[:] for l in area]
    for y in range(len(area)):
        for x in range(len(area[y])):
            nb = neighbours(area, y, x)
            trees = sum(1 for n in nb if n == '|')
            lumber = sum(1 for n in nb if n == '#')
            opena = sum(1 for n in nb if n == '.')

            current = area[y][x]

            if current == '.':
                if trees >= 3:
                    new = '|'
                else:
                    new = '.'
            elif current == '|':
                if lumber >= 3:
                    new = '#'
                else:
                    new = '|'
            elif current == '#':
                if lumber >= 1 and trees >= 1:
                    new = '#'
                else:
                    new = '.'

            new_area[y][x] = new
    return new_area

def run(inp):
    area = read_input(input_file)
    seen = {}
    for cycle in range(1,1000000000 + 1):
        area = evolve(area)
        #print_area(area)
        ss = get_str(area)
        if ss in seen:
            length = cycle - seen[ss]
            offset = (1000000000 - seen[ss]) % length
            number = (offset + seen[ss])
            for k in seen:
                if seen[k] == number:
                    solution = k
                    n_lumber = sum(1 for x in solution if x == '#')
                    n_tree = sum(1 for x in solution if x == '|')
                    print(n_tree*n_lumber)
                    return
        else:
            if cycle == 10:
                n_lumber = sum(1 for x in ss if x == '#')
                n_tree = sum(1 for x in ss if x == '|')
                print(n_tree*n_lumber)

            seen[ss] = cycle

if __name__ == '__main__':
    input_file = "input.txt" if not sys.argv[1:] else sys.argv[1]
    run(input_file)
