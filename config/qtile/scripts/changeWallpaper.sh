#!/bin/bash

feh --bg-scale --randomize ~/git/my-wallpaper/art

# Get current wallpaper 
wallpaper="$(cat "${HOME}/.fehbg" | awk -F "'" '{print $2}')"

#Apply pywal color scheme to desktop
wal -i $wallpaper