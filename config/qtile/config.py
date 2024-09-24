
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
import json
from pathlib import Path

from libqtile import bar, layout, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration


from globalVariables import *
from configKeys import initKeys
from configGroups import initGroups
from configWidgets import initWidgets
from configLayouts import initLayouts

# --------------------------------------------------------
# key configuration
# --------------------------------------------------------
initKeys()

# --------------------------------------------------------
# group configuration
# --------------------------------------------------------
initGroups()

# --------------------------------------------------------
# widget configuration
# --------------------------------------------------------
initWidgets()

# --------------------------------------------------------
# layout configuration
# --------------------------------------------------------
initLayouts()



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

screens = [
    Screen(
        top=bar.Bar(
            widget_list,
            30,
            padding=20,
            opacity=0.7,
            border_width=[0, 0, 0, 0],
            margin=[0,0,0,0],
            background="#000000.3"
        ),
    ),
]

# --------------------------------------------------------
# Mouse configuration
# --------------------------------------------------------
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "QTILE"

@ hook.subscribe.startup_once
def autostart():
    autostartPath = os.path.expanduser(home + '/.config/qtile/autostart.sh')
    subprocess.run([autostartPath])