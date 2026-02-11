#version 430


in vec3 v_color;

out vec4 fragColor;

//uniform vec2 resolution;
//uniform vec3 camPos;



void main()
{
	fragColor = vec4(v_color, 1.0);
}