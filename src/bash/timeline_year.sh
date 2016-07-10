#!/bin/bash
# arguments:
# $1: year of IPhO to be created
# $2: previous year if exists, 0 otherwise
# $3: next year if exists, 0 otherwise
# $4: number of IPhO to be created
echo "Creating timeline/$1"
mkdir -p ../timeline/$1
source timeline_year_index.sh $1 $2 $3
source timeline_year_country.sh $1 $2 $3 $4
source timeline_year_individual.sh $1 $2 $3 $4