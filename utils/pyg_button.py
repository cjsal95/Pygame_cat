import pygame
from pygame.locals import *


class Button:
    def __init__(self, screen, px, py, btn_img_path, btn_press_img_path=None, action=None):
        mouse = pygame.mouse.get_pos()
        mclick = pygame.mouse.get_pressed()

        self.btn_img = pygame.image.load(btn_img_path)
        self.btn_press_img = None
        if btn_press_img_path is not None:
            self.btn_press_img = pygame.image.load(btn_press_img_path)
        self.btn_height = self.btn_img.get_height()
        self.btn_width = self.btn_img.get_width()

        if px + self.btn_width > mouse[0] > px and py + self.btn_height > mouse[1] > py:
            if self.btn_press_img != None:
                screen.blit(self.btn_press_img, (px, py))
            if mclick[0] and action != None:
                action()
        else:
            screen.blit(self.btn_img, (px, py))