#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint
import sys

import numpy as np

from core.evaluators.BipEvaluator import calcBipartCost,readBipartInstance
from core.generators.Neighbours import swap201
from core.searches.local.advance.Anneal import Anneal


class BIPProblem(Anneal):

    """
    Clase que hereda de la clase Anneal del módulo core.searches.local.advance.Anneal, que implementa el enfriamiento estadístico generalizado. BIPProblem cubre
    el problema de bipartición balanceada del grafo.
    """
    def __init__(self, solution, instance = None, max_e= None, k= None , nrep = 1, maxC= None, minC=None):
        """
        nrep=1 Lundy & Mess (1986)
        """
        if instance is not None:
            self.instance = instance
            self.n = len(instance)
            Anneal.__init__(self, solution, max_e, k, nrep, maxC, minC)
        else:
            raise ValueError("Error, la instancia del problema BIP es requerida")

    def energy(self):
        """
        Función objetivo/coste del problema de bipartición del grafo del módulo main.BIP.BipEvaluator
        """
        return calcBipartCost(self.instance, self.n, self.state)

    def transition(self):
        """
        Función de generación del vecindario swap201 del módulo core.generators.Neighbours
        """
        neighbour = swap201(np.asarray(self.state))
        self.state = neighbour[randint(0, neighbour.shape[0]-1)]


def BipAdvLocalSearch(fName, solution, max_eval, k, nrep = 1, maxC= None, minC=None):

    """
    Método búsqueda local usando enfriamiento estadístico
    nrep=1 Lundy & Mess (1986)
    :param fName: archivo con la instancia del problema de bipartición del grafo.
    Formato txt:
    10
    0   3   23   33   16   18   11   31   19   42
    3   0   29   30   31   51   23   48   31   24
    23   29   0   38   21   41   62   10   24   7
    33   30   38   0   45   21   32   34   6   36
    16   31   21   45   0   19   20   20   30   34
    18   51   41   21   19   0   29   25   40   31
    11   23   62   32   20   29   0   14   32   45
    31   48   10   34   20   25   14   0   35   14
    19   31   24   6   30   40   32   35   0   36
    42   24   7   36   34   31   45   14   36   0
    :param solution: solución inicial propuesta
    :param max_eval: número máximo de evaluaciones
    :param k: almacenar mejor valor de la energía cada k evaluaciones
    :return: La mejor solución y los k mejores valores obtenidos en la búsqueda
    Ejemplo de ejecución:
         >>> BipAdvLocalSearch('../../Instances/BIPART/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0],100,10)
    """
    balanceado = sum(solution) == len(solution)/2
    if not balanceado:
     exit("La solución propuesta no esta balanceada")

    bipartInstance = readBipartInstance(fName)
    bip = BIPProblem(solution, bipartInstance, max_eval, k, nrep, maxC, minC)
    return bip.search(True)

if __name__ == '__main__':
    fName = sys.argv[1]
    sol = eval(sys.argv[2])
    max_evals = eval(sys.argv[3])
    k = eval(sys.argv[4])
    bestsol, bestvals = BipAdvLocalSearch(fName , sol, max_evals, k)
    # bestsol, bestvals = BipAdvLocalSearch('../Instances/BIP/test/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0],5000,100)
    # sol = np.concatenate((np.ones([25],dtype=int),np.zeros([25],dtype=int)), axis=0)
    # bestsol, bestval = BipAdvLocalSearch('../Instances/BIP/Cebe.bip.n50.1', np.random.permutation(sol), 5000, 100)
    print(bestsol, bestvals)



