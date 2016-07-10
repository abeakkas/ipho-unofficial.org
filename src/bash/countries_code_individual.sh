#!/bin/bash
# arguments:
# $1: country code to be created
# $2: previous country code if exists, "" otherwise
# $3: next country code if exists, "" otherwise
echo "Creating countries/$1/individual"
# imports:
source countrycodes.sh
source header_side.sh 2
source footer.sh
# load file:
html="$(cat templates/countries/code/individual.html)"
# replace templates:
html="${html/__HEADER_SIDE__/$header_side}"
html="${html/__FOOTER__/$footer}"
# Read from CSV
while IFS=, read code country nationalsite newline
do
    if [ "$code" == "$1" ]
    then
        if [ "$2" != "" ]
        then
            temp="$(cat templates/countries/code/individual_previous_country.html)"
            temp="${temp//__CODE__/$2}"
            html="${html/__PREVIOUS_COUNTRY__/$temp}"
        else
            html="${html/__PREVIOUS_COUNTRY__/}"
        fi
        if [ "$3" != "" ]
        then
            temp="$(cat templates/countries/code/individual_next_country.html)"
            temp="${temp//__CODE__/$3}"
            html="${html/__NEXT_COUNTRY__/$temp}"
        else
            html="${html/__NEXT_COUNTRY__/}"
        fi
        html="${html//__CODE__/$1}"
        html="${html//__COUNTRY__/${countrycodes[$1]}}"
        table=""
        lastyear=""
        yearrows=""
        t_row="$(cat templates/countries/code/individual_row.html)"
        t_gold="$(cat templates/countries/code/individual_gold.html)"
        t_silver="$(cat templates/countries/code/individual_silver.html)"
        t_bronze="$(cat templates/countries/code/individual_bronze.html)"
        t_honourable="$(cat templates/countries/code/individual_honourable.html)"
        while IFS=, read name _code year rank medal newline
        do
            if [ "$_code" == "$1" ]
            then
                row="${t_row//__NAME__/$name}"
                row="${row//__RANK__/$rank}"
                row="${row//__YEAR__/$year}"
                case $medal in
                1) row="${row//__MEDAL__/$t_gold}" ;;
                2) row="${row//__MEDAL__/$t_silver}" ;;
                3) row="${row//__MEDAL__/$t_bronze}" ;;
                4) row="${row//__MEDAL__/$t_honourable}" ;;
                *) row="${row//__MEDAL__/}" ;;
                esac
                if [ "$lastyear" == "$year" ]
                then
                    row="${row//__CLASS__/}"
                    yearrows=$yearrows$row
                else
                    table=$yearrows$table
                    row="${row//__CLASS__/doubleTopLine}"
                    yearrows=$row
                    lastyear="$year"
                fi
            fi
        done < database/estudiantes.csv
        table=$yearrows$table
        html="${html//__TABLE__/$table}"
    fi
done < database/countries.csv

html="${html//__BASE__/../..}"
source final_replacer.sh
# write
echo "$html" > ../countries/$1/individual.html