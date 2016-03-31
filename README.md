# Computación evolutiva

## Packages

Contiene todos los módulos y ficheros que componen el proyecto y son necesarios para el correcto funcionamiento:

```
.
├── core
│   ├── evaluators
│   │   ├── BipEvaluator.py
│   │   └── QAPEvaluator.py
│   ├── generators
│   │   ├── Neighbours.py
│   ├── searches
│   │   ├── ea
│   │   │   ├── BipEA.py
│   │   │   └── UMDA.py
│   │   │   ├── advance
│   │   │   │   ├── Anneal.py
│   │   │   ├── basic
│   │   │   │   ├── BasicLocalSearches.py
│   │   │   │   ├── BasicLocalSearches.pyc
│   └── utils
│       ├── ioutils.py
├── doc
│   ├── build
│   │   └── html
├── main
│   ├── BIP
│   │   ├── BipAdvEA.py
│   │   ├── BipAdvLocalSearch.py
│   │   ├── BipLocalSearch.py
│   ├── Instances
│   │   ├── BIP
│   │   └── QAP
│   └── QAP
│       ├── QAPAdvEA.py
│       ├── QAPAdvLocalSearch.py
│       └── QAPLocalSearch.py
└── README.md

```


### Documentación

* La documentación del api se encuentra bajo el directorio doc/buil/html, el archivo principal _index.html_.
* El informe de la experimentación se encuentra en el directorio //TODO

### Instalación

Instrucciones de ionstalación

### Ejemplos de ejecución
-------------------------

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
(jisanchez003@ikasle.ehu.es)