import pygame
import os
import sys
import random
from PIL import Image


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.go = False
        self.crop('data\\image.png')

        GRAY = pygame.Color('gray15')
        BLUE = pygame.Color('dodgerblue1')
        LIGHTBLUE = pygame.Color('lightskyblue1')
        font = pygame.font.Font(None, 30)

        BUTTON_UP_IMG = self.load_image('16.png')
        BUTTON_UP_IMG.fill(GRAY)

        self.rectangles = []
        self.coords = []
        self.pressed = 15
        self.empty = 15
        self.counter = 'PRESS ENTER TO START'
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        somex, somey = 176, 134

        for i in range(17):
            if i != 0:
                self.rectangles.append(self.load_image(str(i) + '.png'))
        self.rectangles[-1] = BUTTON_UP_IMG

        for i in range(16):
            self.rectangles[i].set_colorkey(i)

        for _ in range(4):
            for __ in range(4):
                self.coords.append((somex, somey))
                somex += 66
            somex = 176
            somey += 66

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if self.go:
                        self.counter = str(int(self.counter) + 1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.go = True
                        self.counter = '0'
                        self.shuffle()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for o in range(16):
                            if self.rectangles[o].get_rect(topleft=self.coords[o]).collidepoint(event.pos):
                                self.pressed = o
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.rotate(self.pressed)

            self.screen.fill(GRAY)
            for ii in range(16):
                self.screen.blit(self.rectangles[ii], self.rectangles[ii].get_rect(topleft=self.coords[ii]))
            txt = font.render(str(self.counter), True, BLUE)
            self.screen.blit(txt, (180, 100))

            c = 0
            for l in range(len(self.rectangles)):
                if self.rectangles[l].get_colorkey()[0] == l:
                    c += 1
            if c == 16 and self.go:
                self.go = False

            pygame.display.flip()
            self.clock.tick(60)

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data\\squares', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def rotate(self, prs):
        if abs(prs - self.empty) == 4 or (prs - self.empty == 1 and (prs != 4 and prs != 8 and prs != 12)) \
                or (prs - self.empty == -1 and (prs != 3 and prs != 7 and prs != 11)):
            self.rectangles[prs], self.rectangles[self.empty] = self.rectangles[self.empty], self.rectangles[prs]
            self.empty = prs

    def shuffle(self):
        for turns in range(300):
            if random.randint(1, 4) == 1 and self.empty < 12:
                self.pressed = self.empty + 4
            elif random.randint(1, 4) == 2 and self.empty < 14:
                self.pressed = self.empty + 1
            elif random.randint(1, 4) == 3 and self.empty > 3:
                self.pressed = self.empty - 4
            elif random.randint(1, 4) == 4 and self.empty > 0:
                self.pressed = self.empty - 1
            self.rotate(self.pressed)

    def crop(self, path):
        im = Image.open(path)
        im = im.resize((256, 256))
        x1, y1, x2, y2 = 0, 0, 64, 64
        c1 = 1
        for _ in range(4):
            for __ in range(4):
                im2 = im.crop((x1, y1, x2, y2))
                im2.save('data\\squares\\' + str(c1) + '.png')
                x1 += 64
                x2 += 64
                c1 += 1
            x1 = 0
            x2 = 64
            y1 += 64
            y2 += 64


if __name__ == '__main__':
    game = Game(640, 480)
