#!/bin/bash
declare -a ordinals
# this will be outdated in 2270 :P
for i in $(seq 0 200)
do
    case "$(( $i % 10 ))" in
    1) ordinals[$i]="st" ;;
    2) ordinals[$i]="nd" ;;
    3) ordinals[$i]="rd" ;;
    *) ordinals[$i]="th" ;;
    esac
done
