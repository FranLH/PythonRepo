

Rendimiento = 0.00066828818
Año = 365
Mes = 91.25/3
Semana = 7
TNA = 0.268

# def RendimientoPorTiempo(plataInicial, dias, rendimiento):
#     plata = plataInicial
#     for dia in range(dias):
#         plata+=plata*Rendimiento
#     print("Plata inicial:", plataInicial, "Plata final:", plata, "Ganancia:", plata-plataInicial)
    
def RendimientoPorTiempo(plataInicial, dias, rendimiento):
    plata = plataInicial
    for dia in range(round(dias)):
        plata+=(plata*rendimiento)/365
    print("Plata inicial:", plataInicial, "Plata final:", plata, "Ganancia:", plata-plataInicial)

# RendimientoPorTiempo(1000000, 1*Año, TNA)
RendimientoPorTiempo(10000000, 1*Mes, TNA)
# RendimientoPorTiempo(10000, 2*Año, Rendimiento)
# RendimientoPorTiempo(10000, 10*Año, Rendimiento)

