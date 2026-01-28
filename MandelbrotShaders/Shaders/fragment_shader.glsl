#version 430


in vec2 uv;
out vec4 fragColor;

uniform vec2 resolution;
uniform float time;


uniform int paletteSize;
uniform vec3 inColor;
uniform vec3[200] outPalette;

uniform float zoom;
uniform vec2 camPos;
uniform float DEPTH;

uniform vec2 fractalPos;



vec3 CalcColor(int iterations, vec2 pos)
{
	if (iterations == DEPTH)
	{
		return inColor;
	}
	else
	{

		vec3 colorModifyer = vec3(sin(time)*pos.x/8,sin(time)*pos.x/16,0);
		return outPalette[int(mod(iterations, paletteSize))] + colorModifyer;
	}
}

vec2 ComplexEquation(vec2 z, vec2 c)
{
	return vec2((z[0]*z[0]-z[1]*z[1]+c[0]),(2*z[0]*z[1]+c[1]));
}


int ComplexAnalize(float depth, vec2 pos)
{
	vec2 ans = ComplexEquation(fractalPos, pos);
	int i = 1;
	while (i < depth){
		ans = ComplexEquation(ans, pos);
		if (ans[0]*ans[0]+ans[1]*ans[1] > 4)
		{
			return(i);
		}
		i += 1;
	}
	return(i);
}

void main()
{
	vec2 UV = (uv - 0.5) * vec2(resolution.x / resolution.y, 1.0);
	vec3 col = CalcColor(ComplexAnalize(DEPTH, UV/zoom+camPos), UV/zoom+camPos);


	fragColor = vec4(col, 1.0);
}