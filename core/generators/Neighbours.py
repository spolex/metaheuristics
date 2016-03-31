#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def swap201(perm):
    """swap201  obtiene el sistema de vecinos V(e) intercambiando dos
    posiciones tales que una tenga valor 1 y la otra 0.

    :param perm: solución inicial propuesta.
    :return: sistema de vecinos V(e)

    Pre: perm es la solución a partir de la cuál hay que generar el sistema de
    vecinos.
    Post: Se devuelve el sistema de vecinos V(e).

    """
    if type(perm) != np.ndarray:
        perm = np.asarray(perm)
    n = perm.shape[0]
    n_neighbors = (n/2)**2           # Número de vecinos
    neighbors = np.zeros((n_neighbors,n),dtype=int) # Guardaremos todos los vecinos en neighbors
    ind = 0
    #print(perm)
    for i in range(0,n):
        #print('vuelta',i)
        if(perm[i]==1): #comprueba que la posición actual tiene un uno
            for j in range(0,n):
                if(perm[j]== 0): #si la posición j tiene un cero, swap201
                    neighbors[ind] = perm
                    neighbors[ind,i]=0
                    neighbors[ind,j]=1
                    ind+=1
                    #print('entro en',j)
    #print(ind)
    return neighbors

def swap2(perm):
    """
    Son soluciones vecinas todas aquellas que se generan intercambiando de lugar
    dos posiciones de la permutación. Por ejemplo, la vecindad de x = [1, 2, 3, 4]
    V(e) es:
        {
        [2, 1, 3, 4], [3, 2, 1, 4],
        [4, 2, 3, 1], [1, 3, 2, 4],
        [1, 4, 3, 2], [1, 2, 4, 3]
                                    }
    pre: Se recibe por parámetros una solución propuesta en forma de vector.
    post: Se devuelve el sistema de vecinos V(e).
    """
    n = perm.shape[0]
    n_neighbors =  n*(n-1)/2           # Número de vecinos
    neighbors = np.zeros((n_neighbors,n),dtype=int) # Guardaremos todos los vecinos en neighbors
    ind = 0
    for j in range(n):
        for i in range(j,n):
            if(j!=i):
                  neighbors[ind, :] = perm
                  neighbors[ind, i] = perm[j]
                  neighbors[ind, j] = perm[i]
                  ind = ind + 1
    return neighbors