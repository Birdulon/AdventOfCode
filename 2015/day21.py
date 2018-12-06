with open('day21-input', 'r') as file:
  data = [l.strip('\n') for l in file]
boss_hp = int(data[0].split()[-1])
boss_damage = int(data[1].split()[-1])
boss_armor = int(data[2].split()[-1])

player_hp = 100
player_damage = 0
player_armor = 0

def attack_damage(damage, armor):
  return max(damage - armor, 1)

from math import ceil
def time_to_kill(damage, armor, hp):
  return ceil(hp/attack_damage(damage, armor))

s_shop_w = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
""".split('\n')[2:-1]

s_shop_a = """
Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
""".split('\n')[2:-1]

s_shop_r = """
Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
""".split('\n')[2:-1]

weapons = [[int(i) for i in w.split()[-3:]] for w in s_shop_w]
armors = [[int(i) for i in a.split()[-3:]] for a in s_shop_a] + [[0,0,0]]
rings = [[int(i) for i in r.split()[-3:]] for r in s_shop_r] + [[0,0,0], [0,0,0]]

def strategy_works(items):
  # cost = sum([i[0] for i in items])
  damage = sum([i[1] for i in items])
  armor = sum([i[2] for i in items])
  return time_to_kill(damage, boss_armor, boss_hp) <= time_to_kill(boss_damage, armor, player_hp)

from itertools import combinations
good_strategies = []
bad_strategies = []
for w in weapons:
  for a in armors:
    for r1, r2 in combinations(rings, 2):
      strat = (w, a, r1, r2)
      if strategy_works(strat):
        good_strategies.append(strat)
      else:
        bad_strategies.append(strat)

print(min([sum([i[0] for i in items]) for items in good_strategies]))  # Part 1
print(max([sum([i[0] for i in items]) for items in bad_strategies]))  # Part 2
