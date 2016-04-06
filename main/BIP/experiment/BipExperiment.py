import numpy as np

from core.utils.ioutils import date_formatter, save
from core.searches.ea.BipEA import BipEA
from core.evaluators.BipEvaluator import readBipartInstance
from experiments.Experiment import Experiment
from main.BIP.BIPProblemVNS import BIPProblemVNS
from main.BIP.BipAdvLocalSearch import BipAdvLocalSearch
from pandas import DataFrame
import numpy as np
import os
import logging
import sys
import time

log = logging.getLogger("BIPExperiments")
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class BIPExperiment(Experiment):
    def __init__(self, experiments_dir, date_format='%d-%m-%Y', verbose=False):
        """
        Clase creada para ejecutar los algoritmos relacionados con el problema de bipartición del grafo
        :param dir: directorio que contiene los archivos con las instancias para el experimento
        """
        Experiment.__init__(self, experiments_dir)
        self.getFiles(experiments_dir)
        self.results = DataFrame(
            columns=['time', 'max', 'min', 'median', 'max_evals', 'gen_k', 'iter', 'algorithm', 'date', 'file'])
        self.today = time.strftime(date_format)
        self.verbose = verbose
        if verbose:
            log.setLevel(logging.DEBUG)

    def ea_search_method(self, *argv):
        """
        Implementa la búsqueda local usando deap, AG
        BipEA('../Instances/BIP/test/Cebe.bip.n10.1', 100, 12, verbose=True)
        """
        return BipEA(argv[0], argv[1], argv[2], verbose=self.verbose)

    def search_method(self, *argv):
        """
        Implementa la busqueda local para el experimento
        solution, n, instance, max_evals, nrep (& k)
        """
        bipVNS = BIPProblemVNS(argv[0], argv[1], argv[2], argv[3], argv[4])
        return bipVNS.basic_vns()

    def sa_search_method(self, *argv):
        """
        Implementa la busqueda local para el experimento
        solution, n, instance, max_evals, nrep (& k) usando SA
        bestsol, bestvals = BipAdvLocalSearch('../Instances/BIP/test/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0],5000,100)
        """
        return BipAdvLocalSearch(argv[0], argv[1], argv[2], argv[3])

    @staticmethod
    def initialize(count, genetic, max_evals, sa, tmp, vns):
        log.info("Inicializando la persistencia...")
        s_path = os.path.join(tmp, vns, str(count), str(2 ** max_evals))
        ea_path = os.path.join(tmp, genetic, str(count), str(2 ** max_evals))
        sa_path = os.path.join(tmp, sa, str(count), str(2 ** max_evals))
        if not os.path.exists(s_path):
            os.makedirs(s_path)
        if not os.path.exists(ea_path):
            os.makedirs(ea_path)
        if not os.path.exists(sa_path):
            os.makedirs(sa_path)

        return ea_path, s_path, sa_path

    def wxExperiment(self, max_evals=7, gen_k=15, to_files=True, types=['VNS', 'SA', 'AG']):
        """
        solution, maxevals, nrep
        """

        # Se inicializan los nombres de los directorios para la persistencia
        tmp = self.today + '_results'
        frame = os.path.join(tmp, 'Final')
        if not os.path.exists(frame):
            os.makedirs(frame)
        vns = 'VNS'
        genetic = 'AG'
        sa = 'SA'

        log.info("BIP - Iniciando el experimento")
        count = 0  # index para data frame
        for index in range(10):

            log.info("Iteración {}".format(index))

            for file in self.files:
                # Si el parámetro indica guardar todos los resultados n archivos
                log.debug("Recorriendo los archivos de instancias")
                if to_files:
                    # Initialize paths
                    ea_path, s_path, sa_path = self.initialize(index, genetic, max_evals, sa, tmp, vns)

                if 'VNS' in types:
                    log.info("Iteración {} VNS".format(index))
                    start_time = time.time()
                    # Se obtienen la instancia BIP
                    instance = readBipartInstance(file)
                    n = instance.shape[1]
                    solution = np.random.permutation(np.append(np.zeros(n / 2, dtype=int), np.ones(n / 2, dtype=int)))
                    best_sol, best_vals = self.search_method(solution, n, instance, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time
                    log.info("Iteración {} VNS".format(index))

                    # Persistencia de las estadísticas para el posterior análisis
                    self.results.loc[count] = ([elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                                max_evals, gen_k, index, vns, self.today, file])
                    log.info(self.results.loc[count])
                    count += 1
                    if to_files:
                        save(best_sol, best_vals, s_path, fNames=['/vns_bipresultsol_', '/vns_bipresultsvals_'])

                if 'AG' in types:
                    log.info("Iteración {} AG".format(index))
                    start_time = time.time()
                    best_sol, best_vals = self.ea_search_method(file, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time

                    # persistencia de los resultados
                    self.results.loc[count] = ([elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                                max_evals, gen_k, index, genetic, self.today, file])
                    log.info(self.results.loc[count])
                    count += 1
                    if to_files:
                        save(best_sol, best_vals, ea_path, fNames=['/vns_bipresultsol_', '/vns_bipresultsvals_'])

                if 'SA' in types:
                    log.info("Iteración {} SA".format(index))
                    start_time = time.time()
                    best_sol, best_vals = self.sa_search_method(file, solution, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time

                    # persistencia de los resultados
                    self.results.loc[count] = [elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                               max_evals, gen_k, index, sa, self.today, file]
                    log.info(self.results.loc[count])
                    count += 1
                    if to_files:
                        save(best_sol, best_vals, sa_path, fNames=['/vns_bipresultsol_', '/vns_bipresultsvals_'])

        # Se guardan los estadisticos en un archivo
        self.results.to_csv(os.path.join(frame, 'frame' + date_formatter() + '.csv'), encoding='utf-8', na_rep=True,
                            index=False, sep=';')
        log.info("BIP - Fin del experimento")

    def experiment(self, from_evals=9, to_evals=16, gen_k=15, to_files=True, types=['VNS', 'SA', 'AG']):
        """

        solution, maxevals, nrep

        """

        # Se inicializan los nombres de los directorios para la persistencia
        tmp = self.today+'_results_bip'
        frame = os.path.join(tmp, 'Final')
        if not os.path.exists(frame):
            os.makedirs(frame)
        vns = 'VNS'
        genetic = 'AG'
        sa = 'SA'

        # Se inicializan las variables de control
        index = 0
        iter = 0

        log.info("Iniciando el experimento")
        for max_evals in range(from_evals, to_evals):

            iter += 1
            log.info("Iteración {}".format(iter))
            count = 1
            log.debug("Grupo de instancias {}".format(count))

            for file in self.files:
                # Si el parámetro indica guardar todos los resultados n archivos
                log.debug("Recorriendo los archivos de instancias")
                if to_files:
                    # Initialize paths
                    ea_path, s_path, sa_path = self.initialize(count, genetic, max_evals, sa, tmp, vns)

                if 'VNS' in types:
                    log.info("Iteración {} VNS".format(iter))
                    start_time = time.time()
                    # Se obtienen la instancia BIP
                    instance = readBipartInstance(file)
                    n = instance.shape[1]
                    solution = np.random.permutation(np.append(np.zeros(n / 2, dtype=int), np.ones(n / 2, dtype=int)))
                    best_sol, best_vals = self.search_method(solution, n, instance, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time
                    log.info("Iteración {} VNS".format(iter))

                    # Persistencia de las estadísticas para el posterior análisis
                    self.results.loc[index] = ([elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                                max_evals, gen_k, iter, vns, self.today])
                    log.info(self.results.loc[index])
                    index += 1
                    if to_files:
                        save(best_sol, best_vals, s_path, fNames=['/sa_bipresultsol_','/sa_bipresultsvals_'])

                if 'AG' in types:
                    log.info("Iteración {} AG".format(iter))
                    start_time = time.time()
                    best_sol, best_vals = self.ea_search_method(file, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time

                    # persistencia de los resultados
                    self.results.loc[index] = ([elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                                max_evals, gen_k, iter, genetic, self.today])
                    log.info(self.results.loc[index])
                    index += 1
                    if to_files:
                        save(best_sol, best_vals, ea_path, fNames=['/sa_bipresultsol_','/sa_bipresultsvals_'])

                if 'SA' in types:
                    log.info("Iteración {} SA".format(iter))
                    start_time = time.time()
                    best_sol, best_vals = self.sa_search_method(file, solution, 2 ** max_evals, gen_k)
                    elapsed = time.time() - start_time

                    # persistencia de los resultados
                    self.results.loc[index] = [elapsed, np.max(best_vals), np.min(best_vals), np.mean(best_vals),
                                               max_evals, gen_k, iter, sa, self.today]
                    log.info(self.results.loc[index])
                    index += 1
                    if to_files:
                        save(best_sol, best_vals, sa_path, fNames=['/sa_bipresultsol_','/sa_bipresultsvals_'])

                count += 1

        # Se guardan los estadisticos en un archivo
        self.results.to_csv(os.path.join(frame, 'frame-bip-' + date_formatter() + '.csv'), encoding='utf-8', na_rep=True,
                            index=False, sep=';')
        log.info("Fin del experimento")

if __name__ == '__main__':
    files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Instances/BIP'))
    experiment = BIPExperiment(files_path, verbose=False)
    # experiment.experiment(8, 16, 10, to_files=False, types=['AG'])
    # experiment.experiment(7, 15, 10, to_files=True)
    experiment.wxExperiment()