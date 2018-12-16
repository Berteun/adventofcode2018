import operator
from collections import namedtuple

Sample = namedtuple('Sample', ['before', 'after', 'opcode'])

def do(combiner, operator, A, B, C, registers):
    registers[C] = combiner(operator, A, B, registers)
    return registers

rr = lambda *args : do(lambda op, A, B, R : int(op(R[A], R[B])), *args)
ri = lambda *args : do(lambda op, A, B, R : int(op(R[A],   B )), *args)
ir = lambda *args : do(lambda op, A, B, R : int(op(  A , R[B])), *args)

opcodes = {
    'addr' : lambda *args : rr(operator.add  , *args) , 'addi' : lambda *args : ri(operator.add  , *args),
    'mulr' : lambda *args : rr(operator.mul  , *args) , 'muli' : lambda *args : ri(operator.mul  , *args),
    'banr' : lambda *args : rr(operator.and_ , *args) , 'bani' : lambda *args : ri(operator.and_ , *args),
    'borr' : lambda *args : rr(operator.or_  , *args) , 'bori' : lambda *args : ri(operator.or_  , *args),
    'setr' : lambda *args : rr(lambda A,B : A, *args) , 'seti' : lambda *args : ir(lambda A,B : A, *args),
    'gtir' : lambda *args : ir(operator.gt   , *args) , 'gtri' : lambda *args : ri(operator.gt   , *args), 'gtrr' : lambda *args : rr(operator.gt, *args),
    'eqir' : lambda *args : ir(operator.eq   , *args) , 'eqri' : lambda *args : ri(operator.eq   , *args), 'eqrr' : lambda *args : rr(operator.eq, *args),
}

def read_input():
    part1, part2 = open("input.txt").read().split("\n\n\n\n")
    samples = [Sample(before=[int(n) for n in s.split("\n")[0][9:-1].split(', ')],
               opcode=[int(n) for n in s.split("\n")[1].split()],
               after=[int(n) for n in s.split("\n")[2][9:-1].split(', ')])
               for s in part1.split("\n\n")]
    program = [tuple(map(int, l.split())) for l in part2.split("\n") if l.strip()]
    return samples, program

def count_three_or_more(samples):
    return sum(sum(s.after == opcodes[op](*s.opcode[1:], s.before[:]) for op in opcodes) > 2 for s in samples)

def make_opcodes_map(samples):
    return { s.opcode[0] : set(op for op,f in opcodes.items() if f(*s.opcode[1:], s.before[:]) == s.after) for s in samples }

def resolve_map(opcode_map):
    while any(len(l) > 1 for l in opcode_map.values()):
        for single, name in ((c,s.copy().pop()) for c,s in opcode_map.items() if len(s) == 1):
            for multiple in (c for c in opcode_map.values() if len(c) > 1):
                    multiple.discard(name)
    return { k : opcode_map[k].pop() for k in opcode_map }

def evaluate(program, opm, registers):
    sum(len(opcodes[opm[code]](A, B, C, registers)) for (code, A, B, C) in program)
    return registers

def run():
    samples,program = read_input()
    print(count_three_or_more((samples)))
    print(evaluate(program, resolve_map(make_opcodes_map(samples)), [0,0,0,0])[0])

if __name__ == '__main__':
    run()
