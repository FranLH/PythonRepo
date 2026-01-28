import random


RECURSOS = {
1:"Oxígeno",
2:"Hidrógeno",
3:"Carbono",
4:"Nitrógeno",
5:"Enlace",
6:"Enlace doble",
7:"Enlace triple",
8:"Par libre"}

COMPUESTOS = {
1:{"nombre":"Agua", "abreviacion":"H2O", "recursos":[(1,1),(2,2),(5,2),(8,2)]},
2:{"nombre":"Dióxido de carbono", "abreviacion":"CO2", "recursos":[(1,2),(3,1),(5,4),(8,4)]}
}

PROPORCIONES = {
1:8,
2:10,
3:6,
4:5,
5:12,
6:6,
7:3,
8:12}

class Compuesto:
    def __init__(self, ID:int):
        data:dict = COMPUESTOS[ID]
        self.nombre=data["nombre"]
        self.abreviacion=data["abreviacion"]
        self.recursos=data["recursos"]
    def __repr__(self):
        return self.nombre

class Recurso:
    def __init__(self, ID):
        self.data = RECURSOS[ID]
    def __repr__(self):
        return self.data
        
class Jugador:
    def __init__(self, nombre:str):
        self.nombre :str = nombre
        self.mano :list[Recurso] = []
        self.mesa :list[Recurso] = []
        self.compuesto :Compuesto = None
        
    def PrintData(self):
        print("Nombre:",self.nombre)
        print("Mano:", self.mano)
        print("Mesa:", self.mesa)
        print("Compuesto:", self.compuesto)
    def __repr__(self):
        return self.nombre
        
class Mesa:
    def __init__(self, jugadores:list[str]):
        self.jugadores :list[Jugador] = []
        for nombre in jugadores:
            self.jugadores.append(Jugador(nombre))
            
        self.mazo :list[Recurso] = []
        for recursoID in PROPORCIONES:
            for i in range(PROPORCIONES[recursoID]):
                self.mazo.append(Recurso(recursoID))
        
        self.compuestos :list[Compuesto]= []
        for compuestoID in COMPUESTOS:
            self.compuestos.append(Compuesto(compuestoID))
        
        self.turno = 0
        
    def MezclarMazo(self):
        random.shuffle(self.mazo)
        
    def MezclarCompuestos(self):
        random.shuffle(self.compuestos)
        
    def RepartirCartas(self,cantidad:int):
        for i in range(cantidad):
            for jugador in self.jugadores:
                jugador.mano.append(self.mazo[0]) # WILL GIVE ERROR IF DECK IS EMPTY
                self.mazo.pop(0)
                
    def RepartirCompuestos(self):
        for jugador in self.jugadores:
            jugador.compuesto = self.compuestos[0] # WILL GIVE ERROR IF COMPOUNDS DECK IS EMPTY
            self.compuestos.pop(0)        
        
    def EmpezarPartida(self):
        self.MezclarCompuestos()
        self.MezclarMazo()
        self.RepartirCompuestos()
        self.RepartirCartas(5)
        self.turno = random.randint(0,len(self.jugadores)-1) # Elige un jugador al azar para comenzar
        

M = Mesa(["Fran", "Nacho"])
M.EmpezarPartida()
for j in M.jugadores:
    j.PrintData()

