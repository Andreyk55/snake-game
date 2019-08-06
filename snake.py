# Snake game

"""
This is not the best design for this game.
Documentation here is minimal.
"""

import pygame
import random

# The snake:
class Player:

    def __init__(self, x_start, y_start, width, height, speed):
        """
        x_start, y_start - Start position of snake.
        width, height - Define the snake dimensions.
                        IMPORTANT Note - They should divide the window dimensions and need to be equal.
        speed - Snake speed.
                IMPORTANT Note - This version supports only speed that equals to snake dimensions.
        """
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.height = height
        self.speed = speed
        self.body = [(x_start, y_start)]
        self.direction = 'left'
        self.color = (255, 0, 1) # temporary
        self.apple = self.get_random_apple()
        self.win_collision = False
        self.color = self.get_random_color()

    def move(self, keys):
        head = self.body[0]
        apple = self.apple
        self.move_head(keys, apple)

        if self.check_for_winning():
            self.exit_with_error('won')

        if self.win_collision:
            self.exit_with_error('win_collision')

        if len(self.body) > 1:
            self.move_tail(head)

        self.draw_snake()

        if self.apple == None:
            self.apple = self.get_random_apple()
            self.color = self.get_random_color()

    # long function, should be shorter:
    def move_head(self, keys, apple):
        body = self.body
        (x_head, y_head) = body[0]
        if keys[pygame.K_LEFT] and x_head >= self.speed:
            if self.is_apple_eaten(apple, x_head - self.speed, y_head):
                pass
            else:
                if self.collision_with_snake(x_head - self.speed, y_head):
                     self.exit_with_error('self collision')
                else:
                    body[0] = (x_head - self.speed, y_head)
            self.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and x_head <= App.win_width - self.speed - self.width:
            if self.is_apple_eaten(apple, x_head + self.speed, y_head):
                pass
            else:
                if self.collision_with_snake(x_head + self.speed, y_head):
                     self.exit_with_error('self collision')
                else:
                    body[0] = (x_head + self.speed, y_head)
            self.direction = 'RIGHT'
        elif keys[pygame.K_UP] and y_head >= self.speed:
            if self.is_apple_eaten(apple, x_head, y_head - self.speed):
                pass
            else:
                if self.collision_with_snake(x_head, y_head - self.speed):
                     self.exit_with_error('self collision')
                else:
                  body[0] = (x_head, y_head - self.speed)
            self.direction = 'UP'
        elif keys[pygame.K_DOWN] and y_head <= App.win_height - self.speed - self.height:
            if self.is_apple_eaten(apple, x_head, y_head + self.speed):
                pass
            else:
                if self.collision_with_snake(x_head, y_head + self.speed):
                     self.exit_with_error('self collision')
                else:
                     body[0] = (x_head, y_head + self.speed)
            self.direction = 'DOWN'
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.win_collision = True
        else:
           self.keep_direction(apple)

    # long function, should be shorter.
    # This function moves the snake when no key is pressed:
    def keep_direction(self, apple):
        body = self.body
        (x_head, y_head) = body[0]

        if self.direction == 'LEFT':
            if x_head >= self.speed:
                if self.is_apple_eaten(apple, x_head - self.speed, y_head):
                    pass
                else:
                    if self.collision_with_snake(x_head - self.speed, y_head):
                        self.exit_with_error('self collision')
                    else:
                        body[0] = (x_head - self.speed, y_head)
            else:
                self.win_collision = True
        if self.direction == 'RIGHT':
            if x_head <= App.win_width - self.speed - self.width:
                if self.is_apple_eaten(apple, x_head + self.speed, y_head):
                    pass
                else:
                    if self.collision_with_snake(x_head + self.speed, y_head):
                        self.exit_with_error('self collision')
                    else:
                         body[0] = (x_head + self.speed, y_head)
            else:
                self.win_collision = True
        if self.direction == 'UP':
            if y_head >= self.speed:
                if self.is_apple_eaten(apple, x_head, y_head - self.speed):
                    pass
                else:
                    if self.collision_with_snake(x_head, y_head - self.speed):
                        self.exit_with_error('self collision')
                    else:
                     body[0] = (x_head, y_head - self.speed)
            else:
                self.win_collision = True
        if self.direction == 'DOWN':
            if y_head <= App.win_height - self.speed - self.height:
                if self.is_apple_eaten(apple, x_head, y_head + self.speed):
                    pass
                else:
                    if self.collision_with_snake(x_head, y_head + self.speed):
                        self.exit_with_error('self collision')
                    else:
                       body[0] = (x_head, y_head + self.speed)
            else:
                self.win_collision = True

    def move_tail(self, head):
        body = self.body

        for i in reversed(range(len(body))):
            if i == 0:
                break
            body[i] = body[i-1]

        body[1] = head

    def draw_snake(self):
        App.win.fill((0, 0, 0))
        (r, g, b) = self.color
        for cell in self.body:
            pygame.draw.rect(App.win, (r, g, b), (cell[0], cell[1], self.width, self.height))

        pygame.display.update()

    def remove_apple(self):
        self.apple = None

    def apple_exist(self, apple, x, y):
        if apple.x_pos == x and apple.y_pos == y:
            return True
        return False

    # If an apple is eaten, snake grows:
    def is_apple_eaten(self, apple, x_head, y_head,):
        if self.apple_exist(apple, x_head, y_head):
              self.body.insert(0, ((x_head, y_head)))
              self.remove_apple()
              return True
        return False

    # Apples appear in a random location (one each time - can decide otherwise):
    def get_random_apple(self):
        x_len = App.win_width / self.width
        y_len = App.win_height / self.height
        while True:
            x = App.win_width - self.width - self.width * random.randrange(0, x_len, 1)
            y = App.win_height - self.height - self.height * random.randrange(0, y_len, 1)
            if not (self.collision_with_snake(x, y)):
                while True:
                    r = random.randrange(0, 256, 1)
                    g = random.randrange(0, 256, 1)
                    b = random.randrange(0, 256, 1)
                    if (r, g, b) != self.color:
                        break
                return Apple(x, y, self.width, self.height,(r, g, b))

    # The snake and the apple are in different random colors changing when snake eats an apple:
    def get_random_color(self):
        while True:
            r = random.randrange(0, 256, 1)
            g = random.randrange(0, 256, 1)
            b = random.randrange(0, 256, 1)
            if (r, g, b) != self.apple.color:
                break
        return (r, g, b)

    # Checks if the snake bumps into itself:
    def collision_with_snake(self, x, y):
        for cell in self.body:
            if cell == (x, y):
                return True
        return False

    def exit_with_error(self, error):
            if error == 'won':
                self.print_message('YOU WON')
            else:
                self.print_message('YOU LOST')
            App.run = False

    def print_message(self, message):
        white = (255, 255, 255)
        red = (255, 0, 0)
        X = 400
        Y = 400

        display_surface = pygame.display.set_mode((X, Y))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(message, True, red, white)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)

        while True:
            display_surface.fill(white)
            display_surface.blit(text, textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                pygame.display.update()

    def check_for_winning(self):
        num_of_cells = self.calculate_num_of_cells()
        if len(self.body) == num_of_cells:
            return True
        else:
            return False

    def calculate_num_of_cells(self):
        x_len = App.win_width / self.width
        y_len = App.win_height / self.height
        return x_len * y_len

# The game:
class App:
    # win = game window, can choose different window size:
    win_width = 500
    win_height = 500
    win = None
    run = True

    def __init__(self, player):
            pygame.init()
            self.player = player

    # The main function that runs the game:
    def snake_run(self):
            App.win = pygame.display.set_mode((App.win_width, App.win_height))
            pygame.display.set_caption('Snake game')

            App.run = True
            while App.run:
                pygame.time.delay(100)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        App.run = False

                keys = pygame.key.get_pressed()
                self.player.move(keys)
                self.draw_apple()


            pygame.quit()

    def draw_apple(self):
        apple = self.player.apple
        pygame.draw.rect(App.win, apple.color, (apple.x_pos, apple.y_pos, apple.width, apple.height))
        pygame.display.update()

class Apple:
    def __init__(self, x_pos, y_pos, width, height, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color



# Run the game:
"""
Player(x_start, y_start, width, height, speed):

x_start, y_start - Start position of snake.
width, height - Define the snake dimensions.
                IMPORTANT Note - They should divide the window dimensions and need to be equal.
speed - Snake speed.
        IMPORTANT Note - This version supports only speed that equals to snake dimensions.
"""
player = Player(250, 250, 25, 25, 25)
app = App(player)

app.snake_run()

