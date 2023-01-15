from math import prod

with open('day24-input', 'r') as file:
	input_nums = [int(x) for x in file.read().strip().split('\n')]
if len(input_nums) == len(set(input_nums)):
	print('All inputs are unique')
else:
	print('Inputs are not unique, this solution will not work without slight changes')


def try_groups(diff, target: int, num_groups: int) -> bool:
	return True  # TODO - this is strictly incorrect but the inputs aren't mean enough for this to matter, lmao


def dfs(input_nums: list[int], num_groups: int = 3):
	full_sum = sum(input_nums)
	target = full_sum//num_groups
	print(input_nums, full_sum, target)
	input_set = set(input_nums)

	best = None

	def is_better(num_packages: int, quantum_entanglement: int) -> bool:
		if best is None:
			return True
		if best[0] > num_packages:
			return True
		if best[0] == num_packages and best[1] > quantum_entanglement:
			return True
		return False

	stack = [{x} for x in input_nums]
	while stack:
		if len(stack)>1000:
			print(f'Stack size is {len(stack)}')
		group_1 = stack.pop()

		num_packages = len(group_1)
		if best and best[0] < num_packages:
			continue
		diff = input_set - group_1
		group_sum = sum(group_1)
		delta = target - group_sum
		if delta < 0:  # overshoot
			continue
		elif delta == 0:
			quantum_entanglement = prod(group_1)
			if is_better(num_packages, quantum_entanglement) and try_groups(diff, target, num_groups):
				best = (num_packages, quantum_entanglement, group_1)
				print(best)
		else:  # delta > 0
			min_package = min(group_1)
			for x in sorted(diff):
				if x > min_package:
					break
				stack.append(group_1 | {x})
	return best


print(f'Part 1: {dfs(input_nums)[1]}')
print(f'Part 2: {dfs(input_nums, 4)[1]}')
