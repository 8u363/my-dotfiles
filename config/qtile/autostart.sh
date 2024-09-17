#!/bin/bash

# wallpaper
feh --bg-scale --randomize ~/git/my-wallpaper/art &
#

# systemtray
blueman-applet &
nm-applet &

# programs
picom &
