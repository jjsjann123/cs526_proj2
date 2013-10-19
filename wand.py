from omega import *
from cyclops import *
from omegaToolkit import *

cam = getDefaultCamera()
flagMoveBack = False
flagMoveForward = False
flagMoveUp = False
flagMoveDown = False
flagRotateUpDown = 0.0
flagRotateLeftRight = 0.0

sphere = SphereShape.create(0.05, 4)
sphere.setEffect("colored -d red")
wall = Sphere(Point3(0., 0., 0.), 3.45)

sphere2 = SphereShape.create(1, 4)
sphere2.setPosition(Vector3(0, 3, -10))
sphere2.setSelectable(True)
sphere3 = SphereShape.create(1, 4)
sphere3.setPosition(Vector3(3, 3, -10))
sphere3.setSelectable(True)
def ifHitAnything (node, distance):
	if (node == None):
		print "missed"
	else:
		node.setEffect("colored -e red")
		

def onEvent():
	global cam
	global sphere
	global wall
	global sphere2
	flagMoveBack = False
	flagMoveForward = False
	flagMoveUp = False
	flagMoveDown = False
	flagRotateUpDown = 0.0
	flagRotateLeftRight = 0.0
	e = getEvent()
	type = e.getServiceType()
	if(type == ServiceType.Pointer or type == ServiceType.Wand or type == ServiceType.Keyboard):
		# Button mappings are different when using wand or mouse
		confirmButton = EventFlags.Button2
		quitButton = EventFlags.Button1

		lowHigh = 0
		leftRight = 0
		if(type == ServiceType.Keyboard):
			forward = ord('w')
			down = ord('s')
			left = ord ('a')
			right = ord('d')
			low = ord('i')
			high = ord('k')
			turnleft = ord('j')
			turnright = ord('l')
			climb = ord('r')
			descend = ord('f')
			if(e.isKeyDown( low)):
				lowHigh = 0.5
			if(e.isKeyDown( high )):
				lowHigh = -0.5
			if(e.isKeyDown( turnleft)):
				leftRight = 0.5
			if(e.isKeyDown( turnright )):
				leftRight = -0.5				
			if(e.isKeyDown( forward)):
				flagMoveForward = True
			if(e.isKeyDown( down )):
				flagMoveBack = True
			if(e.isKeyDown( left)):
				flagMoveLeft = True
			if(e.isKeyDown( right )):
				flagMoveRight = True
			if(e.isKeyDown( climb)):
				flagMoveUp = True
			if(e.isKeyDown( descend )):
				flagMoveDown = True
			
		
		if(type == ServiceType.Wand):
			pos = e.getPosition()
			orient = e.getOrientation()
			Ray = orient * Ray3(Point3(pos[0], pos[1], pos[2]), Vector3( 0., 0., -1.))
			res = Ray.intersect(wall)
			if res != None:
				hitSpot = res.p
				print "moving sphere"
				sphere.setPosition(Vector3(hitSpot[0], hitSpot[1], hitSpot[2]))
			if(e.isButtonDown(EventFlags.Button5)):
				r = getRayFromEvent(e)
				if(r[0]): querySceneRay(r[1], r[2], ifHitAnything)

			# confirmButton = EventFlags.Button2
			# quitButton = EventFlags.Button3
			
			# forward = EventFlags.ButtonUp
			# down = EventFlags.ButtonDown
			# left = EventFlags.ButtonLeft
			# right = EventFlags.ButtonRight
			# climb = EventFlags.Button5
			# descend = EventFlags.Button7
			# lowHigh = e.getAxis(1)
			# leftRight = e.getAxis(0)
			# if(e.isButtonDown( forward)):
				
				# cam.translate(0, 0, -500, Space.Local )
			# if(e.isButtonDown( down )):
				# cam.translate(0, 0, 500, Space.Local )
			# if(e.isButtonDown( left)):
				# cam.translate(-500, 0, 0, Space.Local )
			# if(e.isButtonDown( right )):
				# cam.translate(500, 0, 0, Space.Local )
			# if(e.isButtonDown( climb)):
				# cam.translate(0, 500, 0, Space.Local )
			# if(e.isButtonDown( descend )):
				# cam.translate(0, -500, 0, Space.Local )
	
		# cam.rotate(Vector3(1,0,0), lowHigh*0.1, Space.Local)
		# cam.rotate(Vector3(0,0,1), -leftRight*0.1, Space.Local)
		if(type == ServiceType.Pointer):
			print "pointer"

r = Ray3(Point3(0.0,0.0,0.0), Vector3(0.0,0.0,-1.0))
s = Sphere(Point3(0.0, 0.0, 0.0), 2.0)

setEventFunction(onEvent)