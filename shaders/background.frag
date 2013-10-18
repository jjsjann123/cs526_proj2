varying vec2 var_TexCoord;
uniform float unif_Glow;
uniform vec4 star_color;

void main (void)
{
	float x = var_TexCoord.x;
	float y = var_TexCoord.y;
	float vx = pow(1-x, unif_Glow);
	
	//gl_FragColor.rgb = gl_Color.rgb;
	gl_FragColor.rgb = star_color.rgb;
	//gl_FragColor.rgb = vec3(1.0, 0.0, 0.0);
	gl_FragColor.a = (vx);
	gl_FragDepth = 0.1;
	
	if (var_TexCoord.x < 0.005 || var_TexCoord.x > 0.995 || var_TexCoord.y < 0.02 || var_TexCoord.y > 0.98 )
	{
		gl_FragColor.rgb = vec3(0,0,0);
		gl_FragColor.a = 1.0;
		gl_FragDepth = 0.01;
	}
}