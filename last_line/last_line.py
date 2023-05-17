#!/usr/bin/env python

INPUT = 'aliasTEMP.txt'   # Input file name
OUTPUT = 'last_line.txt'  # Output file name

last_line, aliases = [], []
name = '""'

with open(INPUT, 'r', encoding='utf-8') as f_in:
    aliases = f_in.readlines()
aliases.reverse()

for i, alias in enumerate(aliases):
    if aliases[i].split(',')[0] != name:
        last_line.append(alias)
        name = aliases[i].split(',')[0]

last_line.reverse()
with open(OUTPUT, 'w', encoding='utf-8') as f_out:
    f_out.writelines(last_line)

print('Done... ...')
