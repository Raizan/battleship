__author__ = 'Reisuke'

import pygame


class Battleship:
    def __init__(self, window, col, row, x, y, flag):
        self.window = window
        self.x = x
        self.y = y
        self.col = col
        self.row = row
        self.rect = None
        self.flag = flag
        if flag == "vertical":
            self.image = pygame.image.load("./assets/image/battleship_vertical.png")
        elif flag == "horizontal":
            self.image = pygame.image.load("./assets/image/battleship_horizontal.png")

    def render(self):
        self.rect = self.window.blit(self.image, (self.x, self.y))


class Line:
    def __init__(self, window, x, y, flag):
        self.window = window
        self.x = x
        self.y = y
        self.flag = flag
        if flag == "vertical":
            self.image = pygame.image.load("./assets/image/line_vertical.png")
        elif flag == "horizontal":
            self.image = pygame.image.load("./assets/image/line_horizontal.png")
        elif flag == "separator":
            self.image = pygame.image.load("./assets/image/separator.png")

    def render(self):
        self.window.blit(self.image, (self.x, self.y))


class Water:
    def __init__(self, window, col, row, x, y, flag):
        self.window = window
        self.flag = flag
        self.x = x
        self.y = y
        self.col = col
        self.row = row
        self.rect = None
        self.image_clicked = None
        self.image_1 = pygame.image.load("./assets/image/water_1.png")
        self.image_2 = pygame.image.load("./assets/image/water_2.png")
        self.image_3 = pygame.image.load("./assets/image/water_3.png")

        self.current_image = 1
        self.time_now = 0
        self.time_target = 10

    def update(self):
        self.render()

        if self.time_now == self.time_target:

            if self.current_image == 1:
                self.current_image += 1

            elif self.current_image == 2:
                self.current_image += 1

            else:
                self.current_image = 1

            self.time_now = 0

        else:
            self.time_now += 1

    def render(self):
        if self.flag == 1:
            self.rect = self.window.blit(self.image_clicked, (self.x, self.y))
        else:
            if self.current_image == 1:
                self.rect = self.window.blit(self.image_1, (self.x, self.y))

            elif self.current_image == 2:
                self.rect = self.window.blit(self.image_2, (self.x, self.y))

            elif self.current_image == 3:
                self.rect = self.window.blit(self.image_3, (self.x, self.y))
