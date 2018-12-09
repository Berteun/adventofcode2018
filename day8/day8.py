from collections import defaultdict

class Tree:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def eval_metadata(self):
        return sum(self.metadata) + sum(c.eval_metadata() for c in self.children)

    def eval_tree(self):
        if not self.children:
            return sum(self.metadata)
        else:
            s = 0
            for md in self.metadata:
                try:
                    s += self.children[md - 1].eval_tree()
                except IndexError:
                    pass
            return s

def read_input():
    return [int(x) for x in open("input.txt").readline().split()]

def parse_tree(numbers, index):
    n_children = numbers[index]
    n_metadata = numbers[index + 1]

    index += 2

    children = []
    for _ in range(n_children):
        child, index = parse_tree(numbers, index)
        children.append(child)

    metadata = numbers[index:index + n_metadata]
    index += n_metadata

    return Tree(children, metadata), index

def run():
    numbers = read_input()
    tree, _ = parse_tree(numbers, 0)
    print tree.eval_metadata()
    print tree.eval_tree()

if __name__ == '__main__':
    run()
