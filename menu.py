import os
import nuke
import nukescripts



## Loading asset manager
nuke.load("manager")
nuke.load("panel")

nuke.load ("environment")

def addManagementPanel():
    return assetManagerPanel().addToPane()

menu = nuke.menu('Pane')
menu.addCommand('Project Management Settings', addManagementPanel)
nukescripts.registerPanel( 'assetpanel', addManagementPanel)


