#!/bin/bash

# set a random wallpaper
feh --bg-scale --randomize ~/git/my-wallpaper/art

# get last set deskcop wallpaper
wallpaper="$(cat "${HOME}/.fehbg" | awk -F "'" '{print $2}')"

# set pywal color scheme
wal -i $wallpaper

# reload the qtile config
qtile cmd-obj -o cmd -f reload_config