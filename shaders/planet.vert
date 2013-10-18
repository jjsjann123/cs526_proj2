uniform float orbitScale;

void main(void)
{
	vec4 pos = gl_Vertex;
	pos.x = pos.x * orbitScale;
	gl_Position = pos;
	gl_FrontColor = gl_Color;
}