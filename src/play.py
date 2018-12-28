import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from snake.game import Game

pygame.init()

BACKGROUND = (0, 0, 0)

UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

size = (800, 600)

screen = pygame.display.set_mode(size)

game = Game([20, 15])

clock = pygame.time.Clock()

turn_length = 10

turn_progress = 0

while not game.over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                game.input(UP)
            elif event.key == K_DOWN:
                game.input(DOWN)
            elif event.key == K_RIGHT:
                game.input(RIGHT)
            elif event.key == K_LEFT:
                game.input(LEFT)

    screen.fill(BACKGROUND)

    turn_progress += 1

    if turn_progress >= turn_length:
        turn_progress = 0
        game.play_turn()

        if game.snake.ate:
            game.board.generate_fruit()

    game.draw()

    pygame.display.flip()


    # Set a fixed 60 FPS
    clock.tick(60)

pygame.quit()