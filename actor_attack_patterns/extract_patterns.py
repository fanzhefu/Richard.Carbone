#!/usr/bin/env python
import os

INPUT_DIR = 'json_files'
OUTPUT_DIR = 'results'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for file in os.listdir(INPUT_DIR):
    text = open(INPUT_DIR+'\\'+file, 'r', encoding='utf-8').readlines()[-1]
    open(OUTPUT_DIR+'\\'+file, 'w', encoding='utf-8').write(text)

print('\n Done... ...')
