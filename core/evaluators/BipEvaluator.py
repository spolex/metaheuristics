#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:27:33 2016

@author: Jose Ignacio Sanchez Mendez
"""
import sys
import numpy as np
from core.utils import ioutils as u


#Refactor de la función Read_Bipart_Instance
def readBipartInstance(fileName):    
     milista =u.read(fileName, 'r')
     n = eval(milista[0])
     pAristas = np.zeros((n,n))      
     for i in range(n):
       for j,val in enumerate(milista[i+1].split()):     
         pAristas[i,j]=eval(val)         
     return pAristas
     
def calcBipartCost(pAristas, n, sol):
    # Peso de las aristas entre partes del grafo  
    fval = 0                 
    for i in range(n-1):
     for j in range(i+1, n):
       if sol[i] == 1-sol[j]:      # Si estan en partes diferentes
          fval = fval+pAristas[i,j] 
    return fval
 
def BipEvaluator(fileName,sol):
 pAristas = readBipartInstance(fileName) 
# Número de nodos
 n = pAristas.shape[0] 
 
# Comprobación del número de nodos del grafo
 if n % 2!=0:
     exit("EL número de nodos de la instancia debe ser par")

#Nodos en una de las parte, solución popuesta  
 balanceado=np.sum(sol)
 factible=(balanceado ==(n/2)) 
# Comprobación del balanceo de la solución
 if not factible:
     exit("La solución propuesta no es factible")
     
#Cálculo de la función         
 return calcBipartCost(pAristas, n, sol)    
    
if __name__ == '__main__':
    fName = sys.argv[1]    
    sol = eval(sys.argv[2])  
    balanceado = sum(sol) == len(sol)/2 
    if not balanceado:
     exit("La solución propuesta no es balanceada")
    fval=BipEvaluator(fName, sol)  
    print(fval)
    


