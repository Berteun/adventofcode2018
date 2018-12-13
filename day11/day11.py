def grid_sum(grid, sq, x, y):
    return sum(sum(grid[y][x:x+sq]) for y in range(y, y + sq))

def run():
    grid = [[0] * 300 for _ in range(300)]
    serial = 2187
    for y in range(300):
        for x in range(300):
            grid[y][x] = (((((x + 10) * y + serial)) * (x + 10) % 1000)/ 100) - 5
    
    max = 0
    sq_size = None
    bx, by = None, None

    for y in range(299):
        for x in range(299):
            for sq in range(1, min(300-y,300-x)):
                s = grid_sum(grid, sq, x, y)
                if s > max:
                    max = s
                    sq_size = sq
                    bx, by = x, y

    print "{},{},{}".format(bx,by,sq_size)
    print grid_sum(grid, bx, by)

if __name__ == '__main__':
    run()
