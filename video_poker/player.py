import pygame as pg
from pygame.image import load
from pygame import Surface
from utils import load_sprite


class Player:
    def __init__(self):
        self.avatar = load_sprite('avatar', True)
        self.name = ''
        self.money = 0
        self.curr_bet = 0
        self.total_winnings = 0

    def set_name(self, name):
        self.name = name

    def get_money(self):
        return self.money

    def add_starting_amount(self, amount):
        self.money += amount

    def set_bet(self, bet):
        self.curr_bet = bet
        self.money -= bet

    def add_winnings(self, winnings, bet):
        self.money += (winnings + bet)
        self.total_winnings += winnings

    def get_bet(self):
        return self.curr_bet

    def draw(self, screen):
        screen.blit(self.avatar, (0,screen.get_height()-50))
        myfont = pg.font.SysFont('Times New Roman', 25)

        creditbar = self.create_text_bar(myfont, 'Credits: ${:0.2f}', self.money, (0,0,0), (0,153,0))
        screen.blit(creditbar, (screen.get_width() / 2 - creditbar.get_width() / 2, screen.get_height() - 40))

        winningbar = self.create_text_bar(myfont, 'Total Winnings (Score): ${:0.2f}', self.total_winnings, (0,0,0), (0,153,0))
        screen.blit(winningbar,(screen.get_width() / 2 - winningbar.get_width() / 2, 0))

        namebar = myfont.render(self.name, False, (0, 0, 0))
        screen.blit(namebar, (self.avatar.get_width() + 5, screen.get_height()-40))

        if self.curr_bet > 0:
            moneybar = self.create_text_bar(myfont, 'Bet: ${:0.2f}', self.curr_bet, (0,0,0), (0,153,0))
            screen.blit(moneybar, (screen.get_width() - moneybar.get_width() - 5, screen.get_height() - 40))

    def create_text_bar(self, font, prompt, value, text_color, bar_color):
        textbar = font.render(prompt.format(value), False, text_color)
        textbar_outline = Surface((textbar.get_width(), textbar.get_height()))
        textbar_outline.fill(bar_color)
        textbar_outline.blit(textbar, (0, 0))
        return textbar_outline



