import random

class Population():
    def __init__(self, number_of_individuals, individual_generator, fitness, filter_func):
        '''Crea una nueba población con el número de individuos dados, generados 
        por la función individual_generator.
        ----------
        Parámetros
            number_of_individuals:
                el número de individuos de esta población
            individual_generator:
                función que genera un individuo en la población
            fitness:
                función que recibe un individuo y retorna su fitness
            filter_func:
                función que filtra la población de esta instancia
        '''
        self.n = number_of_individuals
        self.individuals = []
        for _ in range(number_of_individuals):
            self.individuals.append(individual_generator())

        self.fitness = fitness
        self.individual_fitness = {}

        Population.filter_population = filter_func

    def compute_fitness(self):
        '''Calcula el fitness para todos los miembros de la población
        '''
        for individual in self.individuals:
            self.individual_fitness[individual] = self.fitness(individual)

    def reproduce(self):
        '''Rellena la población hasta n, reproduciendo individuos al azar.
        '''
        new_children = []
        while len(self.individuals) + len(new_children) < self.n:
            parentA, parentB = random.choices(self.individuals, k = 2)
            new_children.append(parentA.reproduce(parentB))

        self.individuals.extend(new_children)
