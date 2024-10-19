
#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 

# --------------------------------------------------------
# see https://docs.qtile.org/
# --------------------------------------------------------

import os
import subprocess
from pathlib import Path

from libqtile import bar, layout, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration


from globalVariables import *
from configKeys import initKeys
#from configGroups import initGroups
from configWidgets import initWidgets
from configLayouts import initLayouts

keys            = []   
groups          = [Group(i) for i in "123456"]
widget_list     = []
layouts         = []

home            = str(Path.home())  # get home path
mod             = "mod4"            # windows key
terminal        = "alacritty"
numerOfGroups   = 6

# --------------------------------------------------------
# autostart configuration
# --------------------------------------------------------
@hook.subscribe.startup_once
def autostart():
    autostartPath = os.path.expanduser(home + '/.config/qtile/autostart.sh')
    subprocess.run([autostartPath])

# --------------------------------------------------------
# gernal configuration
# --------------------------------------------------------
dgroups_key_binder          = None
dgroups_app_rules           = []
follow_mouse_focus          = True
bring_front_click           = False
floats_kept_above           = True
cursor_warp                 = False
auto_fullscreen             = True
focus_on_window_activation  = "smart"
reconfigure_screens         = True
auto_minimize               = True
wl_input_rules              = None
wl_xcursor_theme            = None
wl_xcursor_size             = 24
wmname = "QTILE"

# --------------------------------------------------------
# key configuration
# --------------------------------------------------------
initKeys()

# --------------------------------------------------------
# group configuration
# --------------------------------------------------------
for vt in range(1, numerOfGroups):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )
    
groups.append(ScratchPad("6", [        
    DropDown("btop", "alacritty -e btop", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),    
    DropDown("explorer", "krusader", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),   
    DropDown("nitrogen", "nitrogen", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),     
    DropDown("terminal", terminal , x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False ),
]))

# --------------------------------------------------------
# widget configuration
# --------------------------------------------------------
initWidgets()

# --------------------------------------------------------
# layout configuration
# --------------------------------------------------------
initLayouts()

# --------------------------------------------------------
# screen configuration
# --------------------------------------------------------
screens = [
    Screen(
        top=bar.Bar(
            widget_list,
            40,
            padding=20,
            opacity=0.7,
            border_width=[0, 0, 0, 0],
            margin=[0,0,0,0],
            background="#000000.3"
        ),
    ),
]

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# --------------------------------------------------------
# mouse configuration
# --------------------------------------------------------
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]