import numpy as np
from core.utils.ioutils import date_formatter
from core.evaluators.BipEvaluator import readBipartInstance
from experiments.Experiment import Experiment
from main.BIP.BIPProblemVNS import BIPProblemVNS
import os
import logging
import sys

log = logging.getLogger("Experiments")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class BIPExperiment(Experiment):

    def __init__(self, dir):
        """
        Clase creada para ejecutar los algoritmos relacionados con el problema de bipartición del grafo
        :param dir: directorio que contiene los archivos con las instancias para el experimento
        """
        Experiment.__init__(self, dir)
        self.getFiles(dir)

    def ea_search_method(self):
        super().ea_search_method()

    def b_search_method(self, *argv):
        """
        Implementa la busqueda local para el experimento
        solution, n, instance, max_evals, nrep (& k)
        """
        bipVNS = BIPProblemVNS(argv[0], argv[1], argv[2], argv[3], argv[4])
        return bipVNS.basic_vns()

    def experiment(self):
        """
        solution, maxevals, nrep
        """
        count = 1
        for file in self.files:
            # Se obtienen la instancia BIP
            instance = readBipartInstance(file)
            # Se crea la clase especifica para aplicar enfriamiento estadístico al problema
            n = instance.shape[1]
            solution = np.random.permutation(np.append(np.zeros(n/2, dtype=int), np.ones(n/2,dtype=int)))
            best_sol, best_vals = self.b_search_method(solution, n, instance, 100, 10)
            tmp = '_results'
            path =  os.path.join(tmp, str(count))
            if not os.path.exists(path):
                os.makedirs(path)
            np.savetxt(path+'/_bipresults'+date_formatter()+'.csv', np.asarray(best_sol, dtype=int), delimiter=",", comments="# that is comment")
            np.savetxt(path+'/_bipresultsvals'+date_formatter()+'.csv', np.asarray(best_vals), delimiter=",", comments="# that is comment")
            count+=1

if __name__ == '__main__':
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Instances/BIP'))
    experiment = BIPExperiment(dir)
    experiment.experiment()

