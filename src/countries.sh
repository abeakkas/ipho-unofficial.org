#!/bin/bash
declare -A countries
# Read from CSV
while IFS=, read code country newline
do countries[$code]="$country"
done < database/countries.csv