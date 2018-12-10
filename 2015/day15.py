with open('day15-input', 'r') as file:
  data = [l.strip('\n') for l in file]
import numpy as np
from itertools import combinations_with_replacement as combi

ingredients = {}
for line in data:
  tokens = line.split()
  name = tokens[0].rstrip(':')
  values = [int(i.rstrip(',')) for i in tokens[2::2]]
  ingredients[name] = values

ingredients_matrix = np.asmatrix(np.vstack(ingredients.values()))

max_value = 0
max_value_500 = 0
for teaspoons in combi(range(len(ingredients)), 100):
  ingredient_amounts = [teaspoons.count(i) for i in range(len(ingredients))]
  property_amounts = (ingredients_matrix.T * np.mat(ingredient_amounts).T)
  if (property_amounts[:-1] < 1).sum():  # non-positive values for anything other than calories detected, abort
    continue
  value = np.prod(property_amounts[:-1])
  max_value = max(value, max_value)
  if property_amounts[-1] == 500:
    max_value_500 = max(value, max_value_500)

print(max_value)  # Part 1
print(max_value_500)  # Part 2
