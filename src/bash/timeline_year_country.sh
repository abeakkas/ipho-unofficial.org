#!/bin/bash
# arguments:
# $1: year of IPhO to be created
# $2: previous year if exists, 0 otherwise
# $3: next year if exists, 0 otherwise
# $4: number of IPhO to be created
echo "Creating timeline/$1/country"
# imports
source countrycodes.sh
source ordinals.sh
source header_side.sh 1
source footer.sh
# load file and replace basics
html="$(cat templates/timeline/year/country.html)"
html="${html//__HEADER_SIDE__/$header_side}"
html="${html//__FOOTER__/$footer}"
# Replacing year information
html="${html//__NUMBER__/$4}"
html="${html//__ORDINAL__/${ordinals[$4]}}"
html="${html//__YEAR__/$1}"
if [ $2 != 0 ]
then
    previous_year_html="$(cat templates/timeline/year/country_previous_year.html)"
    previous_year_html="${previous_year_html//__PREVIOUS_YEAR__/$2}"
    html="${html//__PREVIOUS_YEAR__/$previous_year_html}"
else
    html="${html//__PREVIOUS_YEAR__/}"
fi
if [ $3 != 0 ]
then
    next_year_html="$(cat templates/timeline/year/country_next_year.html)"
    next_year_html="${next_year_html//__NEXT_YEAR__/$3}"
    html="${html//__NEXT_YEAR__/$next_year_html}"
else
    html="${html//__NEXT_YEAR__/}"
fi
unset medals
declare -A medals
while IFS=, read name code year rank medal newline
do 
    if [ $1 == $year ]
    then
        if [ $((${medals[$code]}+0)) == 0 ]
        then
            # this is to make sure countries with same medals are ranked by their best competitors
            medals[$code]=$((1000-$rank))
        fi
        case $medal in
        1) ((medals[$code]+=1000000)) ;;
        2) ((medals[$code]+=100000)) ;;
        3) ((medals[$code]+=10000)) ;;
        4) ((medals[$code]+=1000)) ;;
        esac
    fi
done < database/estudiantes.csv

# Creating table
table=""
rowt="$(cat templates/timeline/year/country_row.html)"
i=0
if [ ${#medals[@]} != 0 ]
then
    while IFS=, read code medal newline
    do
        ((i++))
        row="$rowt"
        row="${row//__CODE__/$code}"
        row="${row//__COUNTRY__/${countrycodes[$code]}}"
        row="${row//__RANK__/$i}"
        row="${row//__GOLD__/$((medal/1000000%10))}"
        row="${row//__SILVER__/$((medal/100000%10))}"
        row="${row//__BRONZE__/$((medal/10000%10))}"
        row="${row//__HONOURABLE__/$((medal/1000%10))}"
        table+="$row"
    done <<< "$(for k in "${!medals[@]}"; do echo $k","${medals["$k"]}"," ${medals["$k"]} $'\n'; done | sort -rn -k2)"
fi
html="${html/__TABLE__/$table}"
# final replacements and export
html="${html//__BASE__/../..}"
source final_replacer.sh
echo "$html" > ../timeline/$1/country.html