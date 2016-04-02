from random import randint

import numpy as np

from core.generators.Neighbours import swap2
from core.searches.local.advance.VNS import VNS
from main.QAP.search.advance.QAPAdvLocalSearch import Read_QAP_Instance, QAPProblem, qapCostEvaluator


class QAPProblemVNS(VNS):

    def __init__(self, init_solution, n, mDist, mFlux, max_e=None, nrep=None, maxC=None, minC=None, maximize=False):
        if mDist is not None and mFlux is not None and n:
            # Se obtienen las matrices de distanci y flujo,
            self.n = n
            self.mDist = mDist
            self.mFlux = mFlux
            self.max_evals = max_e

            # Se crea la clase especifica para aplicar enfriamiento estadístico al problema //TODO establecer tiempos de CPU
            # nrep corresponde con el número de vecindarios
            VNS.__init__(self, init_solution, nrep, maximize, None)
            # k=int(max_e/nrep) en este caso solo me interesa el mejor de cada búsqueda
            self.qap = QAPProblem(self.state, n, mDist, mFlux, int(max_e/nrep), int(max_e/nrep), nrep, maxC, minC, maximize=maximize)
        else:
            raise ValueError(" Error en los argumentos no ha sido posible obtener todos los elementos que conforman el problema ")

    def local_search(self, *args):
        """
        """
        self.qap.state = args[0]
        return self.qap.search(True)

    def cost(self, *kwargs):
        """
        """
        super().cost(*kwargs)
        return qapCostEvaluator(self.mDist, self.mFlux, kwargs[0]['solution'], self.n)

    def shake(self, *args):
        """
        """
        neighborhood = self.N[args[0]]
        return neighborhood[randint(0, neighborhood.shape[0] - 1)]

    def generate_n(self, *argv):
        """
        """
        solution = argv[1]
        for k in range(argv[0]):
            neighbour = swap2(np.asarray(solution))
            self.N[k] = neighbour
            solution = neighbour[randint(0, neighbour.shape[0] - 1)]


def QAPAdvVNSLocalSearch(fName, solution, max_eval, nrep = None, maxC= None, minC=None):

    """
    Método búsqueda local usando enfriamiento estadístico
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
         >>> QAPAdvLocalSearch('../../Instances/QAP/test/Cebe.qap.n10.1', [1,1,1,1,1,0,0,0,0,0],100,10)
    """

    # Se obtienen las matrices de distanci y flujo,
    n, mDist, mFluj = Read_QAP_Instance(fName)

    # Se crea la clase especifica para aplicar enfriamiento estadístico al problema
    qapVNS = QAPProblemVNS(solution, n, mDist, mFluj, max_eval, nrep, maxC, minC, maximize=False)
    return qapVNS.basic_vns()

if __name__ == '__main__':
    # fName = sys.argv[1]
    # sol = eval(sys.argv[2])
    # max_evals = eval(sys.argv[3])
    # k = eval(sys.argv[4])
    bestsol, bestvals = QAPAdvVNSLocalSearch('../Instances/QAP/test/Cebe.qap.n10.1', [1,2,3,4,5,6,7,8,9,10], max_eval=300000, nrep=10)
    print(bestsol, bestvals)