# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 20:14:15 2016

@author: Jose Ignacio Sánchez Méndez
"""
from core.evaluators.QAPEvaluator import Read_QAP_Instance
from core.searches.local.basic.BasicLocalSearches import QAPLocalSearchSwap2


def QAPLocalSearch(fName, solution):
    vertices, matrizDistancia, matrizFlujo = Read_QAP_Instance(fName)
    return QAPLocalSearchSwap2(vertices, matrizDistancia, matrizFlujo, solution)

if __name__ == '__main__':
    # fName = sys.argv[1]
    # sol = eval(sys.argv[2])
    # bestsol, bestval =  QAPLocalSearch(fName , sol)
    bestsol, bestval = QAPLocalSearch('../Instances/QAP/test/Cebe.qap.n10.1', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(bestsol, bestval)