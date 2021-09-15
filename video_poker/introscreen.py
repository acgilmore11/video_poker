import pygame as pg
from pygame import Surface
from utils import load_sprite


class IntroScreen:
    def __init__(self, screen):
        self.intro_graphic = load_sprite("intropic2", True)
        self.intro_graphic2 = load_sprite("introcards", True)

    def draw(self,screen):
        screen.blit(self.intro_graphic, (screen.get_width() / 2 - self.intro_graphic.get_width() / 2,10))
        screen.blit(self.intro_graphic2, (screen.get_width() / 2 - self.intro_graphic2.get_width() / 2, screen.get_height() - 350))






