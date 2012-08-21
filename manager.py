import nukescripts
import nuke
import re
import os
from glob import glob


#import defineShows

env_check = os.environ.get('NKASSETS')


def shows(SHOWsn):
    SHOWS_dict = {'library':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j00000_library',
    'pitches':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j00000_pitches',
    'playground':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j00000_playground',
    'georgia':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j0001_georgia',
    'man':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j27327_mankind',
    'gen':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j27865_generation_earth',
    'ww2':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j28448_ww2fs',
    'wbu':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j28777_worlds_busiest',
    'ign':'\\\\bcastvfxraid\\RAID\\CURRENT_PROJECTS\\j28973_ignition'}
    
    if SHOWsn in SHOWS_dict:
        SHOWln = SHOWS_dict[SHOWsn]
        return SHOWln
    else:
        return 0

#Create Asset Management and Shot Selection Panel


myPanel = nuke.Panel("ShotSetup")

myPanel.addSingleLineInput("Shot: ", "")
userInput = nuke.getInput( 'Setup: ', 'Your Shot name' ).replace( ' ', '')
if userInput:
	for n in nuke.selectedNodes():
		n['value'] = 0
		pass
	else:
		parts = userInput.split('_')



def newParts():
	
	SHOWsn = (parts[0])
	SHOWln = (shows(SHOWsn))
	if SHOWln == 0:
		EP = ""
		SEQ = ""
		SHOT = ""
		print "shot not found"
		return (SHOWsn, SHOWln, EP, SEQ, SHOT)
	EP = (parts[1])
	SEQ = (parts[0] + "_%s" % parts[1]+ "_%s" % parts [2])
	SHOT = userInput
	
	return (SHOWsn, SHOWln, EP, SEQ, SHOT)
		

SHOWsn, SHOWln, EP, SEQ, SHOT = newParts()
print SHOWsn, SHOWln, EP, SEQ, SHOT

	
def checkNew(): 
	nodeClass = nuke.thisNode().Class() 
	if nodeClass == 'Root': 
		newParts() 
		return 

# Register the callback 
nuke.addOnUserCreate(checkNew)
	
def nukeDir():

	showParts = newParts()
	if showParts == 0:
		return
	#SHOWln = showParts[1]
	nkDir = os.path.join(SHOWln, "%s" % EP, "%s" % SEQ, "%s" % SHOT, 'nuke', os.environ['USERNAME'], 'scripts')
	pathCheck = os.path.join(SHOWln, "%s" % EP, "%s" % SEQ, "%s" % SHOT)
	if os.path.isdir(pathCheck):
            if not os.path.isdir(nkDir):
                os.makedirs(nkDir)
	else:
            nuke.message("Shot does not exist")
            nuke.load("panel")
	    #raise ValueError, 'directory does not exist'          
            print 'Shot does not exist.'
            
	return nkDir
	
	
# DEFINE EASY SAVE


def easySave():
    nkDir = nukeDir()
    # GET DESCRIPTION FROM USER BUT STRIP ALL WHITE SPACES
    description = nuke.getInput( 'script description', 'Your Comp name' ).replace( ' ', '' )

    fileSaved = False
    version = 1
    while not fileSaved:
        # CONSTRUCT FILE NAME
        nkName = '%s_%s_%03d.nk' % (SHOT,description, version)
        # JOIN DIRECTORY AND NAME TO FORM FULL FILE PATH
        nkPath = os.path.join( nkDir, nkName )
        # IF FILE EXISTS VERSION UP
        if os.path.isfile( nkPath ):
            version += 1
            continue
        # SAVE NUKE SCRIPT
        nuke.scriptSaveAs( nkPath )
        fileSaved = True
    return nkPath



# ADD EASY SAVE TO SHOT MENU								    
shotMenu = '%s' % ( SHOT )
nuke.menu( 'Nuke' ).addCommand( shotMenu+'/Easy Save', easySave )
#nuke.menu('Nuke').addCommand( shotMenu+'/Write Assets', 'nuke.createNode("WriteAssets")')

# REQUIRE VERSIONING IN SCRIPT NAME
def checkScriptName():
    if not re.search( r'[vV]\d+', nuke.root().name() ):
		raise NameError, 'Please include a version number and save script again.'
nuke.addOnScriptSave( checkScriptName )

# GET ALL NUKE SCRIPTS FOR CURRENT SHOT
def getNukeScripts():
    nkFiles = glob( os.path.join( nukeDir(), '*.nk' ) )
    return nkFiles

# PANEL TO SHOW NUKE SCRIPTS FOR CURRENT SHOT
class NkPanel( nukescripts.PythonPanel ):
    def __init__( self, nkScripts ):
		nukescripts.PythonPanel.__init__( self, 'Open NUKE Script' )
		self.checkboxes = []
		self.nkScripts = nkScripts
		self.selectedScript = ''

		for i, n in enumerate( self.nkScripts ):
		    # PUT INDEX INTO KNOB NAMES SO WE CAN IDENTIFY THEM LATER
		    k = nuke.Boolean_Knob( 'nk_%s' % i, os.path.basename( n ) )
		    self.addKnob( k )
		    k.setFlag( nuke.STARTLINE )
		    self.checkboxes.append( k )

    def knobChanged( self, knob ):
		if knob in self.checkboxes:
		    # MAKE SURE ONLY ONE KNOB IS CHECKED
		    for cb in self.checkboxes:
				if knob == cb:
				    # EXTRACT THE INDEX FORM THE NAME AGAIN
				    index = int( knob.name().split('_')[-1] )
				    self.selectedScript = self.nkScripts[ index ]
				    continue
				cb.setValue( False )
		    
# HELPER FUNCTION FOR NUKE SCRIPT PANEL
def nkPanelHelper():
		# GET ALL NUKE SCRIPTS FOR CURRENT SHOT
		nkScripts = getNukeScripts()
		if not nkScripts:
				# IF THERE ARE NONE DON'T DO ANYTHING
				return
		# CREATE PANEL
		p = NkPanel( nkScripts )
		# ADJUST SIZE
		p.setMinimumSize( 200, 200 )

		# IF PANEL WAS CONFIRMED AND A NUKE SCRIPT WAS SELECTED, OPEN IT
		if p.showModalDialog():
				if p.selectedScript:
						nuke.scriptOpen( p.selectedScript )


	   

if SHOWln and SHOT != 0:
	##Execute this
	#myLabel = os.path.join(newParts)
	myPath = os.path.join(SHOWln, "%s" % EP, "%s" % SEQ, "%s" % SHOT)
	#myPath3D = os.path.join(SHOWln, "%s" % EP, "%s" % SEQ, "%s" % SHOT)
	nuke.addFavoriteDir('Nuke Scripts', nukeDir())
	nuke.addFavoriteDir('Shot Directory', myPath)
	#nuke.addFavoriteDir('3D Renders', myPath/release)
	
else:
	print 'shot does not exist'

	
	


