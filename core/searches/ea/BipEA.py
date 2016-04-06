#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jose Ignacio Sanchez Mendez
"""

import logging
import sys
import numpy as np
from deap import base, creator, tools, algorithms
from core.evaluators.BipEvaluator import readBipartInstance
from core.operators.Mutators import mut_unbalance

log = logging.getLogger("BipEA")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def naturalSelection(fenotype):
    """
    Función que se encarga de la selección natural, es decir aquellos fenotipos
    que no son factibles en el contexto de Bipartición del grafo se les asigna 
    un 0 en la función de evaluación para que no puedan formar parte de la
    evolución genética
    """
    return sum(fenotype) == int(len(fenotype)/2)

    
def evalBip(mWeight, n, fenotype):
    """
    Función de adaptación diseñada para el problema de bipartición del grafo.
    pre: recibe por parámetros la matriz de pesos y el fenotipo
    post:
    """
    fval = 0
    if(not naturalSelection(fenotype)):
        log.info("Se están generando soluciones desbalanceadas")
        log.debug(fenotype)
        # return (fval, ) # se penalizan las soluciones desbalanceadas
    log.debug("Soy valido!!!")
    for i in range(n-1):
     for j in range(i+1,n):
       if fenotype[i]==1-fenotype[j]:      # Si estan en partes diferentes  
          fval = fval+mWeight[i,j]
    return fval,


def createMaxRace():
    """
    Función que genera los tipos deap necesarios
    """
    # Se crea una clase FitnessMax para la maximización de funciones
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # Se crea una clase individuo asociada a la clase FitnessMax
    creator.create("Individual", list, fitness=creator.FitnessMax)


def bornBipRandomfenotype(n):
    """
    Función que genera un fenotipo válido (balanceado) 
    """
    sample = np.zeros(n, dtype=int)
    for i in range(int(n/2)):
        sample[i] = 1
    return np.random.permutation(sample)


def buildBipRandomPopulation(size, l, toolbox):  

    toolbox.register("indices", bornBipRandomfenotype, l)    
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    # Definimos la población a partir de los individuos
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    return toolbox.population(n=size)


def BipEA(fName, pobSize, genNums, verbose=False):
    """
    ALgoritmo genético para el problema de Bipartición balanceada del grafo.
    """
    if verbose:
        log.setLevel(logging.DEBUG)
    createMaxRace()
    
     # Heredamos las clases y funciones implementadas como parte de DEAP
    toolbox = base.Toolbox()
    
    # Leemos la instancia del problema de Bipartición del grafo    
    instance = readBipartInstance(fName)
    n = instance.shape[0]
    
    # Obtenemos la población inicial de soluciones factibles de forma aleatoria
    population = buildBipRandomPopulation(pobSize, n, toolbox)
    
    # Asociamos como función de aptitud la función evalBip
    toolbox.register("evaluate", evalBip, instance, n)
    # Nuestro operador de cruzamiento será
    toolbox.register("mate", tools.cxUniform, indpb=1/((pobSize**0.9318)*(n**0.4535)))
    # El operador de mutación cambiará 1-->0  y 0-->1
    # hasta balancear el individuo cuando un cruce termine en un individuo NO factible
    toolbox.register("mutate", mut_unbalance)
    # de mutación de 1/(lambda**0.9318)*(l**0.4535) recomendada
    # toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1/((pobSize**0.9318)*(n**0.4535)))
    # Usaremos selección por torneo con un parámetro de torneo = 3
    toolbox.register("select", tools.selTournament, tournsize=3)

    # estadísticos incluidos
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #algoritmo en cada generación
    stats.register("max", np.max)
    
    #Para obtener el mejor individuo que nunca ha existido en la población, deacuerdo a la función de evaluación
    hof = tools.HallOfFame(1, similar=np.array_equal)
    
    # Probabilidad de cruzamiento 0.8
    # Probabilidad de aplicar el operador de mutación 1.0, para evitar soluciones desbalanceadas
    rdo = algorithms.eaSimple(population, toolbox, stats=stats, cxpb=0.8, mutpb=1.0, ngen=genNums, halloffame=hof, verbose=True)
    
    evals = [dic['max'] for dic in rdo[1]]
    for i in range(1, len(evals)):
        if evals[i] < evals[i-1]:
            evals[i] = evals[i-1]
    return hof[0], evals
    

if __name__ == '__main__':
    fName = sys.argv[1]    
    pobSize= eval(sys.argv[2]) 
    genNums = eval(sys.argv[3]) 
    best, evals = BipEA(fName, pobSize, genNums)
#    best, evals = BipEA('../../Instances/BIPART/Cebe.bip.n10.1', 100, 12)
    print(best, evals)

#EJEMPLO DE LLAMADA AL OPTIMIZADOR EN PYTHON:
#best sol, evals = BipEA(' ../Instances/BIP ART /Cebe.bip.n10.1', 100, 12)
#Este programa ejecutar ́ıa el algoritmo poblacional con una poblaci ́on de tamaño 
#100 por 12 generaciones.
