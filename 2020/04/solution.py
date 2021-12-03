import re

import pandas as pd

# load and preprocess puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read()  # .splitlines()

END = "<END>"
puzzle = puzzle.replace('\n\n', END).replace('\n', ' ').replace(END, '\n')
puzzle = puzzle.splitlines()

# create dict of prop:value for each entries
entries = [list(map(lambda x: x.split(':'), entry.split()))
           for entry in puzzle]
entries = [{prop[0]: prop[1] for prop in infos}
           for infos in entries]

# create passport dataframe
passports = pd.DataFrame.from_dict(entries)
print(passports)

# drop useless 'cid' columns and entries with empty values
props = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
passports = passports[[prop for prop in props if prop != 'cid']].copy()
passports = passports.dropna().copy()
print(len(passports))

# convert int columns to int type
passports['byr'] = passports['byr'].map(int)
passports['iyr'] = passports['iyr'].map(int)
passports['eyr'] = passports['eyr'].map(int)

# create masks to filter invalid entries
mask1 = (passports['byr'] >= 1920) & (passports['byr'] <= 2002)
mask2 = (passports['iyr'] >= 2010) & (passports['iyr'] <= 2020)
mask3 = (passports['eyr'] >= 2020) & (passports['eyr'] <= 2030)

passports['hgt_num'] = passports['hgt'].map(
    lambda x: int(x.replace('cm', '').replace('in', '')))
passports['hgt_unit'] = passports['hgt'].map(lambda x: re.sub(r"\d+", '', x))
mask4a = (passports['hgt_unit'] == 'in') & (
    passports['hgt_num'] >= 59) & (passports['hgt_num'] <= 76)
mask4b = (passports['hgt_unit'] == 'cm') & (
    passports['hgt_num'] >= 150) & (passports['hgt_num'] <= 193)

mask5 = (passports['hcl'].map(
    lambda x: bool(re.fullmatch(r"#[0-9a-f]{6}", x))))
mask6 = (passports['ecl'].map(lambda x: x in [
    'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']))
mask7 = (passports['pid'].map(lambda x: bool(re.fullmatch(r"\d{9}", x))))

# filter for valid entries
passports = passports.loc[
    mask1 & mask2 & mask3 & (mask4a | mask4b) & mask6 & mask5 & mask7].copy()
print(len(passports))

"""
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""
