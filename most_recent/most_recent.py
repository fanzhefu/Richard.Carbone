#!/usr/bin/env python

INPUT = 'description.txt'   # Input file name
OUTPUT = 'most_recent.txt'  # Output file name

name, most_recent = '', []

for row in open('description.txt', 'r', encoding='utf-8').readlines()[::-1]:
    row_lst = row.rstrip('","\n').split('"')
    if row_lst[-1] != name:
        most_recent.append(row_lst[-1]+': '+''.join(row_lst[:-3])+'\n')
        name = row_lst[-1]

open(OUTPUT, 'w', encoding='utf-8').writelines(most_recent[::-1])
print('Done... ... ')
