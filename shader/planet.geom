uniform float orbit;
uniform float radius;

uniform float unif_Glow;

void main(void)
{
		gl_Position = gl_PositionIn[0];
		gl_Position = gl_ProjectionMatrix * gl_Position;
		EmitVertex();

		EndPrimitive();
	}
}