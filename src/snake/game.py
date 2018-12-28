'''Here, the basic logic of the snake game is implemented.
'''
from collections import deque
from .board import Board
from .snake import Snake

class Game:
    def __init__(self, dimensions, opacity = 255):
        '''Dimensions must be at least 4 by 4
        '''
        self.board = Board(dimensions, opacity = opacity)
        snake_body = deque([[1,1], [2, 1], [3, 1]])
        self.snake = Snake(snake_body, opacity = opacity)
        self.score = 0
        self.turns = 0
        self.over = False

    def play_turn(self):
        '''Executes the snake's movement, checking if it's alive, and if it ate a fruit
        '''
        if self.over:
            return

        self.snake.move()

        if not self.board.inbounds(self.snake) or self.snake.crashed():
            self.over = True

        if self.board.fruit == self.snake.body[-1]:
            self.score += 100
            self.snake.eat_fruit()

        self.turns += 1

    def input(self, direction):
        '''Tells the snake to move in a certain direction next turn
        '''
        self.snake.turn(direction)
    
    def to_list(self):
        '''Returns a list representation of the game state
        '''
        result = [0] * self.board.width * self.board.height
        self.board.to_list(result)
        self.snake.to_list(result, self.board.height)

        return result
        
    def draw(self):
        '''Draws all of the game's elements using pygame
        '''

        self.board.draw()
        self.snake.draw(self.board.width, self.board.height)
