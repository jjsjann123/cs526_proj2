from omega import *
from omegaToolkit import *
from fun import *
from xmlReader import *
from orbit import *
from multiples import *
from galaxy import *
from stars import *

newSystemInCave = None
allSystem = {}
globalOrbitScale = 5.0
globalRadiusScale = 0.5
getSceneManager().displayWand(0, 1)
getSceneManager().setBackgroundColor(Color('black'))
sky = getStar()
skyScale = 6
sky.setScale(Vector3(1,1,1)*skyScale * globalOrbitScale)

mm = MenuManager.createAndInitialize()
appMenu = mm.createMenu("contolPanel")

appMenu.addButton("OrbitScale +", "changeOrbit(1.5)")
appMenu.addButton("OrbitScale -", "changeOrbit(1.0/1.5)")
appMenu.addButton("RadiusScale +", "changeRadius(1.5)")
appMenu.addButton("RadiusScale -", "changeRadius(1.0/1.5)")

appMenu.addButton("Show Galaxy", "switchSystemInCave(galaxy)")
appMenu.addButton("Reset View", "resetView()")

cam = getDefaultCamera()
cam.setControllerEnabled(False)
flagMoveBack = False
flagMoveForward = False
flagMoveUp = False
flagMoveDown = False
flagRotateUpDown = 0.0
flagRotateLeftRight = 0.0
speed = 5
omega = radians(30)
updateFuncList = []

flagShowSpot = False
spotLight = SphereShape.create(0.02, 4)
spotLight.setPosition(Vector3(0,0,0))
spotLight.setEffect("colored -e red")
cam.addChild(spotLight)
menuShow = False


def pickSystem(node):
	global containerToSystemMap
	global newSystemInCave
	print 'pick the system'
	pick = containerToSystemMap.get(node)
	if pick != None:
		print 'pick ', pick
		print 'node ', node
		switchSystemInCave(pick)
pickMultiples = pickSystem
btest = True
def ifHitAnything (node):
	global btest
	if (node == None):
		print "missed"
	else:
		print 'hit'
		if btest:
			node.setEffect("colored -e red")
		else:
			node.setEffect("colored -e blue")
		btest = not btest

def onUpdate(frame, t, dt):
	global cam
	global speed
	global omega
	global flagMoveBack
	global flagMoveForward
	global flagMoveUp
	global flagMoveDown
	global flagRotateUpDown
	global flagRotateLeftRight
	global updateFuncList
	
	#	Movement
	if(flagMoveForward):
		cam.translate(0, 0, -dt * speed, Space.Local )
	if(flagMoveBack):
		cam.translate(0, 0, dt * speed, Space.Local )
	if(flagMoveUp):
		cam.translate(0, dt * speed, 0, Space.Local )
	if(flagMoveDown):
		cam.translate(0, -dt * speed, 0, Space.Local )
	cam.pitch(flagRotateUpDown*omega*dt)
	cam.yaw(flagRotateLeftRight*omega*dt)
	for func in updateFuncList:
		func(frame, t, dt)
	
def attachUpdateFunction(func):
	global updateFuncList
	updateFuncList.append(func)
	

def changeOrbit(ratio):
	global globalOrbitScale
	global sky
	global skyScale
	globalOrbitScale *= ratio
	setGlobalOrbitScale(globalOrbitScale)
	
	
def changeRadius(ratio):
	global globalRadiusScale
	globalRadiusScale *= ratio
	setGlobalRadiusScale(globalRadiusScale)
	
def resetView():
	cam = getDefaultCamera()
	cam.setPosition(Vector3( 10, 2, 10 ))
	cam.setPitchYawRoll(Vector3(0, radians(45), 0))
	cam.pitch(radians(-10))

def switchSystemInCave(newSystem):
	global systemInCave
	global galaxy
	global galaxyCore
	if newSystem == galaxy:
		systemInCave.setVisible(False)
		galaxy.setChildrenVisible(True)
		galaxy.setVisible(True)
		galaxyCore.getMaterial().setDepthTestEnabled(False)
		systemInCave = galaxy
	else:
		if galaxy.isVisible():
			galaxy.setVisible(False)
			galaxy.setChildrenVisible(False)
		if newSystem != None:
			if systemInCave != None and systemInCave != newSystem:
				systemInCave.setVisible(False)
			newSystem.setVisible(True)
		else:
			if systemInCave != None:
				systemInCave.setVisible(False)
		systemInCave = newSystem
		if systemInCave != None:
			setGlobalOrbitScale(globalOrbitScale)
			setGlobalRadiusScale(globalRadiusScale)

def updateFunction(frame, t, dt):
	global systemInCave
	global newSystemInCave
	global galaxy
	global sky
	if newSystemInCave != None and newSystemInCave != systemInCave:
		print "switch it"
		switchSystemInCave(newSystemInCave)
		newSystemInCave = None
	if systemInCave != None and systemInCave != galaxy:
		systemInCave.running(dt)
	galaxy.yaw(dt*radians(5))
	sky.yaw(dt*radians(5))
	
def setGlobalOrbitScale(scale = 5.0):
	global globalOrbitScale
	globalOrbitScale = scale
	multiples.orbitScale.setFloat(scale)
	PlanetarySystem.orbitScale = scale
	sky.setScale(Vector3(1,1,1)*scale*skyScale)
	if systemInCave != None:
		systemInCave.setOrbitScale()

def setGlobalRadiusScale(scale = 0.2):
	global globalRadiusScale
	globalRadiusScale = scale
	multiples.radiusScale.setFloat(scale)
	PlanetarySystem.radiusScale = scale
	if systemInCave != None:
		systemInCave.setRadiusScale()


def setRotationSpeedScale(scale):
	PlanetarySystem.speedScale = scale

def moveMultiple(x, y, z):
	print x, ' ', y, ' ', z
		
#
#	Here h and v should be in range(1,8)
#
def addMultipleToWall(multiple, h, v):
	global rootNode
	global column
	global row
	global cam
	if column < h or row < v:
		print "out of range"
		return None
	else:
		print "construct"
		multiple.multiple.setPosition(Vector3(-0.5, 0, 0.01) + multiple.multiple.getPosition())
		if h >= 4:
			h+=3
		v -= 1
		hLoc = h + 0.5
		degreeConvert = 36.0/360.0*2*pi #18 degrees per panel times 2 panels per viz = 36
		caveRadius = 3.25
		screenCenter = multiple.parentNode
		screenCenter.setPosition(Vector3(sin(hLoc*degreeConvert)*caveRadius, v * 0.29 + 0.41, cos(hLoc*degreeConvert)*caveRadius))
		screenCenter.yaw(hLoc*degreeConvert+radians(180))
		rootNode.addChild(screenCenter)
		return screenCenter

#
#	Read all files and initialize
#

cam = getDefaultCamera()
rootNode = SceneNode.create("systemOnWall")
#cam.addChild(rootNode)
column = 6
row = 8
systemDir = "./stellar/"
multiples.initialize()
systemDic = readAllFilesInDir(systemDir)

multiples.radiusRatio.setFloat(4.0)
multiples.orbitRatio.setFloat(8.0)

# skybox = Skybox()
# skybox.loadCubeMap('./model/skybox/', 'png')
# getSceneManager().setSkyBox(skybox)
cam.setPosition(Vector3( 10, 2, 10 ))
cam.yaw(radians(45))
cam.pitch(radians(-10))

# for h in range(1,9):
	# for v in range(1,9):
		# outlineBox = SphereShape.create(0.125, 4)
		# addMultipleToWall( outlineBox, h, v)
def loadAllSystem():
	h = 1;
	v = 0;
	global galaxy
	global galaxyCore
	global containerToSystemMap
	global targetList
	(galaxy,galaxyCore) = buildGalaxy(systemDic)
	for systemName in systemDic:
		stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
		stellarMultiple = multiples(systemDic[systemName])
		v+=1;
		if v > row:
			v = 1
			h+=1
		addMultipleToWall(stellarMultiple, h, v)
		stellar.drawSystem(False)
		allSystem.update( {systemName: [stellar, stellarMultiple]} )
		stellarMultiple.multiple.setSelectable(True)
		targetList.append(stellarMultiple.multiple)
		containerToSystemMap.update( {stellarMultiple.multiple: stellar} )
		if v == row and h == column:
			break;
def onEvent():
	global cam
	global flagMoveBack
	global flagMoveForward
	global flagMoveUp
	global flagMoveDown
	global flagRotateUpDown
	global flagRotateLeftRight
	global spotLight
	global pickMultiples
	global targetList
	global appMenu
	global menuShow
	global containerToSystemMap
	global newSystemInCave
	e = getEvent()
	type = e.getServiceType()
	if(type == ServiceType.Pointer or type == ServiceType.Wand or type == ServiceType.Keyboard):
		# Button mappings are different when using wand or mouse
		

		if(type == ServiceType.Keyboard):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button1
			lowHigh = 0
			leftRight = 0
			forward = ord('w')
			down = ord('s')
			low = ord('i')
			high = ord('k')
			turnleft = ord('j')
			turnright = ord('l')
			climb = ord('a')
			descend = ord('d')
			flagH = False
			flagV = False
			if(e.isKeyDown( low)):
				lowHigh = 0.5
				flagV = True
			if(e.isKeyDown( high )):
				lowHigh = -0.5
				flagV = True
			if(e.isKeyDown( turnleft)):
				leftRight = 0.5
				flagH = True
			if(e.isKeyDown( turnright )):
				leftRight = -0.5				
				flagH = True
			if(e.isKeyDown( forward)):
				flagMoveForward = True
			if(e.isKeyDown( down )):
				flagMoveBack = True
			if(e.isKeyDown( climb)):
				flagMoveUp = True
			if(e.isKeyDown( descend )):
				flagMoveDown = True
			if(e.isKeyUp( forward)):
				flagMoveForward = False
			if(e.isKeyUp( down )):
				flagMoveBack = False
			if(e.isKeyUp( climb)):
				flagMoveUp = False
			if(e.isKeyUp( descend )):
				flagMoveDown = False
			flagRotateLeftRight = leftRight
			flagRotateUpDown = lowHigh
			
		if(type == ServiceType.Wand):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button3
			forward = EventFlags.ButtonUp
			down = EventFlags.ButtonDown
			climb = EventFlags.ButtonLeft
			descend = EventFlags.ButtonRight
			pick = EventFlags.Button5
			move = EventFlags.Button7
			lowHigh = e.getAxis(1)
			leftRight = -e.getAxis(0)
			
			if(e.isButtonDown(confirmButton) and not menuShow):
				appMenu.getContainer().setPosition(e.getPosition())
				appMenu.show()
				appMenu.placeOnWand(e)
				menuShow = True
			if(e.isButtonDown(quitButton) and menuShow):
				appMenu.hide()
				menuShow = False
			e.setProcessed()

			if(e.isButtonDown( forward)):
				flagMoveForward = True
			if(e.isButtonDown( down )):
				flagMoveBack = True
			if(e.isButtonDown( climb)):
				flagMoveUp = True
			if(e.isButtonDown( descend )):
				flagMoveDown = True
			if(e.isButtonUp( forward)):
				flagMoveForward = False
			if(e.isButtonUp( down )):
				flagMoveBack = False
			if(e.isButtonUp( climb)):
				flagMoveUp = False
			if(e.isButtonUp( descend )):
				flagMoveDown = False
			flagRotateLeftRight = leftRight
			flagRotateUpDown = lowHigh

			if flagShowSpot:
				pos = e.getPosition()
				orient = e.getOrientation()
				wandPos = Point3(pos[0], pos[1], pos[2])
				Ray = orient * Ray3(wandPos, Vector3( 0., 0., -1.))
				wall = Sphere(Point3(0., 0., 0.), 3.45)
				res = Ray.intersect(wall)
			# r = getRayFromEvent(e)
			# if (r[0]): 
				# ray = Ray3(Point3(r[1][0], r[1][1], r[1][2]), Vector3(r[2][0], r[2][1], r[2][2]))
				# pos = cam.getPosition()
				# wall = Sphere(Point3(pos[0], pos[1], pos[2]), 3.45)
				# res = ray.intersect(wall)
				if res != None:
					hitSpot = res.p
					spotLight.setPosition(Vector3(hitSpot[0], hitSpot[1], hitSpot[2]))
				# if(e.isButtonDown(pick) and pickMultiples != None):
					# camPos = cam.getPosition()
					# pos = e.getPosition()
					# wandPos = Point3(pos[0], pos[1], pos[2]) + Point3(camPos[0], camPos[1], camPos[2])
					# orient = e.getOrientation()
					# ray = cam.getOrientation() * orient * Ray3(Point3(wandPos[0], wandPos[1], wandPos[2]), Vector3( 0., 0., -1.))
					# querySceneRay(ray.p, ray.v, pickMultiples)
						
			if(e.isButtonDown(pick) and targetList != [] and pickMultiples != None):
				r = getRayFromEvent(e)
				print "start finding"
				for item in targetList:
					hitData = hitNode(item, r[1], r[2])
					if(hitData[0]):
						newSystemInCave = containerToSystemMap.get(item)
						#switchSystemInCave(containerToSystemMap.get(item))
						#break

		if(type == ServiceType.Pointer):
			confirmButton = EventFlags.Button2
			quitButton = EventFlags.Button1
			#newSystemInCave = containerToSystemMap.get(targetList[2])
			if(e.isButtonDown(confirmButton)):
				appMenu.getContainer().setPosition(e.getPosition())
				appMenu.show()
				appMenu.placeOnWand(e)
			if(e.isButtonDown(quitButton)):
				appMenu.hide()
			e.setProcessed()
			if flagShowSpot:
				pos = e.getPosition()
				orient = e.getOrientation()
				#Ray = orient * Ray3(Point3(pos[0], pos[1], pos[2]), Vector3( 0., 0., -1.))
				Ray = Ray3(Point3(pos[0], pos[1], pos[2]), Vector3( 0., 0., -1.))
				wall = Sphere(Point3(0., 0., 0.), 3.45)
				res = Ray.intersect(wall)
				# r = getRayFromEvent(e)
				# if (r[0]): 
					# ray = Ray3(Point3(r[1][0], r[1][1], r[1][2]), Vector3(r[2][0], r[2][1], r[2][2]))
					# pos = cam.getPosition()
					# wall = Sphere(Point3(pos[0], pos[1], pos[2]), 3.45)
					# res = ray.intersect(wall)
				if res != None:
					hitSpot = res.p
					print "moving sphere"
					spotLight.setPosition(Vector3(hitSpot[0], hitSpot[1], hitSpot[2]))
			# camPos = cam.getPosition()
			# pos = e.getPosition()
			# wandPos = Point3(pos[0], pos[1], pos[2]) + Point3(camPos[0], camPos[1], camPos[2])
			# orient = e.getOrientation()
			# print cam.getOrientation()
			# print orient
			# print wandPos
			# ray = cam.getOrientation() * orient * Ray3(Point3(wandPos[0], wandPos[1], wandPos[2]), Vector3( 0., 0., -1.))
			# print ray
			# if pickMultiples != None:
				# querySceneRay(ray.p, ray.v, pickMultiples)
	
setEventFunction(onEvent)
setUpdateFunction(onUpdate)

loadAllSystem()
switchSystemInCave(allSystem['Sun'][0])
attachUpdateFunction(updateFunction)
sky.getMaterial().setDepthTestEnabled(False)
# galaxy = buildGalaxy(systemDic)
# systemName = "Kepler-33"
# stellar = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
# stellarMultiple = multiples(systemDic[systemName])
# stellarMultiple.parentNode.setPosition(Vector3( -2, 2, -4))
# stellar.drawSystem(False)
# systemName = "Sun"
# stellar2 = PlanetarySystem(systemDic[systemName]['star'], systemDic[systemName]['planets'], systemName)
# stellarMultiple2 = multiples(systemDic[systemName])
# stellarMultiple2.parentNode.setPosition(Vector3( 0.5, 2, -4))
# stellar2.drawSystem(False)
# switchSystemInCave(stellar2)



