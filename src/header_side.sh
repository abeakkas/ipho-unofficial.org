#!/bin/bash
# arguments:
# $1: index of element to be highlighted
header_side="$(cat templates/header_side.html)"
case $1 in
1) header_side="${header_side//__HIGHLIGHT_1__/highlight}" ;;
2) header_side="${header_side//__HIGHLIGHT_2__/highlight}" ;;
3) header_side="${header_side//__HIGHLIGHT_3__/highlight}" ;;
esac
header_side="${header_side//__HIGHLIGHT_1__/}"
header_side="${header_side//__HIGHLIGHT_2__/}"
header_side="${header_side//__HIGHLIGHT_3__/}"
