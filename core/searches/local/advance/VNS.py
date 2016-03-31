import abc
from abc import ABCMeta
import logging
import sys
import time
import numpy as np

log = logging.getLogger("VNS")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class VNS(object):
    __metaclass__ = ABCMeta

    neigh_max = 10  # número de vecindarios
    maximize = True
    state = None
    cost = None
    N = list([])  # vecindarios
    best_evals = np.array([])  # para devolver las mejores evaluaciones

    def __init__(self, init_solution=None, neigh_max=None, maximize=None, tmax= None):
        """
        :param init_solution: solución de partida
        :param max_e: número máximo de evaluaciones, valor por defecto 1000
        :param k: número de vecindades máximo generado valor por defecto 10
        :param maximize: boolean que determina si se maximiza o minimiza la función objetivo, por defecto se maximiza
        :param tmax: tiempo máximo de CPU permitido
        :return void
        """
        if init_solution is not None:
            self.state = init_solution
            self.cost = self.cost({'solution': self.state})
            if neigh_max:
                self.neigh_max = neigh_max
                self.N = [np.array([]) for i in range(neigh_max)]
            if maximize is not None:
                self.maximize = maximize
            if tmax:
                self.tmax = tmax
        else:
            raise ValueError("Es necesaria una solución óptima inicial")

    @abc.abstractmethod
    def shake(self, *args):
        """REQUERIDO: genera al azar una solución x1 del entorno de x """
        pass

    @abc.abstractmethod
    def local_search(self, *args):
        """REQUERIDO: Método de búsqueda local a utilizar sobre x1, denotar x1 el óptimo obtenido"""
        pass

    @abc.abstractmethod
    def cost(self, *kwargs):
        pass

    @abc.abstractmethod
    def generate_n(self, *argv):
        pass

    def basic_vns(self):
        """
        El número de vecindarios coincide con el número k de cada cuantas evaluaciones se guarda la mejor hasta el momento
        """
        # Inicializar
        best_vals = []
        best_vals = np.append(best_vals, self.cost)
        self.generate_n(self.neigh_max, self.state)
        control = 0
        neighborhood = 0

        # //TODO cpu time max
        start = time.time()
        while neighborhood < self.neigh_max:
            control += 1
            x1 = self.shake(neighborhood)
            x2, costs = self.local_search(x1)
            if self.maximize:
                cost2 = max(costs)
                if cost2 > self.cost:
                    self.state = x2
                    self.cost = cost2
                    neighborhood = 1
                else:
                    neighborhood += 1
            else:
                cost2 = min(costs)
                if cost2 < self.cost:
                    self.state = x2
                    self.cost = cost2
                    neighborhood = 1
                else:
                    neighborhood += 1
            self.best_evals = np.insert(self.best_evals,len(self.best_evals),self.cost)
        elapsed = time.time() - start
        log.info("Duración {:.3f} seconds".format(elapsed))
        log.info("Número de re-arranques {}".format(control-neighborhood))
        log.info("Número máximo de vecindarios construido {}".format(self.neigh_max))
        return self.state, self.best_evals
