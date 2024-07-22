from geodesica import geodesic_dome
from math import sqrt
from icosaedro import *
import os

PHI = (1+sqrt(5))/2

def comandoColocarBloque(coordenadas, bloque:str):
    textCoord = "~" + str(coordenadas[0]) + " ~" + str(coordenadas[1]) + " ~" + str(coordenadas[2])
    comando = "setblock " + textCoord + " minecraft:" + bloque
    return comando

def listaComandos(listaCoordenadas:list ,bloque:str):
    lista = []
    for cord in listaCoordenadas:
        lista.append(comandoColocarBloque(cord, bloque))
    return lista


def llistaComandos():
    radius = 30  # Adjust as needed
    frequency = 3  # Adjust as needed
    center = (0, 0, 0)  # Default center, adjust as needed
    edge_width = 1  # Adjust edge width here
    include_faces = True  # Include faces by default
    only_dome = True  # Only dome by default

    vertex_blocks, edge_blocks, face_blocks = geodesic_dome(radius, frequency, center, edge_width, include_faces, only_dome)

    vertex_blocks = list(vertex_blocks)
    edge_blocks = list(edge_blocks)
    face_blocks = list(face_blocks)

    numVertex = len(vertex_blocks)
    numEdge = len(edge_blocks)
    numFace = len(face_blocks)

    llista = list()

    #for i in range(numFace):
    #    comando = colocarBloque(face_blocks[i], "glass")
    #    llista.append(comando)
    #for i in range(numEdge):
    #    comando = colocarBloque(edge_blocks[i], "gold_block")
    #    llista.append(comando)
    #for i in range(numVertex):
    #    comando = colocarBloque(vertex_blocks[i], "diamond_block")
    #    llista.append(comando)

    print("Mida llista: ", len(llista))
    return(llista)

def escribir_en_archivo(nombre_archivo, llistaComandos):
    c=0
    t = 0
    while t<len(llistaComandos):
        with open(str(c) + nombre_archivo, 'a') as archivo:
            for i in range(65530):
                if t>=len(llistaComandos):
                    break
                archivo.write(llistaComandos[i + c*65530] + "\n")
                t = t+1
        
        
        print(f"Las líneas se han guardado en {str(c) + nombre_archivo}")
        c = c+1

def generarCarasIcosaedro(r):
    bloquesCaras = []
    for triangulo in triangulosIcosaedro(r):
        bloquesCaras = bloquesCaras + llenarTriangulo(triangulo)
    return bloquesCaras

def generarCaras(r):
    bloquesCaras = []

    lista = triangulosIcosaedro(r)
    lista = aumentarTriangulos(lista, r)

    for triangulo in lista:
        bloquesCaras = bloquesCaras + llenarTriangulo(triangulo)
    return bloquesCaras

def main():

    radio = 200
    grosorCaras = 0
    grosorAristas = 1
    grosorEsquinas = 2
    densidadTriangulos = 2
    
    
    
    info = True

    if info:
        print("Eliminando archivos anteriores:")
    print("Generando domo geodésico de radio ", radio)

    for i in range(20):
        nombre = str(i) + "aristas.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = str(i) + "esquinas.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = str(i) + "caras.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)

        nombre = str(i) + "bola.mcfunction"
        if os.path.isfile(nombre):
            os.remove(nombre)
            if info:
                print("  Se ha eliminado " + nombre)


    print("Generando icosaedro...")
    conjuntoTriangulos = triangulosIcosaedro(radio)
    #print(conjuntoTriangulos)
    print("Generando triangulos intermedios...")
    conjuntoTriangulos = aumentarMuchosTriangulos(conjuntoTriangulos, radio, densidadTriangulos)
    #print("Triangulos: ", conjuntoTriangulos)
    print("Generando las aristas...")
    conjuntoAristas = aristasDeTriangulos(conjuntoTriangulos)
    #print("Aristas: ", conjuntoAristas)
    print("Generando las esquinas")
    conjuntoEsquinas = esquinasDeTriangulos(conjuntoTriangulos)
    print("Adaptando coordenadas de esquinas")
    conjuntoEsquinas = redondearPuntosConjunto(conjuntoEsquinas, 0)
    print("Ensanchando las esquinas")
    conjuntoEsquinas = agrandarBordes(conjuntoEsquinas, grosorEsquinas, info)
    print("Adaptando coordenadas de esquinas")
    conjuntoEsquinas = redondearPuntosConjunto(conjuntoEsquinas, 0)

    print("Rellenando las caras")
    conjuntoTriangulos = llenarConjuntoTriangulos(conjuntoTriangulos)
    print("Adaptando las coordenadas de las caras")
    conjuntoTriangulos = redondearPuntosConjunto(conjuntoTriangulos,0)
    print("Ensanchando las caras")
    conjuntoTriangulos = agrandarBordes(conjuntoTriangulos,grosorCaras, info)
    print("Volviendo a adaptar las coordenadas de las caras")
    conjuntoTriangulos = redondearPuntosConjunto(conjuntoTriangulos,0)
    #print("Triangulos: ", conjuntoTriangulos)
    print("Rellenando las aristas")
    conjuntoAristas = llenarConjuntoAristas(conjuntoAristas)
    print("Adaptando las coordenadas de las aristas")
    conjuntoAristas = redondearPuntosConjunto(conjuntoAristas,0)
    print("Ensanchando las aristas")
    conjuntoAristas = agrandarBordes(conjuntoAristas, grosorAristas, info)
    print("Volviendo a adaptar las coordenadas de las aristas")
    conjuntoAristas = redondearPuntosConjunto(conjuntoAristas,0)
    #print("Aristas: ", conjuntoAristas)

    print("funcion creada para colocar bloques")
    com = listaComandos(conjuntoTriangulos, "glass")
    print("   Cara: ", len(com))
    escribir_en_archivo("caras.mcfunction", com)
    #print(conjuntoTriangulos)
    com = listaComandos(conjuntoAristas, "quartz_block")
    escribir_en_archivo("aristas.mcfunction", com)
    print("   Arista: ", len(com))
    #print(conjuntoAristas)
    com = listaComandos(conjuntoEsquinas, "diamond_block")
    escribir_en_archivo("esquinas.mcfunction", com)
    print("   Esquina: ", len(com))
    #com = listaComandos(redondearPuntosConjunto(crearEsfera((0,0,0),1),0), "diamond_block")
    #escribir_en_archivo("bola.mcfunction", com)
    
if __name__ == "__main__":
    main()