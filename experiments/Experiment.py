import time     # tiempo cpu
import abc
from abc import ABCMeta
import logging
import os
import numpy as np
import sys

log = logging.getLogger("Experiments")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class Experiment(object):
    __metaclass__ = ABCMeta

    def __init__(self, dir=None):
        if dir:
            self.dir = dir
            self.files = np.array([])
        else:
            raise ValueError("El directorio con las instancias es requerido")

    @abc.abstractmethod
    def search_method(self):
        """
            Método a utilizar en el experimento

        """

    @abc.abstractmethod
    def experiment(self, *argv):
        """
            Experimento
        """

    def getFiles(self, dir):
        """
        Obtener todos los ficheros del directorio de instancias para el experimento
        """
        for root, dirs, files in os.walk(dir):
            for file in files:
                if os.path.isfile(dir+'/'+file):
                    self.files = np.append(self.files, dir+'/'+file)