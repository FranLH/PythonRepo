#version 330

uniform usampler2D gameTex;
uniform ivec2 simResolution;
uniform ivec2 resolution;

uniform float blurStrength;
uniform float zoom;
uniform vec2 camPos;

in vec2 uv;
out vec4 fragColor;



uniform vec3[3] cellColors;

vec3 getColorFromData(uvec4 data)
{
    vec3 c = cellColors[int(data.r)];
    if (data.g != 1U)
    {
        c.b = 1;
    }
    return c;

}

void main() {

    // Screen pixel
    ivec2 screen = ivec2(gl_FragCoord.xy);

    // Map screen  simulation
    ivec2 simCell = ivec2(round(camPos+resolution/2 + ((screen-resolution/2) / zoom)));

        // Bounds check
    if (simCell.x < 0 || simCell.y < 0 || simCell.x >= simResolution.x || simCell.y >= simResolution.y)
    {
        fragColor = vec4(0); // outside sim  black
        return;
    }

    uvec4 cell = texelFetch(gameTex, simCell, 0);

    vec3 col = getColorFromData(cell);


//    vec2 viewUV = uv;
//
//    // zoom around center
//    viewUV = (viewUV - 0.5) / zoom + 0.5;
//
//    // pan in simulation space
//    viewUV += camPos / vec2(simResolution);
//    ivec2 cell = ivec2(viewUV * vec2(simResolution));
//
//
//
//    uvec4 pixelData = texelFetch(gameTex, cell, 0);
//    vec3 col = getColorFromData(pixelData);
    


    fragColor = vec4(col, 1);
    
}
