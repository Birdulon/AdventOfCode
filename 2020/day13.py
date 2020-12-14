input_t = 1002392  # Short input so we'll just hardcode
input_busIDs = "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,421,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,19,x,x,x,x,x,x,x,x,x,29,x,487,x,x,x,x,x,x,x,x,x,x,x,x,13"
ids = {int(x) for x in input_busIDs.split(',') if x != 'x'}

next_arrivals = {x: x*(-(-input_t//x)) for x in ids}  # -(-x//y) is ceil(x/y)
id, t = min(next_arrivals.items(), key=lambda x: x[1])
print(f'Part 1: Next bus is Bus {id} at t={t} -> {id*(t-input_t)}')

from sympy.ntheory.modular import crt
pairs = [(i,int(v)) for i,v in enumerate(input_busIDs.split(',')) if v != 'x']
print(f'Part 2: t = {crt([id for time,id in pairs], [-time for time,id in pairs])[0]}')
