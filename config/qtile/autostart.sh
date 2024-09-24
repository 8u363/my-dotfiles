#!/bin/bash

# wallpaper
~/.config/qtile/scripts/changeWallpaper.sh

# systemtray
blueman-applet &
nm-applet &

# programs
picom &
