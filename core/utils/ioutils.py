#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time


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


def date_formatter(formatter='%Y%m%d-%H'):
    """
    Formateo de fechas en strings usando el formato recibido por parámetros
    """
    return time.strftime(formatter)
