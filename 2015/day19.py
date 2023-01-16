import re
with open('day19-input', 'r') as file:
	replacements, _, medicine_molecule = file.read().strip().partition('\n\n')
replacements = replacements.strip().split('\n')
replacements = [(old, new) for old, _, new in (rep.partition(' => ') for rep in replacements)]
medicine_molecule = medicine_molecule.strip()


unique_molecules = set()
for old, new in replacements:
	r = re.compile(old)
	for match in r.finditer(medicine_molecule):
		unique_molecules.add(medicine_molecule[:match.start()] + new + medicine_molecule[match.end():])

print(f'Part 1: {len(unique_molecules)}')


starting_molecule = 'e'
replacements_ordered = sorted(replacements, key=lambda x: (len(x[1]), x[1]))  # Shortest output to longest output
regexes_ordered = [(old, re.compile(new)) for old, new in replacements_ordered]
biggest_reduction = max((len(new) - len(old) for old, new in replacements_ordered))
print(f'Biggest reducing step is {biggest_reduction}')

# stack = [(0, medicine_molecule)]  # We will work backwards from medicine to 'e' as it's easier to not make garbage
stack = {medicine_molecule: 0}  # We will work backwards from medicine to 'e' as it's easier to not make garbage
best = 500  # Set a hard limit to prevent any potential cycles going forever
best_molecules = {}

while stack:
	# Retrieve state
	# replacements, molecule = stack.pop()
	molecule, replacements = stack.popitem()
	# Don't process if this is already worse
	if replacements >= best:
		continue
	# If the best case can't reduce enough, abort
	target_reduction = len(molecule) - 1
	min_replacements = -(-target_reduction//biggest_reduction)  # ceildiv
	if replacements + min_replacements > best:
		continue
	# If we have worked back to the starting molecule, record this result
	if molecule == starting_molecule:
		best = replacements
		print(f'New best found: {best}')
		continue

	r1 = replacements + 1
	for old, r in regexes_ordered:
		for match in r.finditer(molecule):
			s = molecule[:match.start()] + old + molecule[match.end():]
			if s not in best_molecules or best_molecules[s] < r1:
				best_molecules[s] = r1
				# stack.append((r1, s))
				stack[s] = r1

print(f'Part 2: fewest replacements = {best}')
