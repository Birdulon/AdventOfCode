from helpers import *
from sympy import Symbol, Eq, solve

lines = read_day(day).split('\n')

sample_lines = '''
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''.strip().split('\n')

monkey_re = re.compile(r'(\w{4})')
def eval_root(lines: list[str]):
	monkeys = {}
	for line in lines:
		monkey, _, operation = line.partition(': ')
		operation = monkey_re.sub(r'e("\1")', operation)
		# print(monkey, operation)
		monkeys[monkey] = operation

	@cache
	def e(monkey):
		return eval(monkeys[monkey], {'e': e})

	return int(e('root'))

def inline_monkeys(lines: list[str]):
	monkeys = {}
	for line in lines:
		monkey, _, operation = line.partition(': ')
		monkeys[monkey] = operation

	monkeys['root'] = monkeys['root'].replace('+', '==')
	monkeys['humn'] = 'X'

	# delisp_pattern = re.compile(r'\((\d+)\)')
	# eval_pattern = re.compile(r'\((\d+[\+\-\*\/]+\d+)\)')
	# def ev(s):
	# 	last = ''
	# 	out = s.replace(' ', '').replace('/', '//')
	# 	while last != out:
	# 		# print('looped')
	# 		last = out
	# 		out = eval_pattern.sub(lambda m: str(eval(m.group(1))), last)
	# 		out = delisp_pattern.sub(r'\1', out)
	# 	return out.replace('//', '/')

	@cache
	def inline(monkey) -> str:
		return monkey_re.sub(lambda m: inline(m.group(1)), f'({monkeys[monkey]})')
	# return ev(inline('root'))
	# lhs, _, rhs = ev(inline('root')).partition('==')
	lhs, _, rhs = inline('root')[1:-1].partition('==')  # above leaves residual () around entire expression
	X = Symbol('X')
	# return solve(Eq(lhs, rhs))
	return int(eval(f'solve(Eq({lhs}, {rhs}))')[0])


print(f'Part 1 (sample): {eval_root(sample_lines)}')  #152
print(f'Part 1: {eval_root(lines)}')  # 66174565793494
print(f'Part 2 (sample): {inline_monkeys(sample_lines)}')
print(f'Part 2: {inline_monkeys(lines)}')
