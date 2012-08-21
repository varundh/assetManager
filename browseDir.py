#nuke.menu( 'Nuke' ).addCommand( 'Scripts/Browse/Node\'s file path', "browseDir.browseDirByNode()", 'shift+b' )



import nuke
import sys
import os
import subprocess



def browseDirByNode():
       try:
           f = os.path.dirname(nuke.selectedNode().knob( "file" ).evaluate()).replace("/","\\")
       except:
           a = nuke.root().name().split("/")
           f = "/".join(a[0:-1]).replace("/","\\")
       subprocess.Popen('explorer '+f)

