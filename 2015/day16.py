from collections.abc import Callable
with open('day16-input', 'r') as file:
	lines = file.read().strip().split('\n')
known_owned = {'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3, 'akitas': 0, 'vizslas': 0, 'goldfish': 5, 'trees': 3, 'cars': 2, 'perfumes': 1}

aunts = {}
for line in lines:
	aunt, _, owned = line.partition(': ')
	owned_dict = {}
	for o in owned.split(', '):
		item, _, qty = o.partition(': ')
		owned_dict[item] = int(qty)
	aunts[aunt] = owned_dict

def find_aunt(aunts: dict[str, dict[str, int]], known_owned: dict[str, int], overrides: dict[str, Callable[[int, int], bool]] = None) -> str:
	def aunt_matches(items):
		for item, qty in items.items():
			target_qty = known_owned[item]
			if overrides is None or item not in overrides:
				if item in known_owned and target_qty != qty:
					return False
			else:
				if item in known_owned and not overrides[item](qty, target_qty):
					return False
		return True

	for aunt, items in aunts.items():
		if aunt_matches(items):
			return aunt
	return 'No Aunt found'

print(f'Part 1: {find_aunt(aunts, known_owned)}')
overrides = {'cats': int.__gt__, 'trees': int.__gt__, 'pomeranians': int.__lt__, 'goldfish': int.__lt__}
print(f'Part 2: {find_aunt(aunts, known_owned, overrides)}')
