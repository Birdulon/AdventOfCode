with open('day8-input', 'r') as file:
  data = [l.strip('\n') for l in file]

count = 0
for line in data:
  count += len(line) - len(line.encode('utf-8').decode('unicode-escape')) + 2  # Overall quotes aren't removed by encoding
print(count)  # Part 1

import json
count2 = 0
for line in data:
  count2 += len(json.dumps(line)) - len(line)
print(count2)  # Part 2
