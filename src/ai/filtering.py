from random import random, choice

def probabilistic_filter(range):
    '''Retorna una nueva funcion de filtro de población, donde un elemento de fitness f
    tiene f - range[0] / range[1] - range[0] probabilidad de no ser eliminado.
    ----------
    Parametros:
        range: array-like de 2 elementos, donde range[0] < range[1]

    '''
    def filter_population(self):
        to_remove = []
        for individual, fitness in self.individual_fitness.items():
            if random() > fitness:
                to_remove.append(individual)
        for individual in to_remove:
            self.individuals.remove(individual)
            self.individual_fitness.pop(individual)

    return filter_population

def fittest_quarter(self):
    '''Sólo guarda el cuarto de mayor fitness de la población
    '''
    sorted_individuals = sorted(self.individual_fitness.items(), key=lambda kv: kv[1])

    self.individual_fitness.clear()
    self.individuals.clear()

    for individual, _ in sorted_individuals[int(-len(sorted_individuals) / 4):]:
        self.individuals.append(individual)
    
def tournament_filtering(k, n):
    '''Corre n torneos de k individuos, sólo guardando los individuos que ganaron
    ----------
    Parámetros:
        n: número de torneos
        k: número de individuos por torneo
    '''
    def tournament(self):
        new_population = []
        for _ in range(n):
            best = None
            for _ in range(k):
                nxt = choice(self.individuals)
                if best == None or self.fitness(best) < self.fitness(nxt):
                    best = nxt
            new_population.append(best)
        self.individuals = new_population
        self.individual_fitness.clear()

    return tournament