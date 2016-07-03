#!/bin/bash
# arguments:
# $1: country code to be created
# $2: previous country code if exists, "" otherwise
# $3: next country code if exists, "" otherwise
echo "Creating countries/$1/index"
# imports:
source countrycodes.sh
source header_side.sh 2
source footer.sh
# load file:
html="$(cat templates/countries/code/index.html)"
# replace templates:
html="${html/__HEADER_SIDE__/$header_side}"
html="${html/__FOOTER__/$footer}"
# Read from CSV
while IFS=, read code country nationalsite newline
do
    if [ "$code" == "$1" ]
    then
        if [ "$nationalsite" != "" ]
        then
            temp="$(cat templates/countries/code/index_contact.html)"
            temp="${temp//__LINK__/$nationalsite}"
            html="${html//__CONTACT__/$temp}"
        else
            html="${html//__CONTACT__/}"
        fi
        # as inefficient as possible
        hosts=""
        while IFS=, read number year date _code city homepage p_country p_student gold silver bronze honourable newline
        do 
            if [ "$code" == "$_code" ]
            then
                temp="$(cat templates/countries/code/index_host.html)"
                temp="${temp//__YEAR__/$year}"
                if [ "$city" != "" ]
                then
                    temp="${temp//__CITY__/ - $city}"
                else
                    temp="${temp//__CITY__/}"
                fi
                if [ "$homepage" != "" ]
                then
                    temppage="$(cat templates/countries/code/index_host_homepage.html)"
                    temppage="${temppage//__LINK__/$homepage}"
                    temppage="${temppage//__YEAR__/$year}"
                    temp="${temp//__HOMEPAGE__/$temppage}"
                else
                    temp="${temp//__HOMEPAGE__/}"
                fi
                hosts="$hosts$temp"
            fi
        done < database/timeline.csv
        if [ "$hosts" != "" ]
        then
            hosts="<dt>IPhO Host</dt>$hosts"
        fi
        if [ "$2" != "" ]
        then
            temp="$(cat templates/countries/code/index_previous_country.html)"
            temp="${temp//__CODE__/$2}"
            html="${html/__PREVIOUS_COUNTRY__/$temp}"
        else
            html="${html/__PREVIOUS_COUNTRY__/}"
        fi
        if [ "$3" != "" ]
        then
            temp="$(cat templates/countries/code/index_next_country.html)"
            temp="${temp//__CODE__/$3}"
            html="${html/__NEXT_COUNTRY__/$temp}"
        else
            html="${html/__NEXT_COUNTRY__/}"
        fi
        html="${html/__HOST__/$hosts}"
        html="${html//__CODE__/$1}"
        html="${html//__COUNTRY__/${countrycodes[$1]}}"
        firstparticipation=10000 # come find me at year 10000
        participation=0
        participation_year=0 # dummy variable
        gold=0
        silver=0
        bronze=0
        honourable=0
        while IFS=, read name code year rank medal newline
        do
            if [ "$code" == "$1" ]
            then
                if [ $year -lt $firstparticipation ]
                then
                    firstparticipation=$year
                fi
                if [ $year != $participation_year ]
                then
                    participation_year=$year
                    ((participation++))
                fi
                case $medal in
                1) ((gold++)) ;;
                2) ((silver++)) ;;
                3) ((bronze++)) ;;
                4) ((honourable++)) ;;
                esac
            fi
        done < database/estudiantes.csv
        html="${html//__FIRST_PARTICIPATION__/$firstparticipation}"
        html="${html//__PARTICIPATION__/$participation}"
        html="${html//__GOLD__/$gold}"
        html="${html//__SILVER__/$silver}"
        html="${html//__BRONZE__/$bronze}"
        html="${html//__HONOURABLE__/$honourable}"
    fi
done < database/countries.csv

html="${html//__BASE__/../..}"
source final_replacer.sh
# write
echo "$html" > ../countries/$1/index.html