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
import subprocess
from pathlib import Path

from libqtile import bar, layout, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)

# --------------------------------------------------------
# autostart configuration
# --------------------------------------------------------
@hook.subscribe.startup_once
def autostart():
    autostartPath = os.path.expanduser(home + '/.config/qtile/autostart.sh')
    subprocess.run([autostartPath])


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
Color0 = "#4A4947"
Color1 = "#FAF7F0"
Color2 = "#FD8B51"
Color3 = "#FFC94A"
Color4 = "#257180"
Color5 = "#CB6040"

def show_power_menu(qtile):
    controls = [
        PopupImage(
            filename="~/.config/qtile/icons/logout.png",
            pos_x=0.15,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            mouse_callbacks={
                "Button1": lazy.shutdown()
            }
        ),
        PopupImage(
            filename="~/.config/qtile/icons/reboot.png",
            pos_x=0.45,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl reboot")
            }
        ),
        PopupImage(
            filename="~/.config/qtile/icons/shutdown.png",
            pos_x=0.75,
            pos_y=0.1,
            width=0.1,
            height=0.5,
            mouse_callbacks={
                "Button1": lazy.spawn("systemctl poweroff")
            }
        ),
        PopupText(
            text="Logout",
            pos_x=0.1,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Reboot",
            pos_x=0.4,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Power Off",
            pos_x=0.7,
            pos_y=0.7,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
    ]

    layout = PopupRelativeLayout(
        qtile,
        width=1000,
        height=200,
        controls=controls,
        background="00000060",
        initial_focus=None,
    )

    layout.show(centered=True)

# --------------------------------------------------------
# key configuration
# --------------------------------------------------------
keys = [
    # general functions
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    Key([mod], "q", lazy.window.kill(), desc="Close the focused window"),
    Key([mod, "shift"], "q", lazy.function(show_power_menu)),

    Key([mod], "Space", lazy.spawn('betterlockscreen -l dim')),

    # Group functions
    Key([mod], "Tab", lazy.next_layout(), desc="Use next layout on the actual group"),

    # Layout function
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),

    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),

    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),

    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Window functions
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Put the focused window to/from fullscreen mode"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Put the focused window to/from floating mode"),

    # Apps
    Key([mod], "r", lazy.spawn('rofi -show run')),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.spawn("sh " + home + "/.config/qtile/scripts/changeWallpaper.sh")),

    # scratch pad
    Key([mod], 'e', lazy.group["6"].dropdown_toggle("explorer")),
    Key([mod], "F2", lazy.group["6"].dropdown_toggle("terminal")),
    Key([mod], 'F3', lazy.group["6"].dropdown_toggle("btop")),

    # Audio functions
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
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
    "border_normal": Color1,
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
spacerLength=5
iconFontSize=16

widget_defaults = dict(
    font="Hack Nerd Font Bold",
    fontsize=14,
    padding=2,
)

widgets_list = [
    widget.Spacer(length=spacerLength),

    widget.CurrentLayoutIcon(
        scale=0.5,
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.GroupBox(
        margin_x = 1,
        margin_y = 4,
        padding_y = 3,
        padding_x = 3,
        borderwidth = 2.5,
        active = Color1,
        inactive = Color0,
        this_current_screen_border = Color5,
        rounded = True,
        highlight_method = "block",
        center_aligned = True,
        disable_drag = True,
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = "󰖟 ",
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(brave)}
    ),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = "󰇮 ",
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(thunderbird)}
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),


    widget.WindowName(
        foreground=Color1,
        max_chars=50,
        width=400,
    ),

    widget.Spacer(length=bar.STRETCH),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " ",
    ),

    widget.Clock(
        foreground=Color1,
        format="%A, %-d.%-m.%y",
    ),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " 󰥔 ",
    ),

    widget.Clock(
        foreground=Color1,
        format="%H:%M",
    ),

    widget.Spacer(length=bar.STRETCH),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = "  ",
    ),

    widget.CheckUpdates(
        foreground=Color1,
        custom_command="checkupdates",
        execute="alacritty -e paru",
        display_format=" {updates}",
        no_update_string= "-",
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " ",
    ),

    widget.Volume(
        foreground=Color1,
        fmt=' {}',
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " ",
    ),

    widget.DF(
        foreground=Color1,
        visible_on_warn=False,
        partition='/',
        format="{p} {uf}{m} ({r:.0f}%)"
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " ",
    ),

    widget.DF(
        foreground=Color1,
        visible_on_warn=False,
        partition='/home',
        format="{p} {uf}{m} ({r:.0f}%)"
    ),

    widget.Spacer(length=spacerLength),
    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),
    widget.Spacer(length=spacerLength),

    widget.Systray(
    ),

    widget.Spacer(length=spacerLength),

    widget.TextBox(
        foreground=Color4,
        text = "|",
    ),

    widget.TextBox(
        fontsize=iconFontSize,
        foreground=Color3,
        text = " ",
        mouse_callbacks={"Button1": lambda: qtile.function(show_power_menu)}
    ),

    widget.Spacer(length=spacerLength),
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
