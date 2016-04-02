# Computación evolutiva

## Packages

Contiene todos los módulos agrupados en funcionlidad:

1. **core** Implementa las funcionalidades transversales a todo el API
    1. **evaluators** funciones de adaptación
    2. **generators** generadores de vecindarios/poblaciones
    3. **searches** algoritmos de búsqueda 
        1. **ea** algoritmos genéticos
        2. **local** 
            1. **advance** búsqueda local con estrategias de 'escape': _BVNS_, SA...
            2. **basic**
    4. utils
2. experiments
3. main
    1. BIP problema de optimización combinatoria: bipartición balanceada del grafo
    2. QAP problema de optimización combinatoria: asignación cuadrática
    3. Instances instancias de test
```


### Documentación

* La documentación del framework puede ser consultada  en [este enlace](https://rawgit.com/spolex/metaheuristics/master/doc/build/html/index.html)
 

### Instalación

Instrucciones de instalación

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

- Iñigo Sánchez Méndez (spolex)
(spolexdroid@gmail.com)