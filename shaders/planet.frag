#version 150 compatibility
#extension GL_ARB_gpu_shader5 : enable
uniform float orbit;
uniform float radius;

varying vec2 var_TexCoord;

uniform float unif_Glow;
void main (void)
{
	float x = var_TexCoord.x;
	float y = var_TexCoord.y;
	float vx = pow(1-x, unif_Glow);
	
	gl_FragColor.rgb = gl_Color.rgb;
	gl_FragColor.a = (vx);
	
	float r = length(vec2(x,y) - vec2(orbit, 0.5));
	if ( r < radius )
	{
		gl_FragColor.rgb = vec3(0.7,0.2,0.2);
		gl_FragColor.a = 1-r/radius;
	}
	
	if (var_TexCoord.x < 0.005 || var_TexCoord.x > 0.995 || var_TexCoord.y < 0.02 || var_TexCoord.y > 0.98 )
	{
		gl_FragColor.rgb = vec3(0,0,0);
		gl_FragColor.a = 1.0;
	}
}