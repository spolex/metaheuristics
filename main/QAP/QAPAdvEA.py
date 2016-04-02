from core.searches.ea.QAPEA import QAPEA

if __name__ == '__main__':
    # fName = sys.argv[1]
    # pobSize= eval(sys.argv[2])
    # numGens = eval(sys.argv[3])
    # best, evals = QAPEA(fName, pobSize, numGens)
    best, evals = QAPEA('../Instances/QAP/Cebe.qap.n30.1', 3000, 10)
    print (best, evals)