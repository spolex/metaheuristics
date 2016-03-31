from experiments.Experiment import Experiment
from main.BIP.BIPProblemVNS import BIPProblemVNS
from core.evaluators.BipEvaluator import readBipartInstance
import numpy as np
import datetime

class QAPExperiment(Experiment):

    def __init__(self, dir):
        Experiment.__init__(self, dir)
        self.getFiles(dir)

    def search_method(self, *argv):
        """
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
            np.savetxt(file+'bipresults'+str(now), self.search_method(solution, n, instance, 100, 10)[1])  # x,y,z equal sized 1D arrays

if __name__ == '__main__':
    experiment = QAPExperiment('../main/Instances/BIP')
    experiment.experiment()