#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.searches.ea.BipEA import BipEA
import sys

if __name__ == '__main__':
    # fName = sys.argv[1]
    # pobSize= eval(sys.argv[2])
    # genNums = eval(sys.argv[3])
    # best, evals = BipEA(fName, pobSize, genNums)
    best, evals = BipEA('../Instances/BIP/test/Cebe.bip.n10.1', 100, 12, verbose=True)
    print (best, evals)
