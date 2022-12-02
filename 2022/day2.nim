{.hint[name]: off.}  # snake_case > camelCase
from std/math import floor_mod
import sequtils
import strutils
import tables

proc `%%` (a: int, b: int): int = floor_mod(a, b)

let move_map = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}.to_table
let rounds = split_lines strip read_file "day2-input"

# Part 1
proc round_1_score(round: string): int =
    let them = move_map[round[0]]
    let us = move_map[round[2]]
    let win_score = [3, 6, 0][(us - them) %% 3]
    us + win_score

echo rounds.map(round_1_score).fold_l(a + b)

# Part 2
proc round_2_score(round: string): int =
    let them: int = move_map[round[0]]
    let us_delta = move_map[round[2]] - 2
    let us: int = ((them + us_delta - 1) %% 3) + 1
    let win_score = [3, 6, 0][(us - them) %% 3]
    us + win_score

echo rounds.map(round_2_score).fold_l(a + b)
