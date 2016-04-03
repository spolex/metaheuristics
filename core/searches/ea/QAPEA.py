#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 18:06:03 2016

@author: Jose Ignacio Sanchez Mendez
"""

import numpy as np
from deap import base, creator, tools, algorithms

from core.evaluators import QAPEvaluator as qap
from core.searches.ea.UMDA import UMDA


def naturalSelection(fenotype, n):
    """
    Función que se encarga de la selección natural, es decir aquellos fenotipos
    que no son factibles en el contexto de QAP se les asigna 
    un 0 en la función de evaluación para que no puedan formar parte de la
    evolución genética
    """
    return (list(range(1,n+1)) == sorted(fenotype))

def createMinRace():
    """
    Función que genera los tipos deap necesarios para minimizar objetivo
    """
    # Se crea una clase FitnessMax para la maximización de funciones
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    # Se crea una clase individuo asociada a la clase FitnessMax
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
def evalQAPEA(mDistance, mFlux, sol, n):
    """
    Función de adaptación diseñada para el problema de QAP.
    """
    fVal = 0  #valor
    if(not naturalSelection(sol, n)):
        print("Soy una solución inutil", sol)
        return fVal
    for i in range(n):
        for j in range(n):
            #Sólo se calcula/incrementa para indices distintos 
            fVal = fVal + (mDistance[i,j]*mFlux[sol[i]-1,sol[j]-1] if i!=j else 0)
    return (fVal,)

def QAPEA(fName, pobSize, genNums):
    """
    Función que utiliza el algoritmo UMDA para encontrar un óptimo sobre una instancia
    del problema de asignación cuadrática.
    """
    createMinRace()
    vertices, mDistance, mFlux = qap.Read_QAP_Instance(fName)
    
    n, N = vertices, pobSize
    trunc_par=0.5
    strategy = UMDA(n,N,trunc_par)
    
    toolbox = base.Toolbox()
    toolbox.register("evaluate", evalQAPEA,mDistance, mFlux,n=n)
    #funcion generate UMDA
    toolbox.register("generate", strategy.generate, creator.Individual)
    #funcion update UMDA
    toolbox.register("update", strategy.update)
    
     # Np equality function (operators.eq) between two arrays returns the
    # equality element wise, which raises an exception in the if similar()
    # check of the hall of fame. Using a different equality function like
    # np.array_equal or np.allclose solve this issue.
    hof = tools.HallOfFame(1, similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("max", np.max)


    rdo= algorithms.eaGenerateUpdate(toolbox, ngen=genNums, stats=stats, halloffame=hof,verbose=True)
    evals = [ dic['min'] for dic in rdo[1] ]
    
    return hof[0], sorted(evals, reverse=True)
    
if __name__ == '__main__':
    # fName = sys.argv[1]
    # pobSize= eval(sys.argv[2])
    # numGens = eval(sys.argv[3])
    # best, evals = QAPEA(fName, pobSize, numGens)
    best, evals = QAPEA('../Instances/QAP/test/Cebe.qap.n10.1', 500, 14)
    print (best, evals)
