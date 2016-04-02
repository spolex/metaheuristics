import numpy as np

from core.utils.ioutils import date_formatter
from core.searches.ea.BipEA import BipEA
from core.evaluators.BipEvaluator import readBipartInstance
from experiments.Experiment import Experiment
from main.BIP.BIPProblemVNS import BIPProblemVNS
import os
import logging
import sys
import time

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

    def ea_search_method(self, *argv):
        """
        Implementa la búsqueda local usando deap, AG
        BipEA('../Instances/BIP/test/Cebe.bip.n10.1', 100, 12, verbose=True)
        """
        return BipEA(argv[0], argv[1], argv[2], verbose=True)

    def search_method(self, *argv):
        """
        Implementa la busqueda local para el experimento
        solution, n, instance, max_evals, nrep (& k)
        """
        bipVNS = BIPProblemVNS(argv[0], argv[1], argv[2], argv[3], argv[4])
        return bipVNS.basic_vns()

    def experiment(self,from_evals=9, to_evals= 16, gen_k=15):
        """
        solution, maxevals, nrep
        """

        # Se inicializan los nombres de los directorios para la persistencia
        tmp = '_results'
        search = 'advance_VNS'
        genetic = 'ea'

        for max_evals in range(from_evals,to_evals):
            count = 1
            for file in self.files:

                # Initialize paths
                s_path = os.path.join(tmp, search, str(count), str(2**max_evals))
                ea_path = os.path.join(tmp, genetic, str(count), str(2**max_evals))
                if not os.path.exists(s_path):
                    os.makedirs(s_path)
                if not os.path.exists(ea_path):
                    os.makedirs(ea_path)

                # VNS
                start_time = time.time()
                # Se obtienen la instancia BIP
                instance = readBipartInstance(file)
                # Se crea la clase especifica para aplicar enfriamiento estadístico al problema
                n = instance.shape[1]
                solution = np.random.permutation(np.append(np.zeros(n/2, dtype=int), np.ones(n/2,dtype=int)))
                best_sol, best_vals = self.search_method(solution, n, instance, 2**max_evals, gen_k)
                elapsed = time.time() - start_time

                #Persistencia de los resultados para el posterior análisis
                np.savetxt(s_path+'/vns_bipresults'+date_formatter()+'.csv', np.asarray(best_sol, dtype=int), delimiter=",",
                           comments="# that is comment")
                np.savetxt(s_path+'/vns_bipresultsvals'+date_formatter()+'.csv', np.asarray(best_vals), delimiter=",",
                           comments="# that is comment")
                np.savetxt(s_path+'/vns_cpu'+date_formatter()+'.csv', np.asarray([elapsed]), delimiter=",",
                           comments="# that is comment")

                # Genetic
                start_time = time.time()
                best_sol, best_vals = BipEA(file, 2**max_evals, gen_k, verbose=True)
                elapsed = time.time() - start_time

                # persistencia de los resultados
                np.savetxt(ea_path + '/ea_bipresults' + date_formatter() + '.csv', np.asarray(best_sol, dtype=int),
                           delimiter=",", comments="# that is comment")
                np.savetxt(ea_path + '/ea_bipresultsvals' + date_formatter() + '.csv', np.asarray(best_vals), delimiter=",",
                           comments="# that is comment")
                np.savetxt(ea_path+'/ea_cpu'+date_formatter()+'.csv', np.asarray([elapsed]), delimiter=",",
                           comments="# that is comment")

                count += 1

if __name__ == '__main__':
    dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Instances/BIP'))
    experiment = BIPExperiment(dir)
    experiment.experiment()

