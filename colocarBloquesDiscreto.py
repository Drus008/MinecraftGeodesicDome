from icosaedro import *
import os

# Posibles expansiones:
# Usar otras figuras para las caras
# Usar otros sólidos platónicos


carpeta = "C:/Users/druss/AppData/Roaming/.minecraft/saves/Pruebas DataPack/datapacks/geodesic_dome/data/dome/function/"
version = "1.21"


PHI = (1+sqrt(5))/2

# Genera el comando que coloca el "bloque" en las coordenadas "coordenadas"
def comandoColocarBloque(coordenadas, bloque:str):
    parametro = True
    if bloque=="arista":
        bloque = "$(arista)"
    elif bloque=="esquina":
        bloque = "$(esquina)"
    elif bloque=="cara":
        bloque = "$(cara)"
    else:
        parametro = False
    
    textCoord = "~" + str(coordenadas[0]) + " ~" + str(coordenadas[1]) + " ~" + str(coordenadas[2])
    comando = "setblock " + textCoord + " minecraft:" + bloque
    if parametro:
        comando = "$"+comando
    return comando

# Genera una lista en la que cada elemento es el comando que coloca el bloque en una coordenada de lista coordenadas
def listaComandos(listaCoordenadas: set ,bloque:str):
    lista = []
    for cord in listaCoordenadas:
        lista.append(comandoColocarBloque(cord, bloque))
    return lista

# Dada una lista de comando de minecraft, escrive cada uno en un archivo de un nombre dado
def escribir_en_archivo(nombre_archivo, llistaComandos):
    c=0
    t = 0
    while t<len(llistaComandos):
        direccion = carpeta + str(c) + nombre_archivo
        with open(direccion, 'a') as archivo:
            for i in range(65530):
                if t>=len(llistaComandos):
                    break
                archivo.write(llistaComandos[i + c*65530] + "\n")
                t = t+1
        
        
        print(f"Las líneas se han guardado en {direccion}")
        c = c+1



def main():
    radio = 10
    grosorCaras = 1
    grosorAristas = 1
    grosorEsquinas = 1
    densidadTriangulos = 0
    
    generarCaras = True
    generarAristas = True
    generarEsquinas = True

    bloqueCaras = "cara"
    bloqueAristas = "arista"
    bloqueEsquinas = "esquina"
    
    info = True

    if info:
        print("Eliminando archivos anteriores:")
    

    for i in range(20):
        nombre = carpeta + str(i) + "aristas.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = carpeta + str(i) + "esquinas.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = carpeta + str(i) + "caras.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = str(i) + "bola.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

    print("Generando domo geodésico de radio ", radio)

    print("Generando icosaedro...")
    conjuntoTriangulos = triangulosIcosaedro(radio)

    print("Generando triangulos intermedios...")
    conjuntoTriangulos = aumentarMuchosTriangulos(conjuntoTriangulos, radio, densidadTriangulos)

    if generarEsquinas:
        print("Generando las esquinas")
        conjuntoEsquinas = esquinasDeTriangulos(conjuntoTriangulos)
        print("Adaptando coordenadas de esquinas")
        conjuntoEsquinas = redondearPuntosConjunto(conjuntoEsquinas, 0)
        print("Ensanchando las esquinas")
        conjuntoEsquinas = agrandarBordes(conjuntoEsquinas, grosorEsquinas, info)
        print("Redaptando coordenadas de esquinas")
        conjuntoEsquinas = redondearPuntosConjunto(conjuntoEsquinas, 0)

    if generarAristas:
        print("Generando las aristas...")
        conjuntoAristas = aristasDeTriangulos(conjuntoTriangulos)
        print("Rellenando las aristas")
        conjuntoAristas = llenarConjuntoAristas(conjuntoAristas)
        print("Adaptando las coordenadas de las aristas")
        conjuntoAristas = redondearPuntosConjunto(conjuntoAristas,0)
        print("Ensanchando las aristas")
        conjuntoAristas = agrandarBordes(conjuntoAristas, grosorAristas, info)
        print("Volviendo a adaptar las coordenadas de las aristas")
        conjuntoAristas = redondearPuntosConjunto(conjuntoAristas,0)

    if generarCaras:
        print("Rellenando las caras")
        conjuntoTriangulos = llenarConjuntoTriangulos(conjuntoTriangulos)
        print("Adaptando las coordenadas de las caras")
        conjuntoTriangulos = redondearPuntosConjunto(conjuntoTriangulos,0)
        print("Ensanchando las caras")
        conjuntoTriangulos = agrandarBordes(conjuntoTriangulos,grosorCaras, info)
        print("Readaptando las coordenadas de las caras")
        conjuntoTriangulos = redondearPuntosConjunto(conjuntoTriangulos,0)

    print(len(conjuntoTriangulos), len(conjuntoAristas), len(conjuntoEsquinas))

    if generarCaras:
        print("Creando comandos para generar las caras...")
        com = listaComandos(conjuntoTriangulos, bloqueCaras)
        print("   Las caras constan de ", len(com), " bloques")
        escribir_en_archivo("caras.mcfunction", com)
    
    if generarAristas:
        print("Creando comandos para generar las aristas...")
        com = listaComandos(conjuntoAristas, bloqueAristas)
        escribir_en_archivo("aristas.mcfunction", com)
        print("   Las aristas constan de ", len(com), " bloques")
    
    if generarEsquinas:
        print("Creando comandos para generar las esquinas...")
        com = listaComandos(conjuntoEsquinas, bloqueEsquinas)
        escribir_en_archivo("esquinas.mcfunction", com)
        print("   Las esquinas constan de ", len(com), " bloques")


if __name__ == "__main__":
    main()