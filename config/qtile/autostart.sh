#!/bin/bash

xrandr --output Virtual1 --primary --mode 1600x900 --pos 0x0 --rotate normal

~/.config/qtile/scripts/setDefaultWallpaper.sh

dunst &
blueman-applet &
nm-applet &
picom &
