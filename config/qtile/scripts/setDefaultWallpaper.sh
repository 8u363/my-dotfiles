#!/bin/bash

# set a random wallpaper
feh --bg-scale ~/.config/qtile/wallpaper/default.jpg

# get last set deskcop wallpaper
wallpaper="$(cat "${HOME}/.fehbg" | awk -F "'" '{print $2}')"

# set pywal color scheme
wal -i $wallpaper

# reload the qtile config
qtile cmd-obj -o cmd -f reload_config