import abc
from abc import ABCMeta
import logging
import sys
import numpy as np
import copy


log = logging.getLogger("Anneal")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class Anneal(object):
    __metaclass__ = ABCMeta

    """
    Clase abstracta que permite aplicar la búsqueda local basada en los fundamentos del Recocido Simulado a cualquier
    tipo de problema de optimización combinatoria. La presente versión cubre aquellos casos que buscan maximizar.
    """
    maxC = 30000.
    minC = 3
    max_evals = 1000
    nrep = 100
    k = 10
    maximize = True

    def __init__(self, init_solution=None, max_e=None, k=None, nrep=None, maxC=None, minC=None, maximize=None):
        """
        :param init_solution: solución de partida
        :param max_e: número máximo de evaluaciones, valor por defecto 1000
        :param k: almacenar mejor valor de la energía cada k evaluaciones, valor por defecto 100
        :param nrep: número de evaluaciones sin variar la temperatura
        :param maxC: valor máximo del parámetro de control, valor por defecto 30000
        :param minC: valor mínimo que puede alcanzar el parámetro de control c, valor por defecto 3
        :param maximize: boolean que determina si se maximiza o minimiza la función objetivo, por defecto se maximiza
        :return void
        """
        if init_solution is not None:
            self.state = init_solution
            if max_e:
                self.max_evals = max_e
            if k:
                self.k = k
            if nrep:
                self.nrep = nrep
            if maxC:
                self.maxC = maxC
            if minC:
                self.minC = minC
            if maximize is not None:
                self.maximize = maximize
        else:
            raise ValueError("Es necesaria una solución inicial")

    @abc.abstractmethod
    def energy(self):
        """REQUERIDO: Equivalente a la función de coste, calcula el cambio de energía"""
        pass

    @abc.abstractmethod
    def transition(self):
        """REQUERIDO: Cambios de estado, transforma la solución actual en una subsecuente"""
        pass

    def control(self, c, beta = 10^(-100)):
        """
        Actualiza la temperatura según el programa de enfriamiento propuesto por Lundy y Mees en 1986
        t-->t/(1+beta*t)
        :param beta: parámetro que controla la velocidad de reducción de la temperatura, por defecto 19(-100)
        :param c:
        :return la temperatura enfriada con el criterio indicado
        """
        return c / (1 + beta*c)

    def search(self, verbose=False):
        """
        Búsqueda local avanzada, enfriamiento estadístico Simulated Annealing
        """
        if verbose:
            log.setLevel(logging.DEBUG)     # establece el modo debug
        evals = 0

        # estado inicial
        c = self.maxC  # parámetro de control inicial
        energy = self.energy() # evaluación de la solución inicial
        bestEnergy = energy  # mejor valor para la energía
        bestState = copy.copy(self.state)  # mejor estado
        best_energy_among_neighbors = bestEnergy  # energía anterior
        best_state_among_neighbors = copy.copy(bestState)  # estado anterior

        # para devolver las k mejores soluciones
        bestEnergies = np.asarray([], dtype=int)
        bestEnergies = np.append(bestEnergies, energy)

        cool = False    # criterio de parada cuando el sistema está frío

        self.start_message()

        while evals < self.max_evals and not cool:
            # Repetir hasta que el sistema esté frío o se alcance el número máximo de evaluaciones

            for rep in range(self.nrep):    # número de repeticiones sin cambiar temperatura
                evals += 1  # Se tiene en cuenta la evaluación inicial
                log.debug("Searching {0:.0f}%".format((self.max_evals - evals) * 100 / self.max_evals))
                self.transition()   # obtener una solución del entorno
                energy = self.energy()  # calcular el nuevo valor de la energía

                # Criterio de actualización de la solución
                if self.maximize:
                    delta = energy - best_energy_among_neighbors  # en caso de maximización
                else:
                    delta = best_energy_among_neighbors - energy  # en caso de minimización
                if delta <= 0:
                    best_energy_among_neighbors = energy
                    best_state_among_neighbors = self.state
                    log.debug("Actualizado a un valor de energía mejor en el entorno {}".format(energy))
                elif -delta / c > np.random.random_sample(size=1)[0]:  # obtener la probabilidad uniforme
                    best_energy_among_neighbors = energy
                    log.debug("Actualizado a un valor de energía peor en el entorno {}".format(energy))

                # Se determina si ha habido mejora con respecto al ciclo anterior
                if self.maximize:
                    improve = (best_energy_among_neighbors > bestEnergy)
                else:
                    improve = (best_energy_among_neighbors < bestEnergy)
                if improve:
                    bestEnergy = best_energy_among_neighbors  # Se actualiza el mejor valor y la mejor solución
                    bestState = best_state_among_neighbors
                    log.debug(bestEnergy)

                if evals % self.k == 0:     # se determina si hay que devolver la mejor solución hasta la evaluación actual
                    log.debug(bestEnergy)
                    log.debug(bestEnergies)
                    bestEnergies = np.append(bestEnergies, bestEnergy)

            c = self.control(c)
            cool = (c == self.minC)     # el sistema está frío cuando alcanza la temperatura mínima

        log.debug("Finish Simulated Annealing")
        return bestState, bestEnergies

    def start_message(self):
        log.debug("Start Simulated Annealing")
        if self.maximize:
            log.debug("Maximizando")
        else:
            log.debug("Minimizando")
        log.debug('Solución inicial: {}'.format(self.state))


