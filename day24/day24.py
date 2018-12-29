import re
import sys
from typing import List
from dataclasses import dataclass

@dataclass
class Group:
    id: int
    kind: str
    unit_size: int
    hit_points: int
    weaknesses: List[str]
    immune: List[str]
    damage: int
    attack_type: str
    initiative: int

    def power(self):
        return self.unit_size * self.damage

    def does_damage(self, other):
        if self.kind == other.kind:
            return 0

        damage = self.power()
        if self.attack_type in other.weaknesses:
            damage *= 2
        if self.attack_type in other.immune:
            damage = 0

        return damage 

    def __hash__(self):
        return hash(self.kind + str(self.id))

full_pattern = r"(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that does (\d*) (cold|slashing|radiation|bludgeoning|fire) damage at initiative (\d+)"
weak_pattern = r"weak to ([^);]*)" 
immune_pattern = r"immune to ([^);]*)" 
trait_pattern = "(cold|slashing|radiation|bludgeoning|fire)"

def read_groups(group_type, group_list, boost):
    groups = []
    for i, group in enumerate(group_list):
        if not group.strip():
            continue
        m = re.match(full_pattern, group)
        unit_size = int(m.group(1))
        hit_points = int(m.group(2))

        weaknesses = []
        immune = []
        if m.group(3):
            if 'weak' in m.group(3):
                traits = re.search(weak_pattern, m.group(3)).group(1)
                weaknesses = re.findall(trait_pattern, traits)
            if 'immune' in m.group(3):
                traits = re.search(immune_pattern, m.group(3)).group(1)
                immune = re.findall(trait_pattern, traits)
    
        damage = int(m.group(4))
        if group_type == 'immune':
            damage += boost
        attack_type = m.group(5)
        initiative = int(m.group(6))

        groups.append(Group(i+1, group_type, unit_size, hit_points, weaknesses, immune, damage, attack_type, initiative))
    return groups

def read_input(input_file, boost=0):
    immune, infection = open(input_file).read().split("\n\n")

    immune_list = immune.split('\n')[1:]
    infection_list = infection.split('\n')[1:]

    immune_groups = read_groups('immune', immune_list, boost)
    infection_groups = read_groups('infection', infection_list, boost)

    return immune_groups + infection_groups

def choose_target(group, other, selected):
    l = [g for g in sorted(other, reverse=True, key=lambda g : (group.does_damage(g), g.power(), g.initiative)) 
            if group.kind != g.kind and group.does_damage(g) > 0 and g.unit_size > 0 and g not in selected]
    return l[0] if l else None

def get_targets(groups):
    d = {}
    selected = set()
    for g in groups:
        target = choose_target(g, groups, selected)
        if target:
            selected.add(target)
            d[g] = target

    return d

def evolve(groups, targets):
    s = 0
    for g in sorted(groups, key=lambda g: g.initiative, reverse=True):
        if g in targets:
            t = targets[g]
            reduced = min(t.unit_size, (g.does_damage(t) // t.hit_points))
            s += reduced
            t.unit_size -= reduced
    return s == 0


def evaluate(groups):
    sides = set(g.kind for g in groups if g.unit_size > 0)
    while len(sides) > 1: 
        groups.sort(key=lambda g : (g.power(), g.initiative), reverse=True)
        targets = get_targets(groups)
        stuck = evolve(groups, targets)
        if stuck:
            return "None"
        sides = set(g.kind for g in groups if g.unit_size > 0)
    return sides.pop()

def run(input_file):
    boost = 0
    winner = 'infection'
    while winner != 'immune':
        groups = read_input(input_file, boost)
        winner = evaluate(groups)
        print("Boost: {}, Winning: {}, Rest: {}".format(boost, winner, sum(g.unit_size for g in groups)))
        boost += 1


if __name__ == '__main__':
    if len(sys.argv) == 1:
        input_file = "input.txt"
    else:
        input_file = sys.argv[1]
    run(input_file)
