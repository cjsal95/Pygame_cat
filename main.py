import pygame, sys
from pygame.locals import *
import random
import time

from utils.pyg_button import Button
from utils.pyg_tools import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

EVENT_FLAG = False

progoramIcon = pygame.image.load("icon.png")
pygame.display.set_icon(progoramIcon)


class Object2(pygame.sprite.Sprite):
    def __init__(self, img_path, speed=2):
        super().__init__()
        self.images = readImg(img_path)
        self.image = self.images[2]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.pos = pygame.Vector2(150, 150)
        self.set_target((0, 0))
        self.speed = speed

        self.hungry_state = 100

    def state_update(self):
        if self.hungry_state > 0.0:
            self.hungry_state -= 0.1
        if self.hungry_state < 0:
            self.image = self.images[4]
        elif 0 < self.hungry_state < 30:
            self.image = self.images[3]
        elif 30 <= self.hungry_state < 70:
            self.image = self.images[2]
        elif 70 <= self.hungry_state < 100:
            self.image = self.images[1]
        elif 100 <= self.hungry_state:
            self.image = self.images[0]

    def set_target(self, pos):
        self.target = pygame.Vector2(pos[0], pos[1] + 100)

    def update(self):
        if self.hungry_state > 0:
            if self.target != list(int(v) for v in self.pos):
                move = self.target - self.pos
                move_length = move.length()

                if move_length < self.speed:
                    self.pos = self.target
                elif move_length != 0:
                    move.normalize_ip()
                    move = move * self.speed
                    self.pos += move
                self.rect.center = list(int(v) for v in self.pos)

            else:
                px = random.randint(self.rect.centerx-10, self.rect.centerx+10)
                if px < 0 + self.image.get_width():
                    px = self.image.get_width()
                elif px > SCREEN_WIDTH:
                    px = SCREEN_WIDTH
                py = random.randint(self.rect.centery-10, self.rect.centery+10)
                if py < 0 + self.image.get_height():
                    py = self.image.get_height()
                elif py > SCREEN_HEIGHT:
                    py = SCREEN_HEIGHT

                self.target = pygame.Vector2(px, py)



class Object1(pygame.sprite.Sprite):
    def __init__(self, img_path, screen):
        super().__init__()
        self.img = pygame.image.load(img_path)
        self.rect = self.img.get_rect()
        self.rect.center = (-100, -50)
        self.screen = screen
        self.flag = False
        self.py = 0
    
    def move(self, px, py):
        self.flag = True
        self.py = py
        self.rect.center = (px, py)
        
    def draw(self):
        if self.flag:
            if self.rect.centery < self.py + 5*20:
                self.rect.move_ip(0, 5)
            self.screen.blit(self.img, self.rect)


class Event1(pygame.sprite.Sprite):
    def __init__(self, img_path, screen):
        super().__init__()
        self.images = readImg(img_path)
        self.screen = screen
        self.img_cnt = 0
        self.endflg = False
        
    def draw(self):
        global EVENT_FLAG
        
        if int(self.img_cnt) > 5:
            self.img_cnt = 0
            EVENT_FLAG = False
        else:
            self.screen.blit(self.images[int(self.img_cnt)], (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.img_cnt += 0.2
            if round(self.img_cnt, 2) == 4.8:
                self.endflg = True
            else:
                self.endflg = False

def event_change():
    global EVENT_FLAG
    EVENT_FLAG = True     

def quitgame():
    pygame.quit()
    sys.exit()

FramePerSec = pygame.time.Clock()
pygame.init()


# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("my cat")
surf = pygame.Surface((50,50))

cat1 = Object2("asset/cat1/")
group = pygame.sprite.Group()
group.add(cat1)
ob1 = Object1("obj1.png", screen)

ev1 = Event1("asset/box/", screen)

# Run until the user asks to quit
running = True
while running:
    mouse = pygame.mouse.get_pos()
    mclick = pygame.mouse.get_pressed()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            # the user clicks the window close button
            running = False

    for obj in group.sprites():
        obj.state_update()

    # Fill the background with white
    screen.fill((255, 255, 255))

    btn = Button(screen, 10, 10, "asset/btn1/button.png", "asset/btn1/button_pressed.png", quitgame)
    btn1 = Button(screen, 10, 100, "asset/btn2/button.png", "asset/btn2/button_pressed.png", event_change)

    if EVENT_FLAG:
        ev1.draw()
        if ev1.endflg:
            group.add(Object2("asset/cat1/"))

    if mclick[0]:
        ob1.move(mouse[0], mouse[1])
        for obj in group.sprites():
            obj.set_target(pygame.mouse.get_pos())
    
    group.update()
    group.draw(screen)

    if not pygame.sprite.spritecollideany(ob1, group):
        ob1.draw()
    else:
        if 0 < cat1.hungry_state < 200:
            cat1.hungry_state += 10
        
        ob1.flag = False
        ob1.rect.center = (-50, -50)
        
    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()
    FramePerSec.tick(60)

# Done! Time to quit.
pygame.quit()