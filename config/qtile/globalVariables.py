import os
import json
from pathlib import Path
from libqtile.config import Group

keys            = []   
groups          = [Group(i) for i in "123456"]
widget_list     = []
layouts         = []

home            = str(Path.home())  # get home path
mod             = "mod4"            # windows key
terminal        = "alacritty"
numerOfGroups   = 6

# --------------------------------------------------------
# widget configuration
# --------------------------------------------------------
showPowerMenu   = True
showWindowName  = True
showGroupBox    = True
showUpdates     = True
showVolume      = True
showFreeDisk    = True
showFreeHome    = False
showSysTray     = True
showClock       = True

# --------------------------------------------------------
# color configuration
# --------------------------------------------------------
colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
Color0=(colordict['colors']['color0'])
Color1=(colordict['colors']['color1'])
Color2=(colordict['colors']['color2'])
Color3=(colordict['colors']['color3'])
Color4=(colordict['colors']['color4'])
Color5=(colordict['colors']['color5'])
Color6=(colordict['colors']['color6'])
Color7=(colordict['colors']['color7'])
Color8=(colordict['colors']['color8'])
Color9=(colordict['colors']['color9'])
Color10=(colordict['colors']['color10'])
Color11=(colordict['colors']['color11'])
Color12=(colordict['colors']['color12'])
Color13=(colordict['colors']['color13'])
Color14=(colordict['colors']['color14'])
Color15=(colordict['colors']['color15'])