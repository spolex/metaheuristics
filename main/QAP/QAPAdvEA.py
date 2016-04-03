from core.searches.ea.QAPAGEA import QAPAGEA
import numpy


def QAPAdvEA(fName, pob_size, num_gens):
    return QAPAGEA(fName, pob_size, num_gens)

if __name__ == '__main__':
    # fName = sys.argv[1]
    # pobSize= eval(sys.argv[2])
    # numGens = eval(sys.argv[3])
    # best, evals = QAPEA(fName, pobSize, numGens)
    best, evals = QAPAdvEA('../Instances/QAP/test/Cebe.qap.n10.1', 3000, 10)
    print(best, evals)