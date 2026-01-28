#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

vec2 cstart = vec2(0,0);

float zoom = time*time;
//float zoom = 10
//int DEPTH = int(round(time))*2;
int DEPTH = 200;
vec2 CamPos = vec2(0.37,0.1);

vec3 CalcColor(int iterations){
	if (iterations == DEPTH){
		return vec3(0,0,0);
	}
	else{
	    float j = iterations/(DEPTH-1);
        int R = 0;
        float G = j;
        float B = (1-j);
		return vec3(R,G,B);
	}

}

vec2 ComplexEquation(vec2 z, vec2 c){
	return vec2((z[0]*z[0]-z[1]*z[1]+c[0]),(2*z[0]*z[1]+c[1]));

}


int ComplexAnalize(int depth, vec2 pos){
	vec2 ans = ComplexEquation(cstart, pos);
	int i = 1;
	while (i != depth){
		ans = ComplexEquation(ans, pos);
		if (ans[0]*ans[0]+ans[1]*ans[1] > 4){
			return(i);
		}
		i += 1;
	}
	return(i);

}

void main(){
	vec2 uv =  (gl_FragCoord.xy - 0.5 * resolution.xy) / resolution.y;
	vec3 col = vec3(0.0,0.1,0.2);

	//col = vec3(CalcColor(ComplexAnalize(DEPTH, (uv)/zoom+CamPos)));
	
	col = vec3(uv[0]*uv[0]*(sin(time*2)/0.5), uv[1]*uv[1]*(sin(time*2)/-0.3), 0.2);
	

	col += vec3(0.01 / length(uv) * (sin(time)+1)/2.0, (sin(time)+0.3)/8.0, length(uv)*0.1);
	col += 0.01 / length(uv - vec2((sin(time)+0.3)/3.0, (sin(time)+0.4)/3.0)) * (sin(time)+1)/1.1;
	//col += 0.01 / length(uv - vec2(0.25));

	//col += vec3(gl_FragCoord.x,0,0);

	 fragColor = vec4(col, 1.0);
}