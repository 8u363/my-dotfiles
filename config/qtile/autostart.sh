#!/bin/bash

# wallpaper
./scripts/chnageWallpaper.sh

# systemtray
blueman-applet &
nm-applet &

# programs
picom &
