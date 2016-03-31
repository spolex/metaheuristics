#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

from core.evaluators.BipEvaluator import calcBipartCost
from core.generators.Neighbours import swap201, swap2
from core.evaluators.QAPEvaluator import qapCostEvaluator


def BIPLocalSearchSwap201(pAristas, initSolution):
    """
    Implementación de la búsqueda local básica
    Elegir e ∈ V (e0 ) tal que f (e) < f (e0 )
        Asignar e a e0
    hasta f (e) ≥ f (e0 ) ∀ e ∈ V (e0 )
    e0 es la aproximación a la solución óptima
    Pre:El problema que resuelve es de maximización.
    Post:Se devuelve la mejor solución y su evalución usando la función de coste
    """
    n = pAristas.shape[1]
    best_val = calcBipartCost(pAristas,n,initSolution)              # Mejor valor
    best_sol = initSolution                                             # Mejor solución
    improve = True
    while improve:
        neighbors = swap201(np.asarray(best_sol))            # Todos los vecinos
        n_neighbors = neighbors.shape[0]
        best_val_among_neighbors = best_val
        for i in range(n_neighbors):
            sol = neighbors[i, :]
            fval = calcBipartCost(pAristas, n, sol)    # Se evalua la función
            if fval > best_val_among_neighbors:             # Si es mejor que el mejor valor entre los vecinos hasta el momento (max)
                best_val_among_neighbors = fval           # se actualiza el mejor valor y solución
                best_sol_among_neighbors = sol
        improve = (best_val_among_neighbors>best_val) #  Se determina si ha habido mejora con respecto al ciclo anterior
        if improve:
            best_val = best_val_among_neighbors           # Se actualiza el mejor valor y la mejor solución
            best_sol = best_sol_among_neighbors
            #print(best_val,best_sol)
    return best_val, best_sol

def QAPLocalSearchSwap2(vertices, mDistance, mFlux, initSolution):
    """
     El algoritmo de búsqueda local debe recorrer todo el vecindario,
    eligiendo a cada paso la mejor solución vecina para un problema de
    asignación cuadrática.
    Pre: El problema que resuelve es de minimización.
    Post:Devuelve la mejor solución y el su evalución usando la función de coste
    """
    best_val = qapCostEvaluator(mDistance, mFlux, initSolution, vertices)              # Mejor valor
    best_sol = initSolution                                             # Mejor solución
    improve = True
    while improve:
        neighbors = swap2(np.asarray(best_sol))            # Todos los vecinos
        n_neighbors = neighbors.shape[0]
        best_val_among_neighbors = best_val
        for i in range(n_neighbors):
            sol = neighbors[i,:]
            fval = qapCostEvaluator(mDistance, mFlux,sol,vertices)    # Se evalua la función
            if fval < best_val_among_neighbors:             # Si es mejor que el mejor valor entre los vecinos hasta el momento (min)
                best_val_among_neighbors = fval           # se actualiza el mejor valor y solución
                best_sol_among_neighbors = sol
        improve = (best_val_among_neighbors<best_val) #  Se determina si ha habido mejora con respecto al ciclo anterior
        if improve:
            best_val = best_val_among_neighbors           # Se actualiza el mejor valor y la mejor solución
            best_sol = best_sol_among_neighbors
            #print(best_val,best_sol)
    return best_val, best_sol