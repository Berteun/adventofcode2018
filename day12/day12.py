from collections import defaultdict 

plants = defaultdict(lambda : '.')

init = "#.#.#..##.#....#.#.##..##.##..#..#...##....###..#......###.#..#.....#.###.#...#####.####...#####.#.#"

min_i = 0
max_i = len(init) - 1

for i, p in enumerate(init):
    plants[i] = p

rules = {
    "..#.." : ".",
    "#...#" : ".",
    ".#..." : "#",
    "#.##." : ".",
    "..#.#" : "#",
    "#.#.#" : ".",
    "###.." : "#",
    "###.#" : "#",
    "....." : ".",
    "....#" : ".",
    ".##.." : "#",
    "#####" : ".",
    "####." : ".",
    "..##." : ".",
    "##.#." : "#",
    ".#..#" : "#",
    "##..#" : ".",
    ".##.#" : ".",
    ".####" : "#",
    "..###" : ".",
    "...##" : "#",
    "#..##" : "#",
    "#...." : ".",
    "##.##" : ".",
    "#.#.." : ".",
    "##..." : ".",
    ".#.##" : "#",
    ".###." : "#",
    "...#." : ".",
    "#.###" : ".",
    "#..#." : "#",
    ".#.#." : ".",
}

for g in xrange(20):
    if plants[min_i] == '#':
        min_i -= 1
    if plants[max_i] == '#':
        max_i += 1

    new_plants = defaultdict(lambda : '.')
    for p in range(min_i, max_i + 1):
        str_ = ''.join(plants[i] for i in range(p - 2, p + 3))
        new_plants[p] = rules[str_]

    plants = new_plants


    s = ''.join(plants[i] for i in range(min_i, max_i + 1))
    if (g + 1 == 20):
        print sum(k for k,v in plants.items() if v == '#')
    
# After about 98 generations the pattern is fixed and just moves to the right
# increasing the value by 25 every generation; this boils down to:
print 991 + 25 *(50000000000)
