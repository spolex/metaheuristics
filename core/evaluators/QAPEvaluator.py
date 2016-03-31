#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 19:25:23 2016

@author: Jose Ignacio Sanchez Mendez

"""
import sys

import numpy as np
from core.utils import ioutils as u


def Read_QAP_Instance(fname):
    
 miLista = u.read(fname, 'r') 
 #número de instalaciones/localizaciones
 vertices = int(miLista[0].split()[0]) 
 
 #Se obtiene la matriz de distancias
 matrizDistancia = np.zeros((vertices,vertices))
 for i in range(vertices):
     for j,val in enumerate(miLista[i+1].split()):   
         matrizDistancia[i,j] = float(val)
 
 #Se obtiene la matriz de flujos
 matrizFlujo = np.zeros((vertices,vertices)) 
 for i in range(vertices):
     for j,val in enumerate(miLista[i+vertices+1].split()):   
         matrizFlujo[i,j] = float(val)         
       
 return vertices, matrizDistancia, matrizFlujo
 
def qapCostEvaluator(mDistance, mFlux, sol, n):
    fVal = 0  #valor  
    for i in range(n):
        for j in range(n):
            #Sólo se calcula/incrementa para indices distintos 
            fVal = fVal + (mDistance[i,j]*mFlux[sol[i]-1,sol[j]-1] if i!=j else 0)
    return fVal
 
def QAPEvaluator(file, perm):    
    
    perm = np.asarray(perm)
    #Se obtienen las matrices de distanci y flujo,
    n, mDist, mFluj = Read_QAP_Instance(file)
    
    if np.sum(perm)!=sum(range(n+1)):
        print('La solución propuesta no es valida, revise que no aparezca ninguna repetición')
        exit()    
    
    if perm.shape[0]!=n:
        print('Error en la dimension de la permutacion')
        exit()
    
    return qapCostEvaluator(mDist,mFluj,perm,n)
    
if __name__ == '__main__':
  fileName = sys.argv[1]
  solucion = eval(sys.argv[2])
  evaluacion = QAPEvaluator(fileName,solucion)
  print(evaluacion)
#  QAPInstance = QAPEvaluator('../Instances/QAP/Cebe.qap.n10.1',[1,2,3,4,5,6,7,8,9,10])
