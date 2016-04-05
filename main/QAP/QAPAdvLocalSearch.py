#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import randint

import numpy as np

from core.evaluators.QAPEvaluator import Read_QAP_Instance, qapCostEvaluator
from core.generators.Neighbours import swap2
from core.searches.local.advance.Anneal import Anneal


class QAPProblem(Anneal):

    """
    Clase que hereda de la clase Anneal del módulo core.searches.local.advance.Anneal, que implementa el enfriamiento estadístico generalizado. BIPProblem cubre
    el problema de bipartición balanceada del grafo.
    """
    def __init__(self, solution, n=None, mDist=None, mFlux=None, max_e= None, k= None , nrep=1, maxC= None, minC=None, maximize=False):
        """
        nrep=1 Lundy & Mess (1986)
        """
        if mDist is not None and mFlux is not None and n:
            self.mDist = mDist
            self.n = n
            self.mFlux = mFlux
            Anneal.__init__(self, solution, max_e, k, nrep, maxC, minC, maximize=maximize)
        else:
            raise ValueError("Error, la instancia del problema BIP es requerida")

    def energy(self):
        """
        Función objetivo/coste del problema de asignación cuadrática del módulo main.QAP.QAPEvaluator
        """
        return qapCostEvaluator(self.mDist, self.mFlux, self.state, self.n)

    def transition(self):
        """
        Función de generación del vecindario swap201 del módulo core.generators.Neighbours
        """
        neighbour = swap2(np.asarray(self.state))
        self.state = neighbour[randint(0, neighbour.shape[0]-1)]


def QAPAdvLocalSearch(fName, solution, max_eval, k, nrep = 1, maxC= None, minC=None):

    """
    Método búsqueda VNS usando enfriamiento estadístico como búsqueda local
    nrep=1 Lundy & Mess (1986)
    :param fName: archivo con la instancia del problema de asignación cuadrática
    Formato txt:
    10
    0   126   1345   244   796   1018   7   151   347   1922
    126   0   635   239   1358   1434   1448   25   1437   215
    1345   635   0   1447   939   1431   187   1997   300   249
    244   239   1447   0   412   286   203   26   1164   996
    796   1358   939   412   0   1612   187   295   1569   644
    1018   1434   1431   286   1612   0   902   440   1011   352
    7   1448   187   203   187   902   0   1176   591   1562
    151   25   1997   26   295   440   1176   0   284   929
    347   1437   300   1164   1569   1011   591   284   0   67
    1922   215   249   996   644   352   1562   929   67   0
    0   0   5   0   0   0   0   0   5   0
    0   0   1271   3205   0   21   143   5   222   0
    0   0   0   10   1   0   0   3   0   26
    28   0   0   0   0   2   0   631   0   0
    0   0   0   511   0   805   2   7315   0   0
    5632   0   0   3036   1   0   0   0   0   75
    0   0   0   9   0   0   0   0   8   1
    0   4   0   0   107   33   1   0   3   3240
    0   0   7   516   42   0   700   0   0   12
    1   0   0   0   0   2   0   0   0   0

    :param solution: solución inicial propuesta
    :param max_eval: número máximo de evaluaciones
    :param k: almacenar mejor valor de la energía cada k evaluaciones
    :return: La mejor solución y los k mejores valores obtenidos en la búsqueda
    Ejemplo de ejecución:
         >>> QAPAdvLocalSearch('../../Instances/BIP/test/Cebe.qap.n10.1', [1,1,1,1,1,0,0,0,0,0],100,10)
    """

    # Se obtienen las matrices de distanci y flujo,
    n, mDist, mFluj = Read_QAP_Instance(fName)
    #Se crea la clase especifica para aplicar enfriamiento estadístico al problema
    qap = QAPProblem(solution, n, mDist, mFluj, max_eval, k, nrep, maxC, minC)
    return qap.search(True)

if __name__ == '__main__':
    # fName = sys.argv[1]
    # sol = eval(sys.argv[2])
    # max_evals = eval(sys.argv[3])
    # k = eval(sys.argv[4])
    # bestsol, bestval = BipLocalSearch(fName , sol, max_evals, k)
    bestsol, bestval = QAPAdvLocalSearch('../Instances/QAP/test/Cebe.qap.n10.1', [1,2,3,4,5,6,7,8,9,10], 100, 10)
    print(bestsol, bestval)



