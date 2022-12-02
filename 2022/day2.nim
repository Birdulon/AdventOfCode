{.hint[name]: off.}  # snake_case > camelCase
from std/math import floor_mod
import sequtils
import strutils
import tables

proc `%%` (a: int, b: int): int = floor_mod a, b

let move_map = to_table {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
let rounds = split_lines strip read_file "day2-input"

proc round_score(us: int, them: int): int = us + [3, 6, 0][(us-them) %% 3]

# Part 1
proc round_1_score(round: string): int =
    let them = move_map[round[0]]
    let us = move_map[round[2]]
    round_score us, them

echo rounds.map(round_1_score).fold_l(a + b)

# Part 2
proc round_2_score(round: string): int =
    let them = move_map[round[0]]
    let us_delta = move_map[round[2]] - 2
    let us = ((them + us_delta - 1) %% 3) + 1
    round_score us, them

echo rounds.map(round_2_score).fold_l(a + b)
