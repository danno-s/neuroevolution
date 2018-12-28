'''Here we model a snake in the classic snake game.
The snake has an initial length of 3, and can only move in 
cardinal directions (axis aligned).
'''
from pygame import display, draw, Surface
from itertools import combinations

class Snake:
    def __init__(self, body, opacity = 255):
        '''Initializes a snake.

        The given body must be an instance of deque, for optimized access for 
        queue functionality.

        The head of the snake is the rightmost element of the body.
        '''
        self.length = 3
        self.body = body
        self.last_move = [1, 0]
        self.next_move = [1, 0]
        self.ate = False
        self.opacity = opacity

    def eat_fruit(self):
        '''Called in the game after moving the snake, affects the next move
        '''
        self.ate = True
    
    def move(self):
        '''Called in the game at the start of a "turn", to move the snake
        '''
        next_head = [
            self.body[-1][0] + self.next_move[0],
            self.body[-1][1] + self.next_move[1]
        ]

        self.body.append(next_head)

        if not self.ate:
            # If the snake didn't eat the previous turn, the delete the tailmost segment.
            self.body.popleft()
        else:
            self.ate = False

        self.last_move = self.next_move

    def turn(self, direction):
        '''Moves in the given direction the next turn, if the snake isn't going opposite that direction
        '''
        # If both move in the same axis, then we just return
        if direction[0] != 0 and self.last_move[0] != 0:
            return

        if direction[1] != 0 and self.last_move[1] != 0:
            return
        
        self.next_move = direction

    def crashed(self):
        '''Checks if the snake crashed into one of its body segments.
        '''
        for first, second in combinations(self.body, 2):
            if first == second:
                return True
        return False

    def to_list(self, cells, height):
        '''Writes the position of the snake to a given list
        '''
        for x, y in self.body:
            cells[x * height + y] = -1

    def draw(self, width, height):
        '''Draws the snake using pygame
        '''
        
        screen = display.get_surface()

        fruit_width = screen.get_width() / width
        fruit_height = screen.get_height() / height

        delta_x = fruit_width * 0.05
        delta_y = fruit_height * 0.05
        
        for x, y in self.body:
            s = Surface((fruit_width - delta_x, fruit_height - delta_y))
            s.set_alpha(self.opacity)
            s.fill((255, 255, 255))
            
            screen.blit(s, (x * fruit_width + delta_x, y * fruit_height + delta_y))
