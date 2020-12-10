with open('input04', 'r') as file:
  lines = [l.replace('\n', ' ') for l in file.read().split('\n\n')]
passports = [{k:v for k,_,v in [token.partition(':') for token in line.split()]} for line in lines]

req_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
valid_passports = [p for p in passports if req_keys.issubset(p.keys())]
print(f'Part 1: {len(valid_passports)} valid passports')

# Absolutely nothing cute about this validation function
valid_ecl = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
valid_hgt = {'cm': lambda i: (150<=i<=193), 'in': lambda i: (59<=i<=76)}
def validate_pp(pp):
  try:
    if not (1920 <= int(pp['byr']) <= 2002):
      return False
    if not (2010 <= int(pp['iyr']) <= 2020):
      return False
    if not (2020 <= int(pp['eyr']) <= 2030):
      return False
    if not valid_hgt[pp['hgt'][-2:]](int(pp['hgt'][:-2])):
      return False
    hcl = pp['hcl']
    if hcl[0] != '#':
      return False
    for c in hcl[1:]:
      if c not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}:
        return False
    if pp['ecl'] not in valid_ecl:
      return False
    if len(pp['pid'])!=9:
      return False
    int(pp['pid'])
    return True
  except:
    #raise
    return False


print(f'Part 2: {[validate_pp(pp) for pp in valid_passports].count(True)} valid passports')
