from proj_2 import *
from omegaToolkit import *


def drawContainer(self, column, row, container):
	print "test"

dataDir = './data/'
caveSystem = None

#	read file and creates the planetary database:
list = readPlanetarySystemFile('starList', dataDir)
readPlanetsFile(list, 'planetsList_tmp_earth.csv', dataDir)

cam = getDefaultCamera()
cam.setPosition( Vector3( 0, 0, 5))
sphere = SphereShape.create( 0.1, 4 )

q = list['Sun']

ui = UiModule.createAndInitialize()
wf = ui.getWidgetFactory()
uiroot = ui.getUi()

windowContainer = wf.createContainer('multiple', uiroot, ContainerLayout.LayoutFree)
windowContainer.setPosition(Vector2(0, 0))

sphere = wf.createImage('sphere', windowContainer)
sphere.setData(loadImage('png/WX_circle_red.png'))
sphere.setPosition(Vector2(0,0))

####	draw planetary sytem:
# drawPlanetarySystems(list)

# caveSystem = list['Sun']

# def onUpdate(frame, t, dt):
	# global caveSystem
	# planetList = caveSystem.planetObjList
	# if caveSystem != None:
		# for name in planetList:
			# caveSystem.planetRotate(dt * caveSystem.speedScale /planetList[name][2], name)
			# planetList[name][1].yaw(dt * caveSystem.speedScale /planetList[name][3])

# setUpdateFunction(onUpdate)

