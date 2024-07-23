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



def main():

    radio = 60
    grosorCaras = 0
    grosorAristas = 1
    grosorEsquinas = 3
    densidadTriangulos = 3
    
    generarCaras = False
    generarAristas = True
    generarEsquinas = True
    
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


    if generarCaras:
        print("Creando comandos para generar las caras...")
        com = listaComandos(conjuntoTriangulos, "glass")
        print("   Las caras constan de ", len(com), " bloques")
        escribir_en_archivo("caras.mcfunction", com)
    
    if generarAristas:
        print("Creando comandos para generar las aristas...")
        com = listaComandos(conjuntoAristas, "quartz_block")
        escribir_en_archivo("aristas.mcfunction", com)
        print("   Las aristas constan de ", len(com), " bloques")
    
    if generarEsquinas:
        print("Creando comandos para generar las esquinas...")
        com = listaComandos(conjuntoEsquinas, "diamond_block")
        escribir_en_archivo("esquinas.mcfunction", com)
        print("   Las esquinas constan de ", len(com), " bloques")

    
if __name__ == "__main__":
    main()