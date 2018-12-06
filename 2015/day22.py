with open('day22-input', 'r') as file:
  data = [l.strip('\n') for l in file]
boss_hp = int(data[0].split()[-1])
boss_damage = int(data[1].split()[-1])
player_hp = 50
player_mp = 500

from collections import namedtuple
State = namedtuple('State', ['player_hp', 'player_mp', 'boss_hp', 'shield', 'poison', 'recharge', 'mp_spent'])

initial_state = State(player_hp, player_mp, boss_hp, 0, 0, 0, 0)

def magic_missile(state):
  if state.player_mp < 53:
    raise ValueError('Not enough mana')
  return State(state.player_hp, state.player_mp-53, state.boss_hp-4,
               state.shield, state.poison, state.recharge, state.mp_spent+53)

def drain(state):
  if state.player_mp < 73:
    raise ValueError('Not enough mana')
  return State(state.player_hp+2, state.player_mp-73, state.boss_hp-2,
               state.shield, state.poison, state.recharge, state.mp_spent+73)

def poison(state):
  if state.player_mp < 173:
    raise ValueError('Not enough mana')
  if state.poison > 0:
    raise ValueError('Already poisoned')
  return State(state.player_hp, state.player_mp-173, state.boss_hp,
               state.shield, state.poison+6, state.recharge, state.mp_spent+173)

def shield(state):
  if state.player_mp < 113:
    raise ValueError('Not enough mana')
  if state.shield > 0:
    raise ValueError('Already shielded')
  return State(state.player_hp, state.player_mp-113, state.boss_hp,
               state.shield+6, state.poison, state.recharge, state.mp_spent+113)

def recharge(state):
  if state.player_mp < 229:
    raise ValueError('Not enough mana')
  if state.recharge > 0:
    raise ValueError('Already recharging')
  return State(state.player_hp, state.player_mp-229, state.boss_hp,
               state.shield, state.poison, state.recharge+5, state.mp_spent+229)

def turn_start(state, hardmode_player_turn=False):
  s = state._asdict()
  if hardmode_player_turn:
    s['player_hp'] -= 1
    if s['player_hp'] <= 0:
      return State(**s)
  if s['recharge'] > 0:
    s['player_mp'] += 101
    s['recharge'] -= 1
  if s['poison'] > 0:
    s['boss_hp'] -= 3
    s['poison'] -= 1
  if s['shield'] > 0:
    s['shield'] -= 1
  return State(**s)

def boss_action(state):
  damage = boss_damage
  if state.shield > 0:
    damage = max(damage-7, 1)
  return State(state.player_hp-damage, state.player_mp, state.boss_hp,
               state.shield, state.poison, state.recharge, state.mp_spent)

spells = [magic_missile, drain, shield, poison, recharge]
mana_reqs = [53, 73, 113, 173, 229]
def execute_round(state, command, hardmode=False):
  state = turn_start(state, hardmode)
  if state.player_hp <= 0:
    return state
  state = spells[command](state)
  state = turn_start(state)
  if state.boss_hp > 0:
    state = boss_action(state)
  return state

maximum_mana_usage = 100000  # Arbitrarily large
winning_commands = []
def tree_simulation(state, commands, hardmode=False):
  global maximum_mana_usage, winning_commands

  state = execute_round(state, commands[-1], hardmode)
  if state.player_hp <= 0 or state.mp_spent > maximum_mana_usage:
    return 100000
  if state.boss_hp <= 0:
    maximum_mana_usage = state.mp_spent
    winning_commands = commands
    return state.mp_spent

  mp_spent = 100000
  for cmd, mana in enumerate(mana_reqs):
    if state.player_mp > mana:
      try:
        mp_spent = min(tree_simulation(state, commands+[cmd], hardmode), mp_spent)
      except ValueError:
        pass
  return mp_spent

mana = min([tree_simulation(initial_state, [c]) for c in range(len(spells))])
print(mana)  # Part 1
part1_commands = winning_commands

maximum_mana_usage = 100000
mana_hard = min([tree_simulation(initial_state, [c], hardmode=True) for c in range(len(spells))])
print(mana_hard)  # Part 2
part2_commands = winning_commands

# Bonus: show the winning simulations
spell_names = ['Magic Missile', 'Drain', 'Shield', 'Poison', 'Recharge']

def perform_simulation(command_list, maximum_mana_usage=None, hardmode=False):
  state = initial_state
  for i, command in enumerate(command_list):
    print(state)
    print(f'Player casts {spell_names[command]}!')
    try:
      state = execute_round(state, command, hardmode)
    except ValueError:
      return f'Failed at round #{i+1}: Insufficient mana'
    if maximum_mana_usage and state.mp_spent >= maximum_mana_usage:
      return f'Failed at round #{i+1}: Exceeded mana budget'
    if state.player_hp <= 0:
      return f'Failed at round #{i+1}: Player died'
    if state.boss_hp <= 0:
      return f'Succeeded at round #{i+1}', state.mp_spent
  return f'Ran out of commands but game is not over', state

print('Ideal normal mode fight:')
print(perform_simulation(part1_commands))
print('')
print('Ideal hard mode fight:')
print(perform_simulation(part2_commands, hardmode=True))
