
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
# --------------------------------------------------------
# General Variables
# --------------------------------------------------------
showHomePartion = False
home            = str(Path.home())  # get home path
mod             = "mod4"            # windows key
terminal        = "alacritty"

# --------------------------------------------------------
# General key binding
# --------------------------------------------------------
keys = [
    # General functions
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "x", lazy.shutdown(), desc="Close the whole Qtile"),
    Key([mod], "space", lazy.spawncmd(), desc= "Open command prompt on the bar"),
    Key([mod], 'r', lazy.spawn('rofi -show run')),
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
    # Apps
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
    DropDown("btop", "alacritty -e btop", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),    
    DropDown("explorer", "krusader", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),   
    DropDown("nitrogen", "nitrogen", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),     
    DropDown("terminal", "alacritty", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False ),
]))

keys.extend([
    Key([mod], "Return", lazy.group["6"].dropdown_toggle("terminal")),
    Key([mod], 'e', lazy.group["6"].dropdown_toggle("explorer")),
    Key([mod], 'F10', lazy.group["6"].dropdown_toggle("btop")),
    Key([mod], 'F11', lazy.group["6"].dropdown_toggle("nitrogen")),
    ])



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
    font="Hack Nerd Font SemiBold",
    fontsize=14,
    padding=3,     
    )

extension_defaults = widget_defaults.copy()
# --------------------------------------------------------
# Pywal Colors
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

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------
layout_theme = {
    "margin":2,
    "border_width": 2,
    "border_focus": Color2,
    "border_normal": "FFFFFF",
    "single_border_width": 3
}


layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),    
    layout.RatioTile(**layout_theme),    
]
    
# --------------------------------------------------------
# Widgets
# --------------------------------------------------------
decor_rounded_right={
    "decorations": [
        PowerLineDecoration(path="rounded_right")        
    ],       
}

decor_rounded_left={
    "decorations": [
        PowerLineDecoration(path="rounded_left")        
    ],   
}

widget_list = [
    widget.CurrentLayoutIcon(background=Color15,),

    # workspace numbers
    widget.TextBox(**decor_rounded_right,),
    widget.GroupBox(  
        **decor_rounded_left,      
        background="#ffffff",
        highlight_method='block',
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=['ffffff','ffffff'],
        block_highlight_text_color='000000',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff'
    ),
         
    # window name    
    widget.TextBox(**decor_rounded_right,),
    widget.WindowName(    
        **decor_rounded_left,
        max_chars=50,
        background=Color2,
        width=400,
        padding=5
    ),         

    # clock
    widget.Spacer(length=bar.STRETCH),
    widget.TextBox(**decor_rounded_right,),
    widget.Clock(
        **decor_rounded_left,
        background="#ffffff",
        foreground="#000000",   
        padding=5,      
        format="%a, %d.%m.%Y %H:%S",
    ), 
    widget.Spacer(length=bar.STRETCH),

    # volume
    widget.TextBox(**decor_rounded_right,),
    widget.Volume(
        **decor_rounded_left,
        background=Color10 +".4",
        padding=5, 
        fmt='Vol: {}',
    ),
    
    widget.TextBox(**decor_rounded_right,),
    widget.DF(
        **decor_rounded_left,
        padding=5, 
        background=Color8+".4",        
        visible_on_warn=False,
        partition='/',
        format="{p} {uf}{m} ({r:.0f}%)"
    ),


    widget.TextBox(**decor_rounded_right,),
    widget.DF(
        **decor_rounded_left,
        padding=5, 
        background=Color8+".4",        
        visible_on_warn=False,
        partition='/home',
        format="{p} {uf}{m} ({r:.0f}%)"
    ),

    # system tray
    widget.TextBox(**decor_rounded_right,),
    widget.Systray(
        **decor_rounded_left,        
    ),  
    
    # Power menu
    widget.TextBox(**decor_rounded_right,),
    widget.TextBox(
        **decor_rounded_left,
        background=Color15+".4",     
        padding=5,    
        text=" ",
        fontsize=20,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + '/.config/qtile/scripts/powermenu.sh')},
    ),
]    


if (showHomePartion==False):
    del widget_list[13:15]

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