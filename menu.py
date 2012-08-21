import os
import nuke
import nukescripts
import autowrite
import browseDir
import SubmitToDeadline


## Loading asset manager
nuke.load("manager")
nuke.load("panel")

nuke.load ("environment")

def addManagementPanel():
    return assetManagerPanel().addToPane()

menu = nuke.menu('Pane')
menu.addCommand('Project Management Settings', addManagementPanel)
nukescripts.registerPanel( 'assetpanel', addManagementPanel)


# Browse Directory
nuke.menu( 'Nuke' ).addCommand( 'Scripts/Browse/Node\'s file path', "browseDir.browseDirByNode()", 'shift+b' )



## Submit to Deadline
tb = menubar.addMenu("&Submit") 
tb.addCommand("Submit To Deadline", SubmitToDeadline.main, "")
