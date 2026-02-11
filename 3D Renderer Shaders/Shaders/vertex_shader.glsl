#version 430


in vec2 in_position;
in vec3 in_normal;
//out vec2 uv;
out vec3 v_color;

void main() {
    //uv = in_position * 0.5 + 0.5;
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_color = in_normal;
    
}
