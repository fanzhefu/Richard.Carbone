#!/bin/bash

# chmod +x scan.sh
# ./scan.sh ipiocs.txt
#

input_file="$1"

while IFS= read -r line; do
    echo "IP addr is been scaned: $line"
    nmap $line >scan_$line.txt 
done < "$input_file"

echo "Well done... 