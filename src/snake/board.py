'''This represents a board in the snake game.
It's responsibilities are creating new fruits when the previous one is eaten,
and recognizing when the snake's head is out of bounds.
'''
from random import randint
from pygame import draw, display, Surface

class Board:
    def __init__(self, dimensions, opacity = 255):
        self.width, self.height = dimensions

        self.opacity = opacity
        
        self.generate_fruit()

    def generate_fruit(self):
        '''Moves the fruit to a new position, deleting the previous one
        '''
        x_pos = randint(0, self.width - 1)
        y_pos = randint(0, self.height - 1)

        self.fruit = [x_pos, y_pos]

    def inbounds(self, snake):
        snake_head = snake.body[-1]
        return not (snake_head[0] < 0 or 
                    snake_head[0] >= self.width or
                    snake_head[1] < 0 or 
                    snake_head[1] >= self.height)

    def to_list(self, cells):
        cells[self.fruit[0] * self.height + self.fruit[1]] = 1

    def draw(self):
        '''Draws the board's tiles using pygame.
        The only thing actually drawn is the fruit.
        '''
        screen = display.get_surface()

        fruit_width = screen.get_width() / self.width
        fruit_height = screen.get_height() / self.height

        delta_x = fruit_width * 0.05
        delta_y = fruit_height * 0.05

        
        s = Surface((fruit_width - delta_x, fruit_height - delta_y))
        s.set_alpha(self.opacity)
        s.fill((255, 0, 0))
        
        screen.blit(s, (self.fruit[0] * fruit_width + delta_x, self.fruit[1] * fruit_height + delta_y))
