#!/bin/bash
# arguments:
# $1: country code to be created
# $2: previous country code if exists, "" otherwise
# $3: next country code if exists, "" otherwise
echo "Creating countries/$1"
mkdir -p ../countries/$1
./countries_code_index.sh $1 $2 $3
./countries_code_individual.sh $1 $2 $3