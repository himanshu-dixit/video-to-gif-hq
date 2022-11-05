#!/bin/sh

filename=$(basename -- "$1")
pattern_name="${1}.png"
gif_name="${1}.gif"
filters="fps=15,scale=1080:-1:flags=lanczos"

ffmpeg -v warning -i $1 -vf "$filters,palettegen" -y $pattern_name
ffmpeg -v warning -i $1 -i $pattern_name -lavfi "$filters [x]; [x][1:v] paletteuse=dither=floyd_steinberg" -y $gif_name

echo "created gif"