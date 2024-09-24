from libqtile import qtile
from libqtile.config import Group, Key, DropDown, ScratchPad
from libqtile.lazy import lazy

from  globalVariables import *

# --------------------------------------------------------
# group configuration
# --------------------------------------------------------

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
def initGroups():
    for i in range(1, numerOfGroups):
        groups.append(Group(i))
        
        keys.append(
            Key(
                ["control", "mod1"],
                f"f{i}",
                lazy.core.change_vt(i).when(func=lambda: qtile.core.name == "wayland"),
                desc=f"Switch to VT{i}",
            )
        )
               
        keys.extend(
            [
                # mod + group number = switch to group
                Key(
                    [mod],
                    str(i),
                    lazy.group[str(i)].toscreen(),
                    desc="Switch to group {}".format(str(i)),
                ),
                # mod + shift + group number = switch to & move focused window to group
                Key(
                    [mod, "shift"],
                    str(i),
                    lazy.window.togroup(str(i), switch_group=True),
                    desc="Switch to & move focused window to group {}".format(str(i)),
                ),
            ]
        )
        
    groups.append(ScratchPad(numerOfGroups, [        
    DropDown("btop", "alacritty -e btop", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),    
    DropDown("explorer", "krusader", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),   
    DropDown("nitrogen", "nitrogen", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False  ),     
    DropDown("terminal", "alacritty", x=0.1, y=0.1, width=0.80, height=0.80, on_focus_lost_hide=False ),
]))