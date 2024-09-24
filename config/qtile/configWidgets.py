from libqtile import bar, qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

from  globalVariables import *
# --------------------------------------------------------
# widgets configuration
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

widget_defaults = dict(
    font="Hack Nerd Font SemiBold",
    fontsize=12,
    padding=2,     
)


def initWidgets():
     # Power menu
    if showPowerMenu==True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.TextBox(
                **decor_rounded_left,
                background="#ffffff",
                foreground="#000000",             
                text=" ",
                fontsize=14,
                padding=2,
                mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(home + '/.config/qtile/scripts/powermenu.sh')},
            )
        ])
        
    # window name 
    if showWindowName == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.WindowName(    
                **decor_rounded_left,
                max_chars=50,
                background=Color10,
                width=400,
                padding=2,
            )
        ])
        
    # group box
    if showGroupBox == True:
        widget_list.extend([
            widget.Spacer(length=bar.STRETCH),
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
            widget.Spacer(length=bar.STRETCH)
        ])
        
    if showUpdates == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.CheckUpdates(
                **decor_rounded_left,
                background=Color10,       
                custom_command="checkupdates",
                execute="alacritty -e paru",
            )
        ])
    
    if showVolume == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.Volume(
                **decor_rounded_left,
                background=Color10,
                padding=2,
                fmt='Vol: {}',
            )         
        ])

    if showFreeDisk == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.DF(
                **decor_rounded_left,
                padding=2,
                background=Color10,        
                visible_on_warn=False,
                partition='/',
                format="{p} {uf}{m} ({r:.0f}%)"
            )            
        ])
    
    if showFreeHome == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.DF(
                **decor_rounded_left,
                padding=2,
                background=Color10,        
                visible_on_warn=False,
                partition='/home',
                format="{p} {uf}{m} ({r:.0f}%)"
            )            
        ])
        
    if showSysTray == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.Systray(
                **decor_rounded_left,              
            )          
        ])
        
    if showClock == True:
        widget_list.extend([
            widget.TextBox(**decor_rounded_right,),
            widget.Clock(
                **decor_rounded_left,
                background="#ffffff",
                foreground="#000000",   
                padding=2,      
                format="%a, %-d.%-m.%y %H:%S",
            )           
        ])