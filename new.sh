#!/bin/sh

filename=$(basename -- "$1")
palette="./palette.png"
filters="fps=15,scale=1080:-1:flags=lanczos"

ffmpeg -v warning -i $1 -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i $1 -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse=dither=floyd_steinberg" -y new.gif