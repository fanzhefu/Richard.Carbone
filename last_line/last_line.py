#!/usr/bin/env python

last_line, aliases = [], []
name = '""'

with open('aliasTEMP.txt', 'r', encoding='utf-8') as f_in:
    aliases = f_in.readlines()
aliases.reverse()

for i, alias in enumerate(aliases):
    if aliases[i].split(',')[0] != name:
        last_line.append(alias)
        name = aliases[i].split(',')[0]

last_line.reverse()
with open('last_line.txt', 'w', encoding='utf-8') as f_out:
    f_out.writelines(last_line)
