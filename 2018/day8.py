with open('day8-input', 'r') as file:
  data = [int(i) for i in [l.strip('\n') for l in file][0].split()]
# data = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]  # For example test casing

def construct_node(i):
  num_children = data[i]
  num_meta = data[i+1]
  children = []
  ptr = i+2
  for c in range(num_children):
    node, ptr = construct_node(ptr)
    children.append(node)
  metadata = data[ptr:ptr+num_meta]
  return (children, metadata), ptr+num_meta

def sum_tree_meta(tree):
  return sum(tree[1] + [sum_tree_meta(child) for child in tree[0]])

def sum_tree_meta_value(tree):
  if not tree[0]:
    return sum(tree[1])
  return sum([sum_tree_meta_value(tree[0][i-1]) for i in tree[1] if i-1 < len(tree[0])])

tree = construct_node(0)[0]
print(sum_tree_meta(tree))  # Part 1
print(sum_tree_meta_value(tree))  # Part 2
