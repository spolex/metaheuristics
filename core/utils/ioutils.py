#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from numpy import savetxt, asarray


def read(file, mode):
    """
    Para la lectura de instancia de problemas combinatorios desde archivos de texto
    :param file: path del archivo
    :param mode: modo de apertura
    """
    hdl = open(file, mode)
    mylist = hdl.readlines()
    hdl.close()
    return mylist


def date_formatter(formatter='%d%m%Y-%H'):
    """
    Formateo de fechas en strings usando el formato recibido por parámetros
    :param formatter: formato de fechas que se desea aplicar
    :return fecha tipo str con el formato aplicado
    """
    return time.strftime(formatter)


def save(best_sol, best_vals, s_path, fName='file', ext='csv', log=None):
    """
    Persistencia de todos los resultados de cada iteración de un experimentos, sin resumir

    :param best_sol: mejor solucion halladas.
    :param best_vals: mejores valores de la función de coste cada k evaluaciones
    :return void:
    """
    if log:
        log.info("Guardando resultados en archivos: " + ext)
    savetxt(s_path + fName + date_formatter() + '.'+ext, asarray(best_sol, dtype=int), delimiter=",")
    savetxt(s_path + fName + date_formatter() + '.'+ext, asarray(best_vals), delimiter=",")
