import random

def mut_unbalance(individual):
    """Muta un individuo de elementos binarios hasta lograr el mismo número de unos y ceros.

    :param individual: Individuo a mutar
    :returns: Una tuple con un individual.

    """

    size = len(individual)
    suma = sum(individual)

    while suma > size/2:
        i = random.randint(0, size)
        individual[i] = 0
        suma = sum(individual)

    while suma < size/2:
        i = random.randint(0, size)
        individual[i] = 1
        suma = sum(individual)

    return individual,