from icosaedro import *
import shutil
import os

maxComandos = 2147483647

# Posibles expansiones:
# Usar otras figuras para las caras
# Usar otros sólidos platónicos
# Implementar multinúcleo

# C:\Users\druss\AppData\Roaming\.minecraft\saves\New World

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

def comandoFinal(ns:list[int], carpeta,  nombre):


    comandoGeneral = '$function '+nombre +":"
    with open(carpeta+ "domo.mcfunction", 'a') as archivo:
        for i in range(ns[2]):
            comando = comandoGeneral + "caras"+str(i) + ' {cara:"$(cara)"}'
            archivo.write(comando + "\n")
        for i in range(ns[1]):
            comando = comandoGeneral + "aristas"+str(i) + ' {arista:"$(arista)"}'
            archivo.write(comando + "\n")
        for i in range(ns[0]):
            comando = comandoGeneral + "esquinas"+str(i) + ' {esquina:"$(esquina)"}'
            archivo.write(comando + "\n")



# Dada una lista de comando de minecraft, escrive cada uno en un archivo de un nombre dado
def escribir_en_archivo(nombre_archivo, llistaComandos, info=False):
    lim = 65530
    c=0
    t = 0
    while t<len(llistaComandos):
        direccion = nombre_archivo + str(c) + ".mcfunction"
        with open(direccion, 'a') as archivo:
            for i in range(lim):
                if t>=len(llistaComandos):
                    break
                archivo.write(llistaComandos[i + c*lim] + "\n")
                t = t+1
        
        if info:
            print(f"Las líneas se han guardado en {direccion}")
        c = c+1
    return c


def checkFiles(carpeta):
    if os.path.exists(carpeta):
        return False
    else:
        os.makedirs(carpeta)
        return True

def crearInicio(carpeta: str):
    carpetaJSON = carpeta + "/minecraft"
    checkFiles(carpetaJSON)
    carpetaJSON = carpetaJSON + "/tags"
    checkFiles(carpetaJSON)
    carpetaJSON = carpetaJSON + "/function"
    checkFiles(carpetaJSON)
    shutil.copy("doc/load.json", carpetaJSON)
    #shutil.copy(os.path.dirname(os.path.abspath(__file__)) + "/tick.json", carpetaJSON)

    carpeta = carpeta + "/main"
    checkFiles(carpeta)
    carpeta = carpeta + "/function"
    checkFiles(carpeta)
    shutil.copy("doc/repetir.mcfunction", carpeta)
    #shutil.copy(os.path.dirname(os.path.abspath(__file__)) + "/iniciar.mcfunction", carpeta)



def creacionDomo(densidadTriangulos:int, radio:int, grosorCaras:int, grosorAristas:int, grosorEsquinas:int, root:str, titulo:str, info:bool = False):
    # Importante! en el radio no se cuenta el grosor de las paredes!

    titulo = titulo.lower()


    generarCaras = True
    generarAristas = True
    generarEsquinas = True

    bloqueCaras = "cara"
    bloqueAristas = "arista"
    bloqueEsquinas = "esquina"
    
    carpeta = root + "/datapacks/DomeCraft"

    if checkFiles(carpeta):
        print("Creando datapack")
        shutil.copy("doc/pack.mcmeta", carpeta)

    carpeta = carpeta + "/data"
    checkFiles(carpeta)
    crearInicio(carpeta)
    carpeta = carpeta + "/" + titulo
    checkFiles(carpeta)
    carpeta = carpeta + "/function"
    checkFiles(carpeta)
    carpeta = carpeta + "/"

    if info:
        print("Eliminando archivos anteriores:")

    nombre = carpeta + "domo.mcfunction"
    if os.path.isfile(nombre):
        os.remove(nombre)
        if info:
            print("  Se ha eliminado " + nombre)

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

    if info:
        print("Generando domo geodésico de radio ", radio)

    if info:
        print("Generando icosaedro...")
    conjuntoTriangulos = triangulosIcosaedro(radio)

    if info:
        print("Generando triangulos intermedios...")
    conjuntoTriangulos = aumentarMuchosTriangulos(conjuntoTriangulos, radio, densidadTriangulos)

    if generarEsquinas:
        if info:
            print("Generando las esquinas")
        conjuntoEsquinas = esquinasDeTriangulos(conjuntoTriangulos)
        if info:
            print("Ensanchando las esquinas")
        conjuntoEsquinas = agrandarBordes(conjuntoEsquinas, grosorEsquinas, info)

    if generarAristas:
        if info:
            print("Generando las aristas...")
        conjuntoAristas = aristasDeTriangulos(conjuntoTriangulos)
        if info:
            print("Rellenando las aristas")
        conjuntoAristas = llenarConjuntoAristas(conjuntoAristas)
        if info:
            print("Ensanchando las aristas")
        conjuntoAristas = agrandarBordes(conjuntoAristas, grosorAristas, info)

    if generarCaras:
        if info:
            print("Rellenando las caras")
        conjuntoTriangulos = llenarConjuntoTriangulos(conjuntoTriangulos)
        if info:
            print("Ensanchando las caras")
        conjuntoTriangulos = agrandarBordes(conjuntoTriangulos,grosorCaras, info)

    if info:
        print(len(conjuntoTriangulos), len(conjuntoAristas), len(conjuntoEsquinas))

    suma = 0
    
    narchivos = [0,0,0]
    if generarCaras:
        if info:
            print("Creando comandos para generar las caras...")
        com = listaComandos(conjuntoTriangulos, bloqueCaras)
        narchivos[2] = escribir_en_archivo(carpeta + "caras", com)
        if info:
            print("   Las caras constan de ", len(com), " bloques")
    
    suma = suma + len(com)
    
    if generarAristas:
        if info:
            print("Creando comandos para generar las aristas...")
        com = listaComandos(conjuntoAristas, bloqueAristas)
        narchivos[1] = escribir_en_archivo(carpeta + "aristas", com)
        if info:
            print("   Las aristas constan de ", len(com), " bloques")
    
    suma = suma + len(com)
    
    if generarEsquinas:
        if info:
            print("Creando comandos para generar las esquinas...")
        com = listaComandos(conjuntoEsquinas, bloqueEsquinas)
        narchivos[0] = escribir_en_archivo(carpeta + "esquinas", com)
        if info:
            print("   Las esquinas constan de ", len(com), " bloques")

    suma = suma + len(com)

    if suma>maxComandos-300:
        print("ERROR: DEMASIADOS BLOQUES, LA CÚPULA NO SE GENERARA CORRECTAMENTE")

    if info:
        print("Creando comando final...")
    comandoFinal(narchivos, carpeta, titulo)



if __name__ == "__main__":
    creacionDomo(1,30,0,1,2,"C:/Users/druss/AppData/Roaming/.minecraft/saves/Prueba", "hola", True)
