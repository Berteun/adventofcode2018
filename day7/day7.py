from collections import defaultdict

def read_input():
    return [(l[5], l[36]) for l in open("input.txt")]

def build_graph(steps):
    graph = defaultdict(set)

    for (fst, snd) in steps:
        graph[fst].add(snd)

    return graph

def get_indegrees(graph):
    in_degrees = defaultdict(int)
    for n,l in graph.items():
        in_degrees[n] += 0
        for nb in l:
            in_degrees[nb] += 1

    return in_degrees

def find_order(graph):
    in_degrees = get_indegrees(graph)
    order = []
    while in_degrees:
        node = min(n for (n,d) in in_degrees.items() if d == 0)
        order.append(node)
        for nbs in graph[node]:
            in_degrees[nbs] -= 1
        del in_degrees[node]

    return order

def assign_work(workers, in_degrees, n_workers, offset):
    nodes = sorted(n for (n,d) in in_degrees.items() if d == 0)
    for i in range(min(len(nodes), n_workers - len(workers))):
        node = nodes.pop(0)
        workers.append([node, offset + ord(node) - 64])
        del in_degrees[node]

def get_progress(workers, in_degrees):
    if not workers:
        return 0, set()

    done = set()
    time_advanced = min(w[1] for w in workers)
    for w in workers:
        w[1] -= time_advanced
        if w[1] == 0:
            done.add(w[0])

    workers[:] = [w for w in workers if w[1] != 0]
    return time_advanced, done

def update(completed, not_done, in_degrees, graph):
    not_done -= completed
    for n in completed:
        for nb in graph[n]:
            in_degrees[nb] -= 1

def find_time(graph, n_workers, offset):
    in_degrees = get_indegrees(graph)
    workers = []
    time = 0

    not_done = set(in_degrees)
    while not_done:
        time_advanced, completed = get_progress(workers, in_degrees)
        update(completed, not_done, in_degrees, graph)
        assign_work(workers, in_degrees, n_workers, offset)
        time += time_advanced

    return time

def run():
    steps = read_input()
    #steps = [('C', 'A'), ('C', 'F'), ('A', 'B'), ('A', 'D'), ('B', 'E'), ('D', 'E'), ('F', 'E')]
    graph = build_graph(steps)
    order = find_order(graph)
    print ''.join(order)
    time = find_time(graph, n_workers=5, offset=60)
    print time

if __name__ == '__main__':
    run()
