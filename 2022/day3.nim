{.hint[name]: off.}  # snake_case > camelCase
import sequtils
import strutils
import std/sets
import sugar

let elves = split_lines strip read_file "input/3"

proc get_priority(c: char): int =
    if c in 'a'..'z':
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27

# Part 1
proc part_1_score(line: string): int =
    let halflen = len(line) shr 1
    var knapsack_1 = collect initHashSet:  # Couldn't work out how to collect to set[char]
        for c in line[0..<halflen]: {c}
    var knapsack_2 = collect initHashSet:
        for c in line[halflen..^1]: {c}
    for common in knapsack_1 * knapsack_2:
        return get_priority(common)

echo elves.map(part_1_score).fold_l(a + b)

# Part 2
proc part_2_score(lines: seq[string]): int =
    let knapsacks = collect newSeq:
        for line in lines:
            collect initHashSet:
                for c in line: {c}
    for common in knapsacks.fold_l(a * b):
        return get_priority(common)

echo elves.distribute(len(elves) div 3).map(part_2_score).fold_l(a + b)
