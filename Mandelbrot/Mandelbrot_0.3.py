import pygame

# initialising the pygame
pygame.init()

WindowSize = 800

#___________________________________________________________________
#___________________________________________________________________

#--------SETTINGS---------#

RenderLayers = 1
# Carga la imagen por capas, puede hacer que cargue mas lento pero permite ver el progreso de manera mas facil. poner en 1 para desactivar

DEPTH = 100
# Aumenta la definicion de la imagen bajo costo de disminuir la velocidad de carga

DepthIncrement = 5
# Cuanto aumenta la definicion cada vez que hagas zoom, la imagen pierde definicion cuando haces zoom y esto hace ese proceso mas lento, aunque tambien aumenta el tiempo que tarda en cargar

zoom = 5
# Cuanto se agranda la imagen al hacer click (20)

cstart = (0,0)
# Cambia la forma del fractal. No recomendaria numeros mucho mas grandes que 1. El valor predeterminado es (0,0)

cam = (0,0)
# La posicion inicial de la camara con respecto al fractal (0,0)

camsize = 5
# Modifica cuan grande o chico se ve el fractal al inicializar el programa (5)

#___________________________________________________________________
#___________________________________________________________________

# Crea una ventana
window = pygame.display.set_mode((WindowSize, WindowSize), pygame.SRCALPHA, 32)
pygame.display.set_caption("Fractals")


Drawing = pygame.Surface((WindowSize, WindowSize), pygame.SRCALPHA, 32)
Drawing.fill((0,0,0,0))
Selection = pygame.Surface((WindowSize, WindowSize), pygame.SRCALPHA, 32)

# Calcula el color del pixel en base a cuantas iteraciones tardo en darse cuenta que era infninito
def CalcColor(iterations):
    if iterations == DEPTH:
        return((0,0,0,255))
    else:
        j = iterations/(DEPTH-1)
        R = 0
        G = j*255
        B = (1-j)*255
        return((R,G,B,255))

def CalcPos(pos,a):
    return((cam[a]+(abs(camsize)/WindowSize)*pos)- camsize/2)

# Esto se ejecuta para cada pixel y define si esta dentro o fuera del fractal. z es una constante que marca el centro del fractal. c es la posicion del pixel en el que se ejecuta la funcion. z(x)^2-z(y)^2 + c(x) ; 2*z(x)*z(y) + c(y)
def ComplexEquation(z,c):
    return((z[0]*z[0]-z[1]*z[1]+c[0]),(2*z[0]*z[1]+c[1]))

# Esto itera la funcion de arriba hasta que el resultado este afuera de un circulo de radio 2 desde el centro, o que llegue a cierta cantidad de iteraciones. Cuando termina devuelve la cantidad de iteraciones que tardo
def ComplexAnalize(depth, pos):
    global cstart
    ans = ComplexEquation(cstart,pos)
    i=1
    while i != depth:
        ans = ComplexEquation(ans,pos)
        if ans[0]*ans[0]+ans[1]*ans[1] > 4:
            return(i)
        i+=1
    return(i)

# Calcula para cada pixel en la pantalla si esta dentro o fuera del fractal y los dibuja
def render():
    global Drawing, Selection

    LastIm = []
    #FirstP = 
    for k in range(RenderLayers):

        for i in range(800):
            if len(LastIm)<800:
                LastIm.append([])
            if i%RenderLayers-k == 0:
                for j in range(800):
		    # El fractal esta contenido dentro de un circulo de radio 2, asi que el programa ignora todas las posiciones afuera de este circulo para ahorrar memoria
                    if CalcPos(i,0)*CalcPos(i,0) + CalcPos(j,1)*CalcPos(j,1) < 4:
                        
			# Calcula para un pixel si esta dentro o fuera del fractal y elije su color en base a cuantas iteraciones tardo en acabar la funcion. si llego a su fin sin salirse del circulo de radio 2 el pixel se pinta color negro
                        result = ComplexAnalize(DEPTH,(CalcPos(i,0),CalcPos(j,1)))
                        LastIm[i].insert(j, (Drawing, CalcColor(result), (i,j), (i,j)))
                        pygame.draw.line(Drawing, CalcColor(result), (i,j), (i,j))
                    else:
                       	# pinta los pixeles afuera del circulo de color azul
                       	LastIm[i].insert(j, (Drawing, (0,0,255,255), (i,j), 1))
                        pygame.draw.circle(Drawing, (0,0,255,255), (i,j), 1)

	    # Actualiza una region de la pantalla cada cierta cantidad de iteraciones
            if i%8 == 0:
                window.blits(((Drawing, (0,0)),(Selection, (0,0))))
                pygame.display.update(i-7,0,i,800)
    
    # actualiza la pantalla
    window.blits(((Drawing, (0,0)),(Selection, (0,0))))
    pygame.display.flip()
    #print(LastIm)
    
def SelectionDraw():
    global zoom
    if zoom < 1:
        zoom = 1
    Selection.fill((0,0,0,0))
    size = (WindowSize/(zoom)/2)

    mouspos = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    #pygame.draw.rect(Selection, (255,0,0,255), (pygame.mouse.get_pos()[0]-size,pygame.mouse.get_pos()[1]-size), (pygame.mouse.get_pos()[0]+size,pygame.mouse.get_pos()[1]+size))
    pygame.draw.rect(Selection, (255,0,0,255), ((mouspos[0]-size,mouspos[1]-size),(size*2,size*2)), 1)
    window.blits(((Drawing, (0,0)),(Selection, (0,0))))
    pygame.display.flip()
# Updates the screen when the code is first executed
render()

running = True
while running:

    # Check for events
    SelectionDraw()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        zoom+=0.1
        SelectionDraw()
    if keys[pygame.K_DOWN]:
        zoom-=0.1
        SelectionDraw()
    for event in pygame.event.get():

        #print(zoom)
        # Check if the event is QUIT, then set running to false
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()

            if mouse_presses[0]:
                     
		# Calcula la nueva posicion de la camara con respecto a la posicion del mouse, aumenta el zoom y vuelve a calcular el fractal      
                cam = (CalcPos(pygame.mouse.get_pos()[0],0),CalcPos(pygame.mouse.get_pos()[1],1))
                camsize = camsize/zoom
                DEPTH+=DepthIncrement
                render()



           
pygame.display.quit()