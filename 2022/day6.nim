{.hint[name]: off.}  # snake_case > camelCase
import strutils
let line = strip read_file "input/6"

# proc find_first(n: int): int =
#     for i in n..line.len:
#         var s = {line[i-n]}
#         for c in line[i-n+1..<i]:
#             s.incl(c)
#         if s.len == n:
#             return i
#     return -1

let a = ord('a')
proc to_bit(c: char): uint32 =
    return uint32(1 shl (ord(c) - a))

proc find_first(n: int, skip: int = 0): int =
    for i in max(n, skip)..line.len:
        block inner:
            var s = to_bit line[i-n]
            for c in line[i-n+1..<i]:
                let b = to_bit c
                if (s and b) != 0:
                    break inner
                s = s or b
            return i
    return -1

# echo find_first 4
# echo find_first 14

var four = 0
var fourteen = 0
for i in 1..1000000:
    four = find_first 4
    fourteen = find_first(14, four)
echo four
echo fourteen
