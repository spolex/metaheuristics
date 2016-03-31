#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:33:25 2016

@author: Jose Ignacio Sanchez Mendez
"""

def read(file, mode):
    """
    Para la lectura de instancia de problemas combinatorios desde archivos de texto
    """
    hdl = open(file, mode)
    lista = hdl.readlines()
    hdl.close()
    return lista


