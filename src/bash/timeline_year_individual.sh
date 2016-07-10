#!/bin/bash
# arguments:
# $1: year of IPhO to be created
# $2: previous year if exists, 0 otherwise
# $3: next year if exists, 0 otherwise
# $4: number of IPhO to be created
echo "Creating timeline/$1/individual"
# imports
source countrycodes.sh
source ordinals.sh
source header_side.sh 1
source footer.sh
# load file and replace basics
html="$(cat templates/timeline/year/individual.html)"
html="${html//__HEADER_SIDE__/$header_side}"
html="${html//__FOOTER__/$footer}"
# Replacing year information
html="${html//__NUMBER__/$4}"
html="${html//__ORDINAL__/${ordinals[$4]}}"
html="${html//__YEAR__/$1}"
if [ $2 != 0 ]
then
    previous_year_html="$(cat templates/timeline/year/individual_previous_year.html)"
    previous_year_html="${previous_year_html//__PREVIOUS_YEAR__/$2}"
    html="${html//__PREVIOUS_YEAR__/$previous_year_html}"
else
    html="${html//__PREVIOUS_YEAR__/}"
fi
if [ $3 != 0 ]
then
    next_year_html="$(cat templates/timeline/year/individual_next_year.html)"
    next_year_html="${next_year_html//__NEXT_YEAR__/$3}"
    html="${html//__NEXT_YEAR__/$next_year_html}"
else
    html="${html//__NEXT_YEAR__/}"
fi
# Creating table
table=""
rowt="$(cat templates/timeline/year/individual_row.html)"
gold="$(cat templates/timeline/year/individual_gold.html)"
silver="$(cat templates/timeline/year/individual_silver.html)"
bronze="$(cat templates/timeline/year/individual_bronze.html)"
honourable="$(cat templates/timeline/year/individual_honourable.html)"
while IFS=, read name code year rank medal newline
do 
    if [ $1 == $year ]
    then
        row="$rowt"
        row="${row//__NAME__/$name}"
        row="${row//__CODE__/$code}"
        row="${row//__COUNTRY__/${countrycodes[$code]}}"
        row="${row//__RANK__/$rank}"
        case $medal in
        1) row="${row//__MEDAL__/$gold}" ;;
        2) row="${row//__MEDAL__/$silver}" ;;
        3) row="${row//__MEDAL__/$bronze}" ;;
        4) row="${row//__MEDAL__/$honourable}" ;;
        *) row="${row//__MEDAL__/}" ;;
        esac
        table+="$row"
    fi
done < database/estudiantes.csv
html="${html/__TABLE__/$table}"
# final replacements and export
html="${html//__BASE__/../..}"
source final_replacer.sh
echo "$html" > ../timeline/$1/individual.html