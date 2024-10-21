#   ___ _____ ___ _     _____    ____             __ _
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 

import json
# --------------------------------------------------------
# see https://docs.qtile.org/
# --------------------------------------------------------
import os
from pathlib import Path

from libqtile import bar, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from qtile_extras import widget

# --------------------------------------------------------
# general configuration
# --------------------------------------------------------
home = str(Path.home())  # get home path
mod = "mod4"  # windows key
terminal = "alacritty"
numerOfGroups = 6

# --------------------------------------------------------
# color configuration
# --------------------------------------------------------
colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
Color0 = (colordict['colors']['color0'])
Color1 = (colordict['colors']['color1'])
Color2 = (colordict['colors']['color2'])
Color3 = (colordict['colors']['color3'])
Color4 = (colordict['colors']['color4'])
Color5 = (colordict['colors']['color5'])
Color6 = (colordict['colors']['color6'])
Color7 = (colordict['colors']['color7'])
Color8 = (colordict['colors']['color8'])
Color9 = (colordict['colors']['color9'])
Color10 = (colordict['colors']['color10'])
Color11 = (colordict['colors']['color11'])
Color12 = (colordict['colors']['color12'])
Color13 = (colordict['colors']['color13'])
Color14 = (colordict['colors']['color14'])
Color15 = (colordict['colors']['color15'])

# --------------------------------------------------------
# key configuration
# --------------------------------------------------------
keys = [
    # general functions
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    Key([mod], "q", lazy.window.kill(), desc="Close the focused window"),
    Key([mod, "shift"], "q", lazy.spawn("sh " + home + '/.config/qtile/scripts/powermenu.sh'), desc="Show Powermenu"),

    # Group functions
    Key([mod], "Tab", lazy.next_layout(), desc="Use next layout on the actual group"),

    # Layout function
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),

    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),

    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),

    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Window functions
    Key([mod], "f", lazy.window.toggle_floating(), desc="Put the focused window to/from floating mode"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Put the focused window to/from fullscreen mode"),

    # Apps
    Key([mod], 'r', lazy.spawn('rofi -show run')),
    Key([mod], "w", lazy.spawn("sh " + home + "/.config/qtile/scripts/changeWallpaper.sh")),
    Key([mod], "b", lazy.spawn("brave"), desc="Launch browser"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # scratch pad
    Key([mod], 'e', lazy.group["6"].dropdown_toggle("explorer")),
    Key([mod], "F2", lazy.group["6"].dropdown_toggle("terminal")),
    Key([mod], "F3", lazy.group["6"].dropdown_toggle("nitrogen")),
    Key([mod], 'F4', lazy.group["6"].dropdown_toggle("btop")),

    # Audio functions
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
]

# --------------------------------------------------------
# group configuration
# --------------------------------------------------------
groups = [Group(i) for i in "123456"]
for vt in range(1, 6):
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
    DropDown("btop", "alacritty -e btop", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False),
    DropDown("explorer", "krusader", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False),
    DropDown("nitrogen", "nitrogen", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False),
    DropDown("terminal", terminal, x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False),
]))

# --------------------------------------------------------
# layout configuration
# --------------------------------------------------------
layout_theme = {
    "margin": 7,
    "border_width": 2,
    "border_focus": Color2,
    "border_normal": "#FFFFFF",
    "single_border_width": 2
}

layouts = [
    layout.Tile(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
]

# --------------------------------------------------------
# widget configuration
# --------------------------------------------------------
widget_defaults = dict(
    font="Hack Nerd Font Bold",
    fontsize=14,
    padding=2,
)

widgets_list = [
    widget.Spacer(length=5),

    widget.CurrentLayoutIcon(
        scale=0.7,
    ),

    widget.GroupBox(
        highlight_method='block',
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=['ffffff', 'ffffff'],
        block_highlight_text_color='000000',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff'
    ),

    widget.Spacer(length=5),

    widget.WindowName(
        foreground="#ffffff",
        max_chars=50,
        width=400,
    ),

    widget.Spacer(length=bar.STRETCH),

    widget.Clock(
        foreground="#ffffff",
        format="%a, %-d.%-m.%y %H:%S",
    ),

    widget.Spacer(length=bar.STRETCH),

    widget.CheckUpdates(
        foreground="#ffffff",
        custom_command="checkupdates",
        execute="alacritty -e paru",
    ),

    widget.Spacer(length=5),

    widget.Volume(
        foreground="#ffffff",
        fmt='\uf028  Vol: {}',
    ),

    widget.Spacer(length=5),

    widget.DF(
        foreground="#ffffff",
        visible_on_warn=False,
        partition='/',
        format="\uf1c0  {p} {uf}{m} ({r:.0f}%)"
    ),

    widget.Spacer(length=5),

    widget.DF(
        foreground="#ffffff",
        visible_on_warn=False,
        partition='/home',
        format="\uf1c0  {p} {uf}{m} ({r:.0f}%)"
    ),

    widget.Spacer(length=5),

    widget.Systray(
    ),

    widget.Spacer(length=5),
]

# --------------------------------------------------------
# screen configuration
# --------------------------------------------------------
screens = [
    Screen(
        top=bar.Bar(
            widgets_list,
            40,
            opacity=0.7,
            border_width=[0, 0, 0, 0],
            margin=[0, 0, 0, 0],
            background="#00000000"
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

"""

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
# autostart configuration
# --------------------------------------------------------
@ hook.subscribe.startup_once
def autostart():
    autostartPath = os.path.expanduser(home + '/.config/qtile/autostart.sh')
    subprocess.run([autostartPath])

# --------------------------------------------------------
# gernal configuration
# --------------------------------------------------------
dgroups_key_binder          = None
dgroups_app_rules           = []  # type: list
follow_mouse_focus          = True
bring_front_click           = False
floats_kept_above           = True
cursor_warp                 = False

auto_fullscreen             = True
focus_on_window_activation  = "smart"
reconfigure_screens         = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize               = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules              = None

# xcursor theme (string or None) and size (integer) for Wayland backend
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
initGroups()

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
"""
