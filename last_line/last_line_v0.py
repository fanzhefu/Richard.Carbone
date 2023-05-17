# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:31:34 2023

@author: fan.z
"""
#!/usr/bin/env python
INPUT = 'aliasTEMP.txt'   # Input file name
OUTPUT = 'last_line1.txt'  # Output file name

name, last_line, aliases = '""', [], []

for alias in open(INPUT, 'r', encoding='utf-8').readlines()[::-1]:
    if alias.split(',')[0] != name:
        last_line.append(alias.split(
            ',')[0]+','+','.join(alias.split(',')[2:]))
        name = alias.split(',')[0]

open(OUTPUT, 'w', encoding='utf-8').writelines(last_line[::-1])
print('Done... ... ')
