from libqtile import layout
from  globalVariables import *
# --------------------------------------------------------
# layout configuration
# --------------------------------------------------------
def initLayouts():
    layout_theme = {
        "margin":2,
        "border_width": 2,
        "border_focus": Color2,
        "border_normal": "#FFFFFF",
        "single_border_width": 3
    }

    layouts.extend([
        layout.MonadTall(**layout_theme),
        layout.MonadWide(**layout_theme),
        layout.Tile(**layout_theme),    
        layout.RatioTile(**layout_theme),    
    ])