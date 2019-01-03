import pygame
from snake.game import Game
from ai.filtering import *
from ai.population import Population
from ai.network_individual import NetworkIndividual
from math import exp

pygame.font.init()
pygame.init()

pygame.event.set_blocked(None)
pygame.event.set_allowed(pygame.QUIT)

BACKGROUND = (0, 0, 0)

UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

WIDTH = 20
HEIGHT = 15

N = 500

size = (800, 600)
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Times New Roman', 30)

games = [Game([WIDTH, HEIGHT], opacity=51) for _ in range(N)]

clock = pygame.time.Clock()

turn_length = 1
turn_progress = 0

done = False


'''AI variables
'''

def individual_generator():
    return NetworkIndividual(WIDTH * HEIGHT)

def fitness(an_individual):
    return an_individual.score * exp(-an_individual.turns)

population = Population(N, individual_generator, fitness, fittest_quarter)

generations = 0

# For all the time we want
while not done:
    # Before starting we make a new set of games.
    games = [Game([WIDTH, HEIGHT], opacity=51) for _ in range(N)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Run the simulations of each network (fitness evaluation)
    # While at least one game isn't finished
    while any(not game.over for game in games) and not done:
        if max(game.turns for game in games) > 500:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # We emulate input using the neural networks (and only on the first)
        # frame of each turn, since it's useless to repeat the processing for all frames
        if turn_progress == 0:
            for individual, game in zip(population.individuals, games):
                # First, we make a very long list with every single cell, and its content
                # For this, an empty cell is a 0, a cell with the snake is a -1, and a cell with a fruit is a 1

                # Of course, we skip games that are already lost
                if game.over:
                    continue

                cells = game.to_list()

                result = individual.network.process(cells)

                i = result.index(max(result))

                if i == 0:
                    # Move up
                    game.input(UP)
                elif i == 1:
                    # Move down
                    game.input(DOWN)
                elif i == 2:
                    # Move left
                    game.input(LEFT)
                elif i == 3:
                    # Move right
                    game.input(RIGHT)

        screen.fill(BACKGROUND)

        turn_progress += 1

        if turn_progress >= turn_length:
            turn_progress = 0
            
            for game in filter(lambda game: not game.over, games):
                game.play_turn()

                if game.snake.ate:
                    game.board.generate_fruit()

        for game in filter(lambda game: not game.over, games):
            game.draw()

        # Render score
        text_surface = font.render("Generation: {}  |  Turn: {}  |  Max Score: {}  |  Avg Score: {}".format(generations, max(game.turns for game in games), max(game.score for game in games), sum(game.score for game in games) / N), False, (255, 255, 255))

        screen.blit(text_surface, (0, 0))

        pygame.display.flip()
    
    # At the end we store the values of the game in the individual
    for individual, game in zip(population.individuals, games):
        individual.score = game.score
        individual.turns = game.turns

    # Then we 'compute' the fitness
    population.compute_fitness()
    
    # And filter it, and reproduce it
    generations += 1
    population.filter_population()
    population.reproduce()

pygame.quit()