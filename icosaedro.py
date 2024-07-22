import numpy as np
from math import sqrt, cos, sin, pi
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI = (1+sqrt(5))/2

# Clases de objetos:
# Puntos: son 3-tuplas
# Aristas: frozenSets con 2 puntos
# Triangulos: frozenSets con 3 puntos
# Conjuntos de puntos: conjuntos que sus elementos son puntos

def triangulosIcosaedro(r):
    esquinas = np.array(esquinasIcosaedro(r))

    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    conjuntTriangles = set()
    for face in faces:
        conjuntTriangles.add(frozenset([tuple(esquinas[face[0]].tolist()), tuple(esquinas[face[1]].tolist()), tuple(esquinas[face[2]].tolist())]))
    return conjuntTriangles

def llenarTriangulo(triangulo: list):
    triangulo = list(triangulo)
    P0 = np.array(triangulo[0])
    P1 = np.array(triangulo[1])
    P2 = np.array(triangulo[2])

    steps = int(np.linalg.norm(P0-P1))+10

    puntos = set()

    for i in range(steps+1):
        for j in range(steps+1):
            k = 1 - j/steps - i/steps
            if not (k<0 or k>1):
                puntos.add(tuple((P0*i/steps + P1*j/steps + P2*k).tolist()))

    return(puntos)

def escalarPuntos(radio, lista):
    for i in range(len(lista)):
        for j in range(3):
            lista[i][j] = lista[i][j]*radio
    return lista

def crearEsfera(P, r):
    conjuntoEsfera = set([P])
    P = np.array(P)

    if r==0:
        return conjuntoEsfera

    if r==1:
        conjuntoEsfera.add(tuple((P+np.array([1,0,0])).tolist()))
        conjuntoEsfera.add(tuple((P+np.array([-1,0,0])).tolist()))
        conjuntoEsfera.add(tuple((P+np.array([0,1,0])).tolist()))
        conjuntoEsfera.add(tuple((P+np.array([0,-1,0])).tolist()))
        conjuntoEsfera.add(tuple((P+np.array([0,0,1])).tolist()))
        conjuntoEsfera.add(tuple((P+np.array([0,0,-1])).tolist()))
        return conjuntoEsfera
    

    for l in range(1,int(2*r)):
        l = l/2
        for phi in range(int(4*l+1)):
            phi = pi*phi/(4*l)
            for teta in range(int(8*l+1)):
                teta = 2*pi*teta/(8*l)
                
                nuevoPunto = P+np.array([l*cos(phi), l*sin(phi)*cos(teta), l*sin(phi)*sin(teta)])
                conjuntoEsfera.add(tuple(nuevoPunto.tolist()))
    return conjuntoEsfera


def agrandarBordes(conjuntoPuntos, g, ix:bool = False):
    
    if g==0:
        return conjuntoPuntos
    nuevoConjunto = set()
    if ix:
        print("Agrandando puntos en ",g)
        tamaño = len(conjuntoPuntos)
        c=0

    tamaño = len(conjuntoPuntos)

    for P in conjuntoPuntos:
        nuevoConjunto = nuevoConjunto.union(crearEsfera(P,g))
        if ix:
            if c%10==0:
                print(c, "/",tamaño)
            c=c+1
    if ix:print()
    return nuevoConjunto




def redondearPuntosConjunto(conjuntoPuntos, decimales):
    nuevoConjunto = set()
    for punto in conjuntoPuntos:
        puntoAprox = tuple([round(punto[0],decimales), round(punto[1],decimales), round(punto[2],decimales)])
        nuevoConjunto.add(puntoAprox)
    return nuevoConjunto


def esquinasIcosaedro(r):
    esquinas = [
        [-1,  PHI,  0], [ 1,  PHI,  0], [-1, -PHI,  0], [ 1, -PHI,  0],
        [ 0, -1,  PHI], [ 0,  1,  PHI], [ 0, -1, -PHI], [ 0,  1, -PHI],
        [ PHI,  0, -1], [ PHI,  0,  1], [-PHI,  0, -1], [-PHI,  0,  1],
    ]

    esquinas = escalarPuntos(r/1.9021, esquinas)

    return esquinas


def dividirTriangulo(triangulo, r):
    triangulo = list(triangulo)
    P0 = np.array(triangulo[0])
    P1 = np.array(triangulo[1])
    P2 = np.array(triangulo[2])

    P01 = (P0+P1)/2
    P02 = (P0+P2)/2
    P12 = (P1+P2)/2

    P01 = r*P01/np.linalg.norm(P01)
    P02 = r*P02/np.linalg.norm(P02)
    P12 = r*P12/np.linalg.norm(P12)

    P0 = tuple(P0.tolist())
    P1 = tuple(P1.tolist())
    P2 = tuple(P2.tolist())
    P01 = tuple(P01.tolist())
    P02 = tuple(P02.tolist())
    P12 = tuple(P12.tolist())
    conjunto = {frozenset([P0, P01, P02]), frozenset([P1,P12, P01]), frozenset([P2,P02,P12]), frozenset([P01, P02, P12])}
    
    return conjunto


def aumentarTriangulos(listaTriangulos, r):
    listaNueva = set()
    for triangulo in listaTriangulos:
        listaNueva = listaNueva.union(dividirTriangulo(triangulo,r))
    return listaNueva

def aumentarMuchosTriangulos(listaTriangulos, r, n):
    if n<0:
        print("ERROR, n<0")
    else:
        for i in range(n):
            
            listaTriangulos = aumentarTriangulos(listaTriangulos, r)

    return listaTriangulos


def esquinasDeTriangulos(listaTriangulos):
    conjunto = set()
    for triangulo in listaTriangulos:
        for P in triangulo:
            conjunto.add(P)
    return conjunto

def aristasDeTriangulos(listaTriangulos):
    conjunto = set()
    for triangulo in listaTriangulos:
        for P in triangulo:
            for Q in triangulo:
                if P!=Q:
                    conjunto.add(frozenset([P,Q]))


    return conjunto

def llenarArista(arista):
    arista = list(arista)
    P0 = np.array(arista[0])
    P1 = np.array(arista[1])

    steps = int(np.linalg.norm(P0-P1))+10

    conjunto = set()

    for i in range(steps+1):
        puntoIntermedio = (P0*i/steps+P1*(1-i/steps))
        conjunto.add(tuple(puntoIntermedio.tolist()))

    return conjunto

def llenarConjuntoAristas(conjuntoAristas):
    conjunto = set()
    for arista in conjuntoAristas:
        conjunto = conjunto.union(llenarArista(arista))
    return conjunto

def unirConjunto(conjuntoAristas):
    conjuntoFinal = set()
    for conjunt in conjuntoAristas:
        conjuntoFinal.union(conjunt)

    return conjuntoFinal

def llenarConjuntoTriangulos(conjuntoTriangulos):
    conjuntoPuntos = set()
    c=0
    tamño = len(conjuntoTriangulos)
    for triangulo in conjuntoTriangulos:
        conjuntoPuntos = conjuntoPuntos.union(llenarTriangulo(triangulo))
        if c%10==0:
            print(str(c) + "/" + str(tamño))
        c= c+1
    return conjuntoPuntos



