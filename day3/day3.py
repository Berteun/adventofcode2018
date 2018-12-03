import re

def extract(line):
    return [int(m) for m in re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line).group(1,2,3,4,5)]

def read_input(input_):
    f = open(input_)

    claims = {}
    for line in f:
        claim_id, x,y, w,h = extract(line)
        claims[claim_id] = (x, y, w, h)
    
    return claims

def fill_fabric(claims):
    length = 0
    for x, y, w, h in claims.values():
        length = max(length, x + w, y + h)

    fabric = [[0 for _ in range(length)] for _ in range(length)]

    for x, y, w, h in claims.values():
        for m in range(w):
            for n in range(h):
                fabric[x + m][y + n] += 1
            
    return fabric

def part1(claims, fabric):
    return sum(1 for row in fabric for square in row if square > 1)

def part2(claims, fabric):
    for claim_id in claims:
        x, y, w, h = claims[claim_id]
        counts = [fabric[x + m][y + n] == 1 for m in range(w) for n in range(h)]
        if all(counts):
            return claim_id

claims = read_input("input.txt")
fabric = fill_fabric(claims)

print(part1(claims, fabric))
print(part2(claims, fabric))
