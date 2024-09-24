from pathlib import Path
from libqtile.config import  Key
from libqtile.lazy import lazy

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
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    
    # Audio functions
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute/Unmute Volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),    
]