#!/bin/bash
declare -A countrycodes
# Read from CSV
while IFS=, read code country newline
do countrycodes[$code]="$country"
done < database/countries.csv