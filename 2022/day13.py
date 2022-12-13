from helpers import *
list_pairs = [[eval(l) for l in pair.split('\n')] for pair in read_day(day).split('\n\n')]

def compare_lists(l1, l2) -> int:
	for e1, e2 in zip(l1, l2):
		if isinstance(e1, int):
			if isinstance(e2, int):
				if e1 < e2:
					return -1
				if e1 > e2:
					return 1
			else:
				comp = compare_lists([e1], e2)
				if comp != 0:
					return comp
		else:  # e1 list
			if isinstance(e2, int):
				comp = compare_lists(e1, [e2])
				if comp != 0:
					return comp
			else:
				comp = compare_lists(e1, e2)
				if comp != 0:
					return comp
	# At this point, lists are equal elementwise up to the smaller list
	if len(l1) > len(l2):
		return 1
	elif len(l1) < len(l2):
		return -1
	else:
		return 0

def count_ordered_pairs(list_pairs):
	return sum((i for i, (l1, l2) in enumerate(list_pairs, 1) if compare_lists(l1, l2) == -1))

def sort_all_and_find_dividers(list_pairs):
	spacers = [[[2]], [[6]]]
	flat = [l for ls in list_pairs + [spacers] for l in ls]
	flat.sort(key=cmp_to_key(compare_lists))
	return prod((flat.index(spacer) + 1 for spacer in spacers))


print(f'Part 1: {count_ordered_pairs(list_pairs)}')
print(f'Part 2: {sort_all_and_find_dividers(list_pairs)}')
