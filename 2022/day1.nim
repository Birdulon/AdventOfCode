import sequtils
import strutils
import sugar
from algorithm import sorted

let inputString = strip readFile "day1-input"
let elfStrings = inputString.split("\n\n")
let elfRations = collect(newSeq):
    for elf in elfStrings: collect(newSeq):
        for c in elf.split(): parseInt(c)
let elfCalories = collect(newSeq):
    for rations in elfRations: rations.foldl(a + b)

# Part 1
echo max elfCalories
# Part 2
echo elfCalories.sorted()[^3 .. ^1].foldl(a + b)
