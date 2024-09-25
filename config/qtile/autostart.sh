#!/bin/bash

xrandr --output Virtual1 --primary --mode 1600x1200 --pos 0x0 --rotate normal

~/.config/qtile/scripts/changeWallpaper.sh

dunst &
blueman-applet &
nm-applet &
picom &
