from main.BIP.experiment.BipExperiment import BIPExperiment
from main.QAP.experiments.QAPExperiments import QAPExperiment
import os

if __name__ == '__main__':
    bip_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Instances/BIP'))
    bipexperiment = BIPExperiment(bip_files_path, verbose=False)
    bipexperiment.wxEperiment()
    qap_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Instances/QAP'))
    qapexperiment = QAPExperiment(qap_files_path, verbose=False)
    qapexperiment.wxEperiment()