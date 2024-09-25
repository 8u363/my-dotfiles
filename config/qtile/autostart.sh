#!/bin/bash

~/.config/qtile/scripts/changeWallpaper.sh

xrandr --output Virtual-1 --primary --mode 1600x1200 --pos 0x0 --rotate normal

dunst &
blueman-applet &
nm-applet &
picom &
