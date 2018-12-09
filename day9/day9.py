from collections import defaultdict, deque
def read_input():
    f = open("input.txt")
    return [int(t) for (i,t) in enumerate(f.readline().split()) if i in (0, 6)]

def play_game(players, rounds):
    scores = defaultdict(int)
    marbles = deque([0])

    for cur_round in range(1, rounds + 1):
        if (cur_round % 23 == 0):
            marbles.rotate(7)
            scores[cur_round % players] += cur_round + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(cur_round)

        #print "[{}/{}]".format(cur_round, cur_round % players), "({})".format(marbles[0]), marbles

    print max(scores.values())

def run():
    players, rounds = read_input()
    play_game(players, rounds)
    play_game(players, rounds*100)

if __name__ == '__main__':
    run()
