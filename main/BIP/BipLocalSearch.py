#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from core.evaluators import BipEvaluator as bie
from core.searches.local.basic.BasicLocalSearches import  BIPLocalSearchSwap201


def BipLocalSearch(fName, solution):
    """
    pre:El archivo debe contener el formato de instancia de grafo,
    es decir debe contener tanto la matriz de pesos de las aristas
    post:Deveulve la solución y el valor obtenidos por la función de
    coste, para una búsqueda local básica
    """
    bipartInstance = bie.readBipartInstance(fName)
    return BIPLocalSearchSwap201(bipartInstance, solution)
#    return (solution, bestVal)

if __name__ == '__main__':
    fName = sys.argv[1]
    sol = eval(sys.argv[2])
    balanceado = sum(sol) == len(sol)/2
    if not balanceado:
     exit("La solución propuesta no esta balanceada")
    bestsol, bestval = BipLocalSearch(fName , sol)
    print(bestsol, bestval)



