import pygame as pg
from pygame import Surface
from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, load_font


class InputBox:
    def __init__(self, screen, w, h, c, prompt):
        self.entered = False
        self.color = c
        self.prompt = prompt
        self.window = Surface((w, h))
        self.window_coord = (screen.get_width() / 2 - w / 2, screen.get_height() / 2 - h / 2)
        self.window.fill(c)


class NameBox(InputBox):
    color = (255, 0, 0)
    name_surface = None

    def __init__(self, screen, w, h, c, prompt):
        super().__init__(screen, w, h, c, prompt)
        self.input = ''
        self.clicked = False
        self.box_rect = pg.Rect((self.window_coord[0], self.window_coord[1] + h - 30), (w, 30))
        self.namebox = Surface((w, 30))
        self.namebox.fill((192, 192, 192))
        self.myfont = pg.font.SysFont('Times New Roman', 30)
        self.prompt_surface = self.myfont.render(self.prompt, False, (255,255,255))

    def handle_input(self, event, player):
        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
            self.enter()
            player.set_name(self.input)
        elif event.key == pg.K_BACKSPACE:
            self.back()
        else:
            self.type(event)
        self.update()

    def type(self,event):
        self.input += event.unicode

    def back(self):
        self.input = self.input[:-1]

    def enter(self):
        print(self.input)
        self.entered = True

    def update(self):
        self.namebox.fill((192, 192, 192))
        self.name_surface = self.myfont.render(self.input, False, (0, 0, 0))
        self.namebox.blit(self.name_surface, (0, 0))
        self.window.blit(self.namebox, (0, self.window.get_height() - self.namebox.get_height()))

    def draw(self,screen):
        pg.draw.rect(screen, (255, 255, 255), self.box_rect)
        screen.blit(self.window, (screen.get_width() / 2 - self.window.get_width() / 2, screen.get_height() / 2 - self.window.get_height() / 2))
        self.window.blit(self.prompt_surface, (0, 0))
        self.window.blit(self.namebox, (0, self.window.get_height() - self.namebox.get_height()))


class StartBox(InputBox):
    def __init__(self, screen, w, h, c, prompt):
        super().__init__(screen, w, h, c, prompt)
        self.input = ''
        self.clicked = False
        self.value = 0
        self.bills = [Bill('1', (300, 128)), Bill('5', (300, 128)), Bill('10', (300, 128))]

    def draw(self,screen):
        myfont = pg.font.SysFont('Times New Roman', 30)
        namebar = myfont.render(self.prompt, False, (0, 0, 0))
        self.window.blit(namebar, (self.window.get_width() / 2 - namebar.get_width() / 2,0))

        screen.blit(self.window, (screen.get_width() / 2 - self.window.get_width() / 2, screen.get_height() / 2 - self.window.get_height() / 2))
        i = 5
        for b in self.bills:
            b.draw(screen, (screen.get_width() / 2 - self.window.get_width() / 2 + i, screen.get_height() / 2 + self.window.get_height() / 2 - 128 - 5))
            i += 305

    def bill_clicked(self, click):
        clicked = False
        i = 0
        while not clicked and i < len(self.bills):
            if self.bills[i].get_bill_rect().collidepoint(click):
                clicked = True
                self.value = self.bills[i].get_value()
            i += 1

        return clicked

    def get_value(self):
        return self.value

    def set_click(self):
        self.clicked = True


class BetBox(InputBox):
    def __init__(self, screen, w, h, c, prompt):
        super().__init__(screen, w, h, c, prompt)
        self.clicked = 0
        self.coin = Bill('0.50', (105, 105))

    def draw(self,screen):
        self.window.fill(self.color)
        myfont = pg.font.SysFont('Times New Roman', 30)
        namebar = myfont.render(self.prompt, False, (0, 0, 0))
        betbar = myfont.render(f'x {self.clicked}', False, (255,255,255))
        self.window.blit(namebar, (self.window.get_width() / 2 - namebar.get_width() / 2,0))
        self.window.blit(betbar, (self.window.get_width() / 2 - betbar.get_width() / 2, self.window.get_height() - betbar.get_height()))

        screen.blit(self.window, (screen.get_width() / 2 - self.window.get_width() / 2, screen.get_height() / 2 - self.window.get_height() / 2))
        self.coin.draw(screen, (self.window_coord[0] + self.window.get_width()/2 - self.coin.image.get_width()/2,
                                self.window_coord[1] + namebar.get_height() + 10))

    def handle_click(self, click):
        if self.coin.get_bill_rect().collidepoint(click) and self.clicked < 2:
            self.clicked += 1

    def handle_enter(self, event, player):
        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
            self.entered = True
            player.set_bet(self.clicked * 0.50)


class Bill:
    def __init__(self, currency, size):
        self.image = pg.transform.scale(load_sprite(currency), size)
        self.rect = self.image.get_rect()
        self.value = float(currency)

    def draw(self, screen, coord):
        self.rect.topleft = coord
        screen.blit(self.image, self.rect)


    def get_bill_rect(self):
        return self.rect

    def get_value(self):
        return self.value

class WinningsBox:
    # UP = Vector2(0,-1)
    def __init__(self, screen, size, hand, winnings):
        self.image = pg.transform.scale(load_sprite(f'award'), size)
        self.coord = Vector2(screen.get_width() / 2 - size[0] / 2, screen.get_width())
        self.velocity = Vector2(0, -20)
        self.center_reached = False
        myfont = load_font('Verve', 50)
        self.handbar = myfont.render(f'You got {hand}', False, (0, 0, 0))
        self.winbar = myfont.render('You win ${:0.2f}'.format(winnings), False, (0, 153, 0))

    def draw(self, screen):
        self.image.blit(self.handbar, (self.image.get_width() / 2 - self.handbar.get_width() / 2,
                                       self.image.get_height() / 2 - self.handbar.get_height()))
        self.image.blit(self.winbar, (self.image.get_width() / 2 - self.winbar.get_width() / 2,
                                      self.image.get_height() / 2 + self.handbar.get_height()))
        screen.blit(self.image, self.coord)

    def handle_enter(self, player, winnings):
        if winnings > 0:
            player.add_winnings(winnings, player.curr_bet)

    def move(self, screen):
        self.coord = self.coord + self.velocity
        if self.coord[1] <= (screen.get_height() / 2 - self.image.get_height() / 2):
            self.center_reached = True

