from std/math import floorMod
import sequtils
import strutils
import tables

proc `%%` (a: int, b: int): int = floorMod(a, b)

let moveMap = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}.toTable
let rounds = splitlines strip readFile "day2-input"

# Part 1
proc round1Score(round: string): int =
    let them = moveMap[round[0]]
    let us = moveMap[round[2]]
    let winScore = [3, 6, 0][(us - them) %% 3]
    us + winScore

echo rounds.map(round1Score).foldl(a + b)

# Part 2
proc round2Score(round: string): int =
    let them: int = moveMap[round[0]]
    let usDelta = moveMap[round[2]] - 2
    let us: int = ((them + usDelta - 1) %% 3) + 1
    let winScore = [3, 6, 0][(us - them) %% 3]
    us + winScore

echo rounds.map(round2Score).foldl(a + b)
