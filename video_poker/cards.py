import random
import pygame as pg
from utils import load_sprite, rank_to_num

CARD_IMAGE_SIZE = (204, 300)
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['C', 'D', 'H', 'S']


class Card:
    def __init__(self, rank, suit):
        self.clicked = False
        self.suit = suit
        self.rank = rank
        self.num = rank_to_num(rank)
        self.image = pg.transform.scale(load_sprite(f'cards/{rank}{suit}'), CARD_IMAGE_SIZE)
        self.rect = self.image.get_rect()

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_num(self):
        return self.num

    def get_card_rect(self):
        return self.rect

    def draw (self, screen, coord, swapped):
        self.rect.topleft = coord
        if not swapped:
            if not self.clicked:
                pg.draw.rect(screen, (255,0,0), [coord[0] - 10,coord[1] - 10, CARD_IMAGE_SIZE[0] + 20, CARD_IMAGE_SIZE[1] + 20])
            else:
                pg.draw.rect(screen, (0, 0, 0), [coord[0] - 10, coord[1] - 10, CARD_IMAGE_SIZE[0] + 20, CARD_IMAGE_SIZE[1] + 20])
        screen.blit(self.image, self.rect)


class GroupOfCards:
    def __init__(self):
        self.num_cards = 0
        self.cards = list()

    def add_card(self, card):
        self.cards.append(card)
        self.num_cards += 1

    def deal_card(self):
        self.num_cards -= 1
        return self.cards.pop(0)

    def replace_card(self, card, index):
        self.cards[index] = card

    def sort_cards(self):
        self.cards.sort(key=lambda card: card.num)

    def get_cards(self):
        return self.cards

    #debug
    def print(self):
        for c in self.cards:
            print (f'{c.get_rank()} of {c.get_suit()}')


class Deck(GroupOfCards):
    def __init__(self):
        super().__init__()
        for r in ranks:
            for s in suits:
                card = Card(r, s)
                self.add_card(card)

    def deal_hand(self):
        cards = list()
        for x in range(5):
            cards.append(self.deal_card())
        return Hand(cards)

    def shuffle(self):
        for i in range(10):
            random.shuffle(self.cards)


class Hand(GroupOfCards):
    def __init__(self, cards):
        super().__init__()
        self.cards = cards
        self.num_cards = len(cards)
        self.swapped = False

    def draw(self, screen):
        index = 0
        for i in range (30, screen.get_width(), CARD_IMAGE_SIZE[0] + 30):
            self.cards[index].draw(screen, (i, screen.get_height() / 2 - CARD_IMAGE_SIZE[1] / 2), self.swapped)
            index += 1

        if not self.swapped:
            myfont = pg.font.SysFont('Times New Roman', 25)
            swapbar = myfont.render("To Swap Selected Cards, Press Enter", False, (255, 255, 255))
            screen.blit(swapbar, (screen.get_width() / 2 - swapbar.get_width() / 2, screen.get_height() * (3 / 4)))

    def handle_click(self,click):
        for c in self.cards:
            if c.get_card_rect().collidepoint(click):
                c.clicked = not c.clicked

    def handle_enter(self, event, deck):
        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
            for i in range(5):
                if self.cards[i].clicked:
                    self.replace_card(deck.deal_card(), i)

        print()
        self.print()
        self.sort_cards()
        self.swapped = True




