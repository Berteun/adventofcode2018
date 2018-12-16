import operator
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Sample:
    before: List[int]
    after: List[int]
    opcode: List[int]

def make_register(func):
    def generic_r(A, B, C, registers):
        registers[C] = int(func(registers[A], registers[B]))
    return generic_r

def make_immediate(func):
    def generic_i(A, B, C, registers):
        registers[C] = int(func(registers[A], B))
    return generic_i

def make_immediate_reverse(func):
    def generic_ir(A, B, C, registers):
        registers[C] = int(func(A, registers[B]))
    return generic_ir

opcodes = {
    'addr' : make_register(operator.add),
    'addi' : make_immediate(operator.add),
    'mulr' : make_register(operator.mul),
    'muli' : make_immediate(operator.mul),
    'banr' : make_register(operator.and_),
    'bani' : make_immediate(operator.and_),
    'borr' : make_register(operator.or_),
    'bori' : make_immediate(operator.or_),
    'setr' : make_register(lambda A, B : A),
    'seti' : make_immediate_reverse(lambda A, B : A),
    'gtir' : make_immediate_reverse(operator.gt),
    'gtri' : make_immediate(operator.gt),
    'gtrr' : make_register(operator.gt),
    'eqir' : make_immediate_reverse(operator.eq),
    'eqri' : make_immediate(operator.eq),
    'eqrr' : make_register(operator.eq),
}

def read_samples():
    lines = open("input.txt").readlines()
    offset = 0
    samples = []
    while True:
        sample = lines[offset:offset + 4]
        if not sample[0].startswith('Before'):
            break
        before_ = re.match(r'Before: \[(\d+), (\d+), (\d+), (\d+)\]', sample[0])
        before = [int(n) for n in before_.group(1,2,3,4)]
        opcode = [int(n) for n in sample[1].split()]
        after_ = re.match(r'After:  \[(\d+), (\d+), (\d+), (\d+)\]', sample[2])
        after = [int(n) for n in after_.group(1,2,3,4)]
        samples.append(Sample(before=before, after=after, opcode=opcode))
        offset += 4
    return samples

def read_program():
    lines = open("input.txt").readlines()
    offset = 0
    while True:
        if lines[offset].startswith('Before'):
            offset += 4
            continue
        else:
            offset += 1
            if not lines[offset].strip():
                continue
            return [tuple(map(int, l.split())) for l in lines[offset:]]

def count_three_or_more(samples):
    count = 0
    for s in samples:
        possible = 0
        for op in opcodes:
            registers = s.before[:]
            A,B,C = tuple(s.opcode[1:])
            opcodes[op](A,B,C, registers)
            if registers == s.after:
                possible += 1
        if possible > 2:
            count += 1
    return count

def make_opcodes_map(samples):
    names = set(opcodes.keys())
    candidates = {
        n : names.copy() for n in range(len(opcodes))
    }

    for s in samples:
        possible = set()
        for op in opcodes:
            registers = s.before[:]
            code,A,B,C = s.opcode
            opcodes[op](A,B,C, registers)
            if registers == s.after:
                possible.add(op)
        candidates[code] &= possible

    return candidates

def reduce_map(opcode_map):
    while any(len(l) > 1 for l in opcode_map.values()):
        fixed = set(code for code in opcode_map if len(opcode_map[code]) == 1)
        for n in fixed:
            name = opcode_map[n].copy().pop()
            for candidates in opcode_map.values():
                if len(candidates) > 1 and name in candidates:
                    candidates.remove(name)
    return { k : opcode_map[k].pop() for k in opcode_map }

def evaluate(program, opm, registers):
    for (code, A, B, C) in program:
        opcodes[opm[code]](A, B, C, registers)
    return registers

def run():
    samples = read_samples()
    print(count_three_or_more((samples)))
    m = reduce_map(make_opcodes_map(samples))
    print(evaluate(read_program(), m, [0,0,0,0])[0])

if __name__ == '__main__':
    run()
