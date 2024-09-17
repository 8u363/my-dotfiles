
#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 

# --------------------------------------------------------
# see https://docs.qtile.org/
# --------------------------------------------------------

import subprocess
import os
import json

from libqtile import bar, hook,layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder

from pathlib import Path
from colors import gruvbox

from bar1 import bar

# --------------------------------------------------------
# General Variables
# --------------------------------------------------------
home        = str(Path.home())  # get home path
mod         = "mod4"            # windows key
terminal    = "alacritty"

# --------------------------------------------------------
# General key binding
# --------------------------------------------------------
keys = [
    # General functions
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "x", lazy.shutdown(), desc="Close the whole Qtile"),
    Key([mod], "space", lazy.spawncmd(), desc= "Open command prompt on the bar"),
        
    # Group functions
    Key([mod], "Tab", lazy.next_layout(), desc="Use next layout on the actual group"), 
    
    # Layout function
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
        
    # Window functions       
    Key([mod], "x", lazy.window.kill(), desc="Close the focused window"),
    Key([mod], "f", lazy.window.toggle_floating(), "Put the focused window to/from fullscreen mode"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), "Put the focused window to/from fullscreen mode"),

    # Screen functions
    Key([mod], "w", lazy.spawn("sh " + home +"/.config/qtile/scripts/changeWallpaper.sh" )),
    Key([mod, "shift"], "w", lazy.spawn("nitrogen")),
    
    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("brave"), desc="Launch browser"),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------
# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 6):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456"]

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

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------
groups.append(ScratchPad("6", [        
    DropDown("btop", "alacritty -e btop", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),    
    DropDown("thunar", "thunar", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),    
]))

keys.extend([
    Key([mod], 'F9', lazy.group["6"].dropdown_toggle("thunar")),
    Key([mod], 'F10', lazy.group["6"].dropdown_toggle("btop")),
    
    ])

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------
layout_theme = {
        "margin":5,
        "border_width": 2,
        "border_normal": gruvbox['black'],
        "border_focus": gruvbox['cyan'],
    }


layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    
    # Try more layouts by unleashing below layouts.    
    layout.Tile(**layout_theme),    
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),            
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
# Widgets
# --------------------------------------------------------
widget_defaults = dict(
    font="monospace",
    fontsize=12,
    padding=3, 
    #bacgkround=gruvbox['bg'],
    )

extension_defaults = widget_defaults.copy()

screens = [
    Screen(top=bar)
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
wmname = "LG3D"

@ hook.subscribe.startup_once
def autostart():
    autostartPath = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([autostartPath])