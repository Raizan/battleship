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

        self.attacked_image_1 = pygame.image.load("./assets/image/attacked_water_1.png")
        self.attacked_image_2 = pygame.image.load("./assets/image/attacked_water_2.png")
        self.attacked_image_3 = pygame.image.load("./assets/image/attacked_water_3.png")

        self.hit_image_1 = pygame.image.load("./assets/image/hit_water_1.png")
        self.hit_image_2 = pygame.image.load("./assets/image/hit_water_2.png")
        self.hit_image_3 = pygame.image.load("./assets/image/hit_water_3.png")

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
        if self.flag == "clicked":
            if self.current_image == 1:
                self.rect = self.window.blit(self.attacked_image_1, (self.x, self.y))

            elif self.current_image == 2:
                self.rect = self.window.blit(self.attacked_image_2, (self.x, self.y))

            elif self.current_image == 3:
                self.rect = self.window.blit(self.attacked_image_3, (self.x, self.y))

        elif self.flag == "hit":
            if self.current_image == 1:
                self.rect = self.window.blit(self.hit_image_1, (self.x, self.y))

            elif self.current_image == 2:
                self.rect = self.window.blit(self.hit_image_2, (self.x, self.y))

            elif self.current_image == 3:
                self.rect = self.window.blit(self.hit_image_3, (self.x, self.y))

        else:
            if self.current_image == 1:
                self.rect = self.window.blit(self.image_1, (self.x, self.y))

            elif self.current_image == 2:
                self.rect = self.window.blit(self.image_2, (self.x, self.y))

            elif self.current_image == 3:
                self.rect = self.window.blit(self.image_3, (self.x, self.y))


class Hit:
    def __init__(self, window, col, row, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.col = col
        self.row = row
        self.rect = None
        self.image = pygame.image.load("./assets/image/hit.png")

    def render(self):
        self.rect = self.window.blit(self.image, (self.x, self.y))


class Explosion:
    def __init__(self, window, col, row, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.col = col
        self.row = row
        self.rect = None
        self.image_clicked = None
        self.image_1 = pygame.image.load("./assets/image/explosion_0001.png")
        self.image_2 = pygame.image.load("./assets/image/explosion_0002.png")
        self.image_3 = pygame.image.load("./assets/image/explosion_0003.png")
        self.image_4 = pygame.image.load("./assets/image/explosion_0004.png")
        self.image_5 = pygame.image.load("./assets/image/explosion_0005.png")
        self.image_6 = pygame.image.load("./assets/image/explosion_0006.png")
        self.image_7 = pygame.image.load("./assets/image/explosion_0007.png")
        self.image_8 = pygame.image.load("./assets/image/explosion_0008.png")
        self.image_9 = pygame.image.load("./assets/image/explosion_0009.png")
        self.image_10 = pygame.image.load("./assets/image/explosion_0010.png")
        self.image_11 = pygame.image.load("./assets/image/explosion_0011.png")
        self.image_12 = pygame.image.load("./assets/image/explosion_0012.png")
        self.image_13 = pygame.image.load("./assets/image/explosion_0013.png")
        self.image_14 = pygame.image.load("./assets/image/explosion_0014.png")
        self.image_15 = pygame.image.load("./assets/image/explosion_0015.png")
        self.image_16 = pygame.image.load("./assets/image/explosion_0016.png")
        self.image_17 = pygame.image.load("./assets/image/explosion_0017.png")
        self.image_18 = pygame.image.load("./assets/image/explosion_0018.png")
        self.image_19 = pygame.image.load("./assets/image/explosion_0019.png")
        self.image_20 = pygame.image.load("./assets/image/explosion_0020.png")
        self.image_21 = pygame.image.load("./assets/image/explosion_0021.png")
        self.image_22 = pygame.image.load("./assets/image/explosion_0022.png")
        self.image_23 = pygame.image.load("./assets/image/explosion_0023.png")
        self.image_24 = pygame.image.load("./assets/image/explosion_0024.png")

        self.current_image = 1
        self.time_now = 0
        self.time_target = 10

    def update(self):
        self.render()

        if self.time_now == self.time_target:

            if self.col == 24:
                self.current_image = 1
            else:
                self.current_image += 1

            self.time_now = 0

        else:
            self.time_now += 1

    def render(self):
        if self.current_image == 1:
            self.rect = self.window.blit(self.image_1, (self.x, self.y))

        elif self.current_image == 2:
            self.rect = self.window.blit(self.image_2, (self.x, self.y))

        elif self.current_image == 3:
            self.rect = self.window.blit(self.image_3, (self.x, self.y))

        elif self.current_image == 4:
            self.rect = self.window.blit(self.image_4, (self.x, self.y))

        elif self.current_image == 5:
            self.rect = self.window.blit(self.image_5, (self.x, self.y))

        elif self.current_image == 6:
            self.rect = self.window.blit(self.image_6, (self.x, self.y))

        elif self.current_image == 7:
            self.rect = self.window.blit(self.image_7, (self.x, self.y))

        elif self.current_image == 8:
            self.rect = self.window.blit(self.image_8, (self.x, self.y))

        elif self.current_image == 9:
            self.rect = self.window.blit(self.image_9, (self.x, self.y))

        elif self.current_image == 10:
            self.rect = self.window.blit(self.image_10, (self.x, self.y))

        elif self.current_image == 11:
            self.rect = self.window.blit(self.image_11, (self.x, self.y))

        elif self.current_image == 12:
            self.rect = self.window.blit(self.image_12, (self.x, self.y))

        elif self.current_image == 13:
            self.rect = self.window.blit(self.image_13, (self.x, self.y))

        elif self.current_image == 14:
            self.rect = self.window.blit(self.image_14, (self.x, self.y))

        elif self.current_image == 15:
            self.rect = self.window.blit(self.image_15, (self.x, self.y))

        elif self.current_image == 16:
            self.rect = self.window.blit(self.image_16, (self.x, self.y))

        elif self.current_image == 17:
            self.rect = self.window.blit(self.image_17, (self.x, self.y))

        elif self.current_image == 18:
            self.rect = self.window.blit(self.image_18, (self.x, self.y))

        elif self.current_image == 19:
            self.rect = self.window.blit(self.image_19, (self.x, self.y))

        elif self.current_image == 20:
            self.rect = self.window.blit(self.image_20, (self.x, self.y))

        elif self.current_image == 21:
            self.rect = self.window.blit(self.image_21, (self.x, self.y))

        elif self.current_image == 22:
            self.rect = self.window.blit(self.image_22, (self.x, self.y))

        elif self.current_image == 23:
            self.rect = self.window.blit(self.image_23, (self.x, self.y))

        elif self.current_image == 24:
            self.rect = self.window.blit(self.image_24, (self.x, self.y))