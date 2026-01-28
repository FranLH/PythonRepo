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
	uvec4 outColor = pixelData;
	uvec4[8] neighboursData = uvec4[8](
	getCellData(cell+ivec2(0,1)),
	getCellData(cell+ivec2(1,1)),
	getCellData(cell+ivec2(1,0)),
	getCellData(cell+ivec2(1,-1)),
	getCellData(cell+ivec2(0,-1)),
	getCellData(cell+ivec2(-1,-1)),
	getCellData(cell+ivec2(-1,0)),
	getCellData(cell+ivec2(-1,1)));


	if (frame%1==0)
	{

		if (pixelData.r == AIR) // If the pixel is air
		{
			if (neighboursData[0].r == SAND) // If it has sand on top
			{
				if (neighboursData[4].r == AIR) // If below is air or moving
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
				}
				else
				{
					if ( (!parity && (neighboursData[5].r == AIR || neighboursData[5].g == 1U)) || (parity && (neighboursData[3].r == AIR || neighboursData[3].g == 1U))) // If parity and bottom left is air or moving or not parity and bottom right is air or moving
					{
						outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
					}
					else
					{
						outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
					}
				}
			
			}
			else
			{
				if (neighboursData[1].r == SAND) // If top right is sand
				{
					if (parity && neighboursData[2].ga == uvec2(0,1)) // If parity and right is a static solid
					{
						if (neighboursData[4].r == AIR) // If below is air 
						{
							outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
						}
						else
						{
							outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
						}

					}
				}
				else if (neighboursData[7].r == SAND) // If top left is sand
				{
					if (!parity && neighboursData[6].ga == uvec2(0,1)) // If not parity and left is a static solid
					{
						if (neighboursData[4].r == AIR) // If below is air
						{
							outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
						}
						else
						{
							outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
						}
					}
				}
				else
				{
					outColor = uvec4(AIR, 0, 0, 0); // Turns into air
				}
			}
		}
		else if (pixelData.r == SAND) // If the pixel is sand
		{
			if (neighboursData[0].gr == uvec2(1,SAND)) // If it has moving sand on top
			{
				if ( (!parity && pixelData.g != 1U && neighboursData[7].r != SAND && neighboursData[7].g != 1U && (neighboursData[6].r == AIR || neighboursData[6].g == 1U)) && (neighboursData[4].r == AIR || neighboursData[4].g == 1U || ( (neighboursData[3].r == AIR) && neighboursData[2].r != SAND) )) // if not parity and is not moving and top left not sand or moving and left is air or moving and below is air or moving or (below right is air or moving and right is not sand)
				{
					outColor = uvec4(AIR, 0, 0, 0); // Turns into air
				}

				else if ( (parity && pixelData.g != 1U && neighboursData[2].r != SAND && neighboursData[2].g != 1U && (neighboursData[3].r == AIR || neighboursData[3].g == 1U)) && (neighboursData[4].r == AIR || neighboursData[4].g == 1U || ( (neighboursData[5].r == AIR) && neighboursData[6].r != SAND) )) // if not parity and is not moving and top right not sand or moving and right is air or moving and below is air or moving or (below left is air or moving and left is not sand)
				{
					outColor = uvec4(AIR, 0, 0, 0); // Turns into air
				}

				else if (neighboursData[4].r == AIR) // If below is air 
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
				}
//				else if ((!parity && ( (neighboursData[5].r == AIR || neighboursData[5].g == 1U) && neighboursData[6].r != SAND)) || (parity && ( (neighboursData[3].r == AIR || neighboursData[3].g == 1U) && neighboursData[2].r != SAND)))
//				{
//					outColor = uvec4(SAND, 0, 0, 1); // Turns into moving sand
//				}
				else
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
				}
			}

			else if (parity)
			{
				if (pixelData.g == 1U && neighboursData[1].r == SAND && neighboursData[2].ga == uvec2(0,1)) // If moving and top right is sand and right is static solid
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
				}
				else if (neighboursData[4].r == AIR || ( (neighboursData[5].r == AIR) && neighboursData[6].r != SAND) ) // If below is air or moving or (below left is air or moving and left is not sand)
				{
					outColor = uvec4(AIR, 0, 0, 0); // Turns into air
				}
				else
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
				}
			}
			else
			{
				if (pixelData.g == 1U && neighboursData[7].r == SAND && neighboursData[6].ga == uvec2(0,1)) // If moving and top left is sand and left is static solid
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
				}
				else if (neighboursData[4].r == AIR || ( (neighboursData[3].r == AIR) && neighboursData[2].r != SAND) ) // If below is air or (below right is air or moving and right is not sand)
				{
					outColor = uvec4(AIR, 0, 0, 0); // Turns into air
				}
				else
				{
					outColor = uvec4(SAND, 0, 0, 1); // Turns into static sand
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

	if (frame 
	= 20 && cell == ivec2(420, simResolution.y-420))
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