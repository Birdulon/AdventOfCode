{.hint[name]: off.}  # snake_case > camelCase
import strutils
let line = strip read_file "input/6"

proc string_no_duplicate_chars(s: string): bool =
    # 1M iterations: nim r -d:danger day6.nim  90.29s user 0.27s system 99% cpu 1:30.99 total
    for i in 0..<s.len:
        let c = s[i]
        for j in (i+1)..<s.len:
            if c == s[j]:
                return false
    return true

proc string_no_duplicate_chars_1iter(s: string): bool =
    # 1M iterations: nim r -d:danger day6.nim  206.13s user 0.69s system 99% cpu 3:27.83 total
    for i in 0..<s.len:
        let c1 = s[i]
        for c2 in s[i+1..^1]:
            if c1==c2:
                return false
    return true

proc string_no_duplicate_chars_2iter(s: string): bool =
    # 1M iterations: nim r -d:danger day6.nim  259.15s user 0.76s system 99% cpu 4:20.86 total
    for i, c1 in s[0..^2]:
        for c2 in s[i+1..^1]:
            if c1==c2:
                return false
    return true

proc find_first(n: int, skip: int = 0): int =
    for i in max(n, skip)..<line.len:
        if string_no_duplicate_chars(line[i-n..<i]):
            return i
    return -1

var four = 0
var fourteen = 0
for i in 1..1000000:
    four = find_first 4
    fourteen = find_first(14, four)
echo four
echo fourteen
