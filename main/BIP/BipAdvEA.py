#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.searches.ea.BipEA import BipEA, np

if __name__ == '__main__':
    # fName = sys.argv[1]
    # pobSize= eval(sys.argv[2])
    # genNums = eval(sys.argv[3])
    # best, evals = BipEA(fName, pobSize, genNums)
    np.set_printoptions(suppress=True)
    best, evals = BipEA('../Instances/BIP/test/Cebe.bip.n10.1', 10, 10, verbose=True)
    print (best, evals)
