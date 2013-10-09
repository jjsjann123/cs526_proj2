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

#		container3D multiples:
# ui = UiModule.createAndInitialize()
# wf = ui.getWidgetFactory()
# uiroot = ui.getUi()

# windowContainer = wf.createContainer('multiple', uiroot, ContainerLayout.LayoutFree)
# windowContainer.setPosition(Vector2(0, 0))

# sphere = wf.createImage('sphere', windowContainer)
# sphere.setData(loadImage('png/WX_circle_red.png'))
# sphere.setPosition(Vector2(0,0))

##	Shader multiples:
scene = getSceneManager()
scene.createProgramFromString("multiple", 
# Vertex shader
'''
	uniform float orbit;
	uniform float radius;
	varying vec2 var_TexCoord;
	varying vec3 var_Normal;
	varying vec3 var_EyeVector;

	
	void main(void)
	{
		gl_Position = ftransform();
		vec4 eyeSpacePosition = gl_ModelViewMatrix * gl_Vertex;
		
		var_TexCoord = gl_MultiTexCoord0.xy;
		
		var_EyeVector = -eyeSpacePosition.xyz;
		var_Normal = gl_NormalMatrix * gl_Normal;
		
		gl_FrontColor = gl_Color;
	}
''',
# Fragment shader
'''
	uniform float orbit;
	uniform float radius;

	varying vec2 var_TexCoord;
	
	uniform float unif_Glow;
	void main (void)
	{
		float vx = pow(abs((var_TexCoord.x - 0.5) * 2), unif_Glow);
		float vy = pow(abs((var_TexCoord.y - 0.5) * 2), unif_Glow);

		gl_FragColor.rgb = gl_Color.rgb;
		gl_FragColor.a = (vx + vy);
	}
''')

multipleScale = 1.0;
multiple = PlaneShape.create(10*multipleScale, 2*multipleScale)
multiple.setPosition(Vector3(0, 3, -10))

multiple.setEffect("multiple -d red -t")
glowPower = multiple.getMaterial().addUniform('unif_Glow', UniformType.Float)
glowPower.setFloat(10)

##	draw planetary sytem:
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