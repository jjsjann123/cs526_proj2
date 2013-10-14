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