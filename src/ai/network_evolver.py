import random
from network_individual import NetworkIndividual
import filtering
from population import Population
from time import time

if __name__ == "__main__":
    # Definimos las funciones necesarias para el algoritmo genético
    def individual_generator():
        return NetworkIndividual()
    
    def fitness(an_individual):
        return an_individual.score

    population = Population(100, individual_generator, fitness, filtering.fittest_quarter)

    generations = 1
    gen_fitness = []
    gen_change = []
    solution = None

    start = time()
    while True:
        population.compute_fitness()

        # Conseguimos el elemento de mejor fitness
        sorted_individuals = sorted(population.individual_fitness.items(), key=lambda kv: kv[1])

        # Si el fitness es el número de bits de la frase
        if sorted_individuals[-1][1] == 1:
            # La solución es el par asociado a ese fitness
            solution = sorted_individuals[-1][0]


        print("\033[KBest individual fitness: {}".format(sorted_individuals[-1][1]), end="\r")
        if len(gen_fitness) == 0 or gen_fitness[-1] != sorted_individuals[-1][1]:
            gen_fitness.append(sorted_individuals[-1][1])
            gen_change.append(generations)

        if solution:
            break

        generations += 1
        population.filter_population()
        population.reproduce()
