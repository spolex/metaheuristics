import datetime

import numpy as np

from core.evaluators.BipEvaluator import readBipartInstance
from experiments.Experiment import Experiment
from main.BIP.search.advance.BIPProblemVNS import BIPProblemVNS


class BIPExperiment(Experiment):

    def __init__(self, dir):
        """
        Clase creada para ejecutar los algoritmos relacionados con el problema de bipartición del grafo
        :param dir: directorio que contiene los archivos con las instancias para el experimento
        """
        Experiment.__init__(self, dir)
        self.getFiles(dir)

    def search_method(self, *argv):
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
        now = datetime.datetime.now()
        for file in self.files:
            # Se obtienen la instancia BIP
            instance = readBipartInstance(file)
            # Se crea la clase especifica para aplicar enfriamiento estadístico al problema
            n = instance.shape[1]
            solution = np.random.permutation(np.append(np.zeros(n/2, dtype=int),np.ones(n/2,dtype=int)))
            print(self.search_method(solution, n, instance, 100, 10)[1])
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            np.savetxt('../main/Instances/BIP/results/bipresults'+str(now)+".csv", self.search_method(solution, n, instance, 100, 10)[1], delimiter=",")  # x,y,z equal sized 1D arrays

if __name__ == '__main__':
    np.set_printoptions(precision=3)
    experiment = QAPExperiment('../main/Instances/BIP')
    np.set_printoptions(suppress=True)
    #experiment.experiment()
    now = datetime.datetime.now()
    instance = readBipartInstance(experiment.files[0])
    n = instance.shape[1]
    solution = np.random.permutation(np.append(np.zeros(n / 2, dtype=int), np.ones(n / 2, dtype=int)))
    best_sol, best_vals = experiment.search_method(solution, n, instance, 100, 10)
    print(best_sol, best_vals)
    np.savetxt("../main/Instances/BIP/results/"+'bipresults'+str(now)+".csv", np.asarray(best_sol, dtype=int), delimiter=",", comments="# that is comment")
    np.savetxt("../main/Instances/BIP/results/"+'bipresultsvals'+str(now)+".csv", np.asarray(best_vals), delimiter=",", comments="# that is comment")

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

