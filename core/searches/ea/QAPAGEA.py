#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementación algoritmo genético para el problema de asignación cuadrática.

"""

import numpy as np
from deap import base, creator, tools, algorithms, gp
from core.evaluators.QAPEvaluator import Read_QAP_Instance
import random
import sys

# paralelización
import multiprocessing


def naturalSelection(fenotype, n):
    """
    Función que se encarga de la selección natural, es decir aquellos fenotipos
    que no son factibles en el contexto de QAP se les asigna 
    un 0 en la función de evaluación para que no puedan formar parte de la
    evolución genética
    """
    return list(range(1, n + 1)) == sorted(fenotype)


def naturalSelection(fenotype, n):
    """
    Función que se encarga de la selección natural, es decir aquellos fenotipos
    que no son factibles en el contexto de QAP se les asigna
    un 0 en la función de evaluación para que no puedan formar parte de la
    evolución genética
    """
    return list(range(1, n + 1)) == sorted(np.asarray(fenotype) + 1)


def createMinRace():
    """
    Función que genera los tipos deap necesarios para minimizar objetivo
    """
    # Se crea una clase FitnessMax para la maximización de funciones
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    # Se crea una clase individuo asociada a la clase FitnessMin
    creator.create("Individual", list, fitness=creator.FitnessMin)


def evalQAPEA(mDistance, mFlux, sol, n):
    """
    Función de adaptación diseñada para el problema de QAP y la recombinación de cromosomas ordenados.
    https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)
    http://www.obitko.com/tutorials/genetic-algorithms/crossover-mutation.php
    // TODO explicar porque se usan los índices.
    """
    fVal = sys.maxsize  # valor
    if not naturalSelection(sol, n):
        print("Soy una solución inutil", sol)
        return (fVal,)
    for i in range(n):
        for j in range(n):
            # Sólo se calcula/incrementa para indices distintos
            # fVal = fVal + (mDistance[i,j]*mFlux[sol[i]-1,sol[j]-1] if i!=j else 0)
            # Adaptación con el fin de poder utilizar el operador de recombinación de cromosomas ordenados
            # ya que ahora la función maneja los indices no es necesario restar 1
            fVal = fVal + (mDistance[i, j] * mFlux[sol[i], sol[j]] if i != j else 0)
    return (fVal,)


def QAPAGEA(fName, pobSize, genNums):
    """
    Función que utiliza el algoritmo UMDA para encontrar un óptimo sobre una instancia
    del problema de asignación cuadrática.
    """
    createMinRace()

    # Leemos la instancia del problema de asignación cuadrática
    vertices, mDistance, mFlux = Read_QAP_Instance(fName)

    n, N = vertices, pobSize
    toolbox = base.Toolbox()

    # paralelización work
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    # construinçmos la población
    toolbox.register("indices", random.sample, range(n), n)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    population = toolbox.population(n=pobSize)

    # función de adaptación
    toolbox.register("evaluate", evalQAPEA, mDistance, mFlux, n=n)
    # Nuestro operador de cruzamiento será   Ordered Crossover (OX) evolucionando la versión anterior la
    # función de evaluación
    toolbox.register("mate", tools.cxOrdered)
    # El operador de mutación cambiará dos posiciones del individuo con una probabilidad
    # de mutación de 1/(lambda**0.9318)*(l**0.4535) recomendada
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1 / ((pobSize ** 0.9318) * (n ** 0.4535)))
    # Usaremos selección por torneo con un parámetro de torneo = 3
    toolbox.register("select", tools.selTournament, tournsize=3)

    # estadísticos incluidos
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # algoritmo en cada generación
    stats.register("min", np.min)

    # Para obtener el mejor individuo que nunca ha existido en la población, deacuerdo a la función de evaluación
    hof = tools.HallOfFame(1, similar=np.array_equal)

    # Probabilidad de cruzamiento 0.8
    # Probabilidad de aplicar el operador de mutación 0.2
    rdo = algorithms.eaSimple(population, toolbox, stats=stats, cxpb=0.8, mutpb=0.2, ngen=genNums, halloffame=hof,
                              verbose=True)
    evals = [dic['min'] for dic in rdo[1]]
    for i in range(1, len(evals)):
        if evals[i] > evals[i - 1]:
            evals[i] = evals[i - 1]

    return np.asarray(hof[0]) + 1, evals


if __name__ == '__main__':
    fName = sys.argv[1]
    pobSize = eval(sys.argv[2])
    numGens = eval(sys.argv[3])
    best, evals = QAPAGEA(fName, pobSize, numGens)
    # best, evals = QAPAGEA('../Instances/QAP/test/Cebe.qap.n10.1', 500, 14)
    print(best, evals)
