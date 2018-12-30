import sys
from z3 import *

def read_input(input_name):
    f = open(input_name)
    bots = []
    for l in f:
        pos_str,radius_str=l[5:].split(">, r=")
        bots.append((int(radius_str), tuple(int(x) for x in pos_str.split(","))))
    return bots

def part1(bots):
    maxr,maxp = max(bots)
    return sum(sum(abs(c1 - c2) for (c1,c2) in zip(pos,maxp)) < maxr for _,pos in bots)

def part2(bots):
    def abs(c):
        return If(c < 0, -c, c)

    o = Optimize()

    cx, cy, cz = Int('x'), Int('y'), Int('z')
    in_range_of = list(map(Int, ['is_in_range_of_{}'.format(i) for i in range(len(bots))]))

    count = Int('count')
    dist_from_zero = Int('dist_from_zero')

    for i, (radius, (ox, oy, oz)) in enumerate(bots):
        o.add(in_range_of[i] == If(abs(cx - ox) + abs(cy - oy) + abs(cz - oz) <= radius, 1, 0))

    o.add(count == sum(in_range_of))
    o.add(dist_from_zero == abs(cx) + abs(cy) + abs(cz))

    h1 = o.maximize(count)
    h2 = o.minimize(dist_from_zero)
    assert o.check()
    print(o.lower(h2))

def run(input_name):
    bots = read_input(input_name)
    print(part1(bots))
    part2(bots)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_name = "input.txt"
    else:
        input_name = argv[1]
    run(input_name)
