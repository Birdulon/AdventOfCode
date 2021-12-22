with open('day22input', 'r') as file:
    inputlines = file.read().strip().split('\n')

input_steps = []
for line in inputlines:
    state, _, coords = line.partition(' ')
    coords_str = [token[2:] for token in coords.split(',')]
    coords = tuple(tuple(int(i) for i in s.partition('..')[::2]) for s in coords_str)
    input_steps.append((state, coords))

def coord_t_to_cube(tup):
    (x0,x1), (y0,y1), (z0,z1) = tup
    return f'translate([{x0},{y0},{z0}]) cube([{x1-x0},{y1-y0},{z1-z0}]);'

scadlist = []
for onoff, tup in input_steps:
    operator = {'on':'union()', 'off':'difference()'}[onoff]
    cube = coord_t_to_cube(tup)
    scadlist.insert(0, operator+'{')
    scadlist.append(cube+'}')
scadstr = '\n'.join(scadlist)

with open('day22.scad', 'w') as file:
    file.write(scadstr)
