import abc
from abc import ABCMeta
import logging
import sys
from deap import creator, tools, base
import numpy as np


log = logging.getLogger("AG")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class AG(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def naturalSelection(self):
        """Criterio de selección natural para soluciones no factibles"""
        pass

    @abc.abstractmethod
    def createMaxRace(self):
        """
        Función que genera los tipos deap necesarios y define el problema de optimización (max Vs. min)
        """
        pass

    @abc.abstractmethod
    def evaluation(self):
        """
        Función de adaptación

        """
        pass


    @abc.abstractmethod
    def buildBipRandomPopulation(self, *argv):
        """
        """
        toolbox = argv[2]
        l = argv[1]
        size = argv[0]
        toolbox.register("indices", self.bornBipRandomfenotype, l)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        # Definimos la población a partir de los individuos
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        return toolbox.population(n=size)

    def AG(self,fName, pobSize, genNums, verbose=False):
        """
        Pre:El problema que resuelve es de maximización.
        Post:
        """

        self.createMaxRace()

        # Heredamos las clases y funciones implementadas como parte de DEAP
        toolbox = base.Toolbox()

        # Leemos la instancia del problema de Bipartición del grafo
        instance = bie.readBipartInstance(fName)
        n = instance.shape[0]

        # Obtenemos la población inicial de soluciones factibles de forma aleatoria
        population = self.buildBipRandomPopulation(pobSize, n, toolbox)

        # Asociamos como función de aptitud la función evalBip
        toolbox.register("evaluate", self.evaluation, instance, n, verbose=verbose)
        # Nuestro operador de cruzamiento será el recomendado cruzamiento en 2 puntos
        toolbox.register("mate", tools.cxTwoPoint)
        # El operador de mutación cambiará 1-->0  y 0-->1 con una probabilidad
        # de mutación de 1/(lambda**0.9318)*(l**0.4535) recomendada
        toolbox.register("mutate", tools.mutFlipBit, indpb=1 / ((pobSize ** 0.9318) * (n ** 0.4535)))
        # Usaremos selección por torneo con un parámetro de torneo = 3
        toolbox.register("select", tools.selTournament, tournsize=3)
        # Incluimos los
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        # Obtenemos el resultado de el mejor valor de la funcion obtenido por el
        # algoritmo en cada generación
        stats.register("max", max)

        # Para obtener el mejor individuo que nunca ha existido en la población, deacuerdo a la función de evaluación
        hof = tools.HallOfFame(1, similar=np.array_equal)

        # Probabilidad de cruzamiento 0.8
        # Probabilidad de aplicar el operador de mutación 0.2
        rdo = algorithms.eaSimple(population, toolbox, stats=stats, cxpb=0.8, mutpb=0.2, ngen=genNums, halloffame=hof,
                                  verbose=True)

        evals = [dic['max'] for dic in rdo[1]]
        return (hof[0], sorted(evals))