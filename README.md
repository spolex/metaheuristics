# Computación evolutiva

## Packages

Contiene todos los módulos y ficheros que componen el proyecto y son necesarios para el correcto funcionamiento:

```
..
├── core
│   ├── evaluators
│   │   ├── BipEvaluator.py
│   │   └── QAPEvaluator.py
│   ├── generators
│   │   ├── Neighbours.py
│   ├── searches
│   │   ├── ea
│   │   │   ├── BipEA.py
│   │   │   ├── QAPEA.py
│   │   │   └── UMDA.py
│   │   ├── __init__.py
│   │   ├── local
│   │   │   ├── advance
│   │   │   │   ├── Anneal.py
│   │   │   │   └── VNS.py
│   │   │   ├── basic
│   │   │   │   ├── BasicLocalSearches.py
│   └── utils
│       ├── ioutils.py
├── doc
├── experiments
│   ├── Experiment.py
│   ├── __init__.py
├── __init__.py
├── main
│   ├── BIP
│   │   ├── BipAdvEA.py
│   │   ├── BipAdvLocalSearch.py
│   │   ├── BipExperiment.py
│   │   ├── BipLocalSearch.py
│   │   ├── BIPProblemVNS.py
│   ├── Instances
│   │   ├── BIP
│   │   │   ├── Cebe.bip.n50.1
│   │   │   ├── Cebe.bip.n50.2
│   │   │   ├── Cebe.bip.n50.3
│   │   │   ├── Cebe.bip.n50.4
│   │   │   ├── Cebe.bip.n50.5
│   │   │   ├── Cebe.bip.n80.1
│   │   │   ├── Cebe.bip.n80.2
│   │   │   ├── Cebe.bip.n80.3
│   │   │   ├── Cebe.bip.n80.4
│   │   │   ├── Cebe.bip.n80.5
│   │   │   └── results
│   │   └── QAP
│   │       ├── Cebe.qap.n30.1
│   │       ├── Cebe.qap.n30.2
│   │       ├── Cebe.qap.n30.3
│   │       ├── Cebe.qap.n30.4
│   │       ├── Cebe.qap.n30.5
│   │       ├── Cebe.qap.n50.1
│   │       ├── Cebe.qap.n50.2
│   │       ├── Cebe.qap.n50.3
│   │       ├── Cebe.qap.n50.4
│   │       └── Cebe.qap.n50.5
│   └── QAP
│       ├── QAPAdvEA.py
│       ├── QAPAdvLocalSearch.py
│       ├── QAPLocalSearch.py
│       └── QAPProblemVNS.py
└── README.md

```


### Documentación

* La documentación del framework puede ser consultada  en [este enlace](https://cdn.rawgit.com/spolex/metaheuristics/master/doc/build/html/index.html)
 

### Instalación

Instrucciones de ionstalación

### Ejemplos de ejecución

1. BipLocalSearch

    ```python    
    BipLocalSearch('../../Instances/BIPART/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0])    
    ```
1. BipAdvLocalSearch

    ```python
    BipAdvLocalSearch('../../Instances/BIPART/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0],100,10)        
    ```
1. BipAdvEA 

    ```python
    BipAdvEA('../../Instances/BIPART/Cebe.bip.n10.1', [1,1,1,1,1,0,0,0,0,0],100,10)        
    ```
1. QAPLocalSearch

    ```python    
    QAPLocalSearch('../../Instances/QAP/Cebe.qap.n10.1', [1,2,3,4,5,6,7,8,9,10])    
    ```
1. QAPAdvLocalSearch

    ```python    
    QAPAdvLocalSearch('../../Instances/QAP/Cebe.qap.n10.1', [1,2,3,4,5,6,7,8,9,10],100,10)    
    ```
1. QAPAdvEA

    ```python    
    QAPAdvEA('../../Instances/QAP/Cebe.qap.n10.1', [1,2,3,4,5,6,7,8,9,10],100,10)    
    ```
### Authors
-----------

- Jose Ignacio Sánchez Méndez (spolex)
(spolexdroid@gmail.com)