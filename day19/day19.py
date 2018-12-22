import operator
import sys
from collections import namedtuple


def do(combiner, operator, A, B, C, registers):
    registers[C] = combiner(operator, A, B, registers)
    return registers

rr = lambda *args : do(lambda op, A, B, R : int(op(R[A], R[B])), *args)
ri = lambda *args : do(lambda op, A, B, R : int(op(R[A],   B )), *args)
ir = lambda *args : do(lambda op, A, B, R : int(op(  A , R[B])), *args)
si = lambda *args : do(lambda op, A, B, R : int(op(A)   ), *args)
sr = lambda *args : do(lambda op, A, B, R : int(op(R[A])), *args)

opcodes = {
    'addr' : lambda *args : rr(operator.add  , *args) , 'addi' : lambda *args : ri(operator.add  , *args),
    'mulr' : lambda *args : rr(operator.mul  , *args) , 'muli' : lambda *args : ri(operator.mul  , *args),
    'banr' : lambda *args : rr(operator.and_ , *args) , 'bani' : lambda *args : ri(operator.and_ , *args),
    'borr' : lambda *args : rr(operator.or_  , *args) , 'bori' : lambda *args : ri(operator.or_  , *args),
    'setr' : lambda *args : sr(lambda A: A, *args) , 'seti' : lambda *args : si(lambda A : A, *args),
    'gtir' : lambda *args : ir(operator.gt   , *args) , 'gtri' : lambda *args : ri(operator.gt   , *args), 'gtrr' : lambda *args : rr(operator.gt, *args),
    'eqir' : lambda *args : ir(operator.eq   , *args) , 'eqri' : lambda *args : ri(operator.eq   , *args), 'eqrr' : lambda *args : rr(operator.eq, *args),
}

def read_input():
    f = open("input.txt")
    ip = int(f.readline().rstrip().split()[1])
    instructions = []
    for l in f:
        op, A, B, C = l.rstrip().split(" ")
        instructions.append((op, int(A), int(B), int(C)))
    return ip, instructions

def evaluate(ip_reg, program, registers):
    ip = registers[ip_reg]
    while True:
        instr, A, B, C  = program[ip]
        registers[ip_reg] = ip
        sys.stdout.write("ip={:2} {} {} {} {} {}".format(ip, registers, instr, A, B, C))
        registers = opcodes[instr](A, B, C, registers)  
        ip = registers[ip_reg]
        sys.stdout.write(" {}\n".format(registers))
        ip += 1
        if ip >= len(program):
            break

    print('Done')
    return registers[0]

def run():
    ip,program = read_input()
    #print(evaluate(ip, program, [0] * 6))
    print(evaluate(ip, program, [1] + [0] * 5))

if __name__ == '__main__':
    run()
