import pygame
import random
import time
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (45, 42, 46)


class Apple:
    def __init__(self, parent_screen, snake):
        self.image = pygame.image.load("resources/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (33, SIZE))
        self.parent_screen = parent_screen
        self.snake = snake
        self.x = SIZE * 3
        self.y = SIZE * 3

    def move(self):
        self.x = int(random.randint(
            0, (self.parent_screen.get_width()-SIZE)/SIZE)) * SIZE
        self.y = int(random.randint(
            0, (self.parent_screen.get_height()-SIZE)/SIZE)) * SIZE

        for i in range(self.snake.length):
            if self.is_collision(self.x, self.y, self.snake.x[i], self.snake.y[i]):
                self.move()
                break

        self.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.body = pygame.image.load(
            "resources/Snake Body.png").convert_alpha()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.x_vel = SIZE
        self.y_vel = 0

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_up(self):
        self.y_vel = -1*SIZE
        self.x_vel = 0

    def move_down(self):
        self.y_vel = SIZE
        self.x_vel = 0

    def move_left(self):
        self.x_vel = -1*SIZE
        self.y_vel = 0

    def move_right(self):
        self.x_vel = SIZE
        self.y_vel = 0

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        self.x[0] += self.x_vel
        self.y[0] += self.y_vel
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.play_background_music()
        pygame.mixer.music.set_volume(.15)
        self.surface = pygame.display.set_mode((1000, 600))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface, self.snake)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load("resources/Background Music.wav")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        self.sound = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(self.sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # Snake - Apple collision
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("resources/Eat Sound.wav")
            self.snake.increase_length()
            self.apple.move()

        # Snake - Snake collision
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("resources/Game Over Sound.wav")
                raise ValueError("Game over")

        # Snake - Wall collision
        if self.snake.x[0] > 1000 or self.snake.x[0] < 0:
            self.play_sound("resources/Game Over Sound.wav")
            raise ValueError("Game over")

        # Snake - Wall collision
        if self.snake.y[0] > 600 or self.snake.y[0] < 0:
            self.play_sound("resources/Game Over Sound.wav")
            raise ValueError("Game over")

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            f"To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.update()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface, self.snake)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except ValueError as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
