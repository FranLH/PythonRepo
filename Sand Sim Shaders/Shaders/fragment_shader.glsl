#version 330

in vec2 uv;
layout (location = 0) out uvec4 fragColor;

uniform usampler2D gameTex;
uniform ivec2 simResolution;
uniform float time;
uniform vec2 camPos;
uniform int frame;

const uint LIMIT = 0U;
const uint AIR = 1U;
const uint SAND = 2U;






// r ->  cell type 0=limit 1=air 2=sand
// g ->  is falling 0=static 1=falling
// b ->  lifetime
// a ->  occupied 0=empty 1=solid

uvec4 getCellData(ivec2 cell)
{
	if (cell.x<0 || cell.y<0 || cell.x>= simResolution.x || cell.y >= simResolution.y)
	{
		return uvec4(LIMIT, 0U, 0U, 1U);
	}
	else
	{
		return texelFetch(gameTex, cell, 0);
	}
}

void main()
{
	
	ivec2 cell = ivec2(gl_FragCoord.xy);
	bool parity = ((cell.x + cell.y) & 1) == 0; // Checkerboard pattern

	uvec4 pixelData = getCellData(cell);
	
	uvec4[8] neighboursData = uvec4[8](
	getCellData(cell+ivec2(0,1)),
	getCellData(cell+ivec2(1,1)),
	getCellData(cell+ivec2(1,0)),
	getCellData(cell+ivec2(1,-1)),
	getCellData(cell+ivec2(0,-1)),
	getCellData(cell+ivec2(-1,-1)),
	getCellData(cell+ivec2(-1,0)),
	getCellData(cell+ivec2(-1,1)));



	uvec4 outColor = pixelData;
	if (true)
	{
		if (pixelData.r == AIR) // If the pixel is air
		{
			if (neighboursData[0].r == SAND) // If it has sand on top
			{
				outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
			}
			else
			{
				if (parity) // If parity
				{
					if (neighboursData[1].r == SAND && neighboursData[2].r != AIR) // if top right is sand and right is not air
					{
						outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
					}
				}
				else // if not parity
				{
					if (neighboursData[7].r == SAND && neighboursData[6].r != AIR) // if top left is sand and left is not air
					{
						outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
					}
				}
			}
		}
		else if (pixelData.r == SAND) // If the pixel is sand
		{
			if (neighboursData[4].r == AIR) // if below is air
			{
				outColor = uvec4(AIR, 0, 0, 1); // Turns into air
			}
			else if (parity) // if parity
			{
				if (neighboursData[5].r == AIR && neighboursData[6].r == AIR) // if below left is AIR and left is AIR
				{
					outColor = uvec4(AIR, 0, 0, 1); // Turns into air
				}
			}
			else // if not parity
			{
				if (neighboursData[3].r == AIR && neighboursData[2].r == AIR) // if below right is AIR and right is AIR
				{
					outColor = uvec4(AIR, 0, 0, 1); // Turns into air
				}
			}
		}
	}
	//   O
	//   O 
	//   #O
	// ######

	if (frame == 0)
	{
		if (length(cell-vec2(420,200)) <= 30)
		{
			outColor = uvec4(LIMIT,0,0,1);
		}
	}

	if (frame == 20 && cell == ivec2(420, simResolution.y-420))
	{
		outColor = uvec4(SAND,0,0,1);
	}

	if (cell.y == 270 && (421>= cell.x && cell.x >=420))
	{
		if (frame <= 288)
		{
			outColor = uvec4(SAND,0,0,1);
		}
	
//		else
//		{
//			outColor = uvec4(AIR,0,0,0);
//		}
	}



	fragColor = outColor;
}