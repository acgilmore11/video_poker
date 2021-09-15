import pygame as pg
from cards import Card, GroupOfCards, Deck, Hand

from introscreen import IntroScreen
from player import Player
from inputbox import NameBox, StartBox, WinningsBox, BetBox
from utils import load_sprite, num_to_hand
from analyzer import HandAnalyzer
import sys


class VideoPoker:
    def __init__(self):
        self._init_pygame()
        self.screen = pg.display.set_mode((1200,800))
        self.background = load_sprite("background", False)
        self.clock = pg.time.Clock()
        self.name_box = NameBox(self.screen, 500, 80, (139,26,26), 'Type name and then click enter to begin:')
        self.intro_graphics = IntroScreen(self.screen)
        self.game_objects = [self.name_box, self.intro_graphics]
        self.player = Player()
        self.startBox = None
        self.betBox = None
        self.deck = Deck()
        self.hand = None
        self.analyzer = None
        self.analyzed = False
        self.winning_box = None
        self.curr_winnings = 0

    def start(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pg.init()
        pg.display.set_caption("AG Video Poker")

    def _handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.name_box.box_rect.collidepoint(event.pos):
                    self.name_box.clicked = True
                if self.startBox and self.startBox.bill_clicked(event.pos) and not self.betBox:
                    self.player.add_starting_amount(self.startBox.get_value())
                    self.startBox.clicked = True
                if self.betBox and not self.hand:
                    self.betBox.handle_click(event.pos)
                if self.hand:
                    self.hand.handle_click(event.pos)

            if event.type == pg.KEYDOWN:
                if self.name_box.clicked and not self.name_box.entered and not self.hand:
                    self.name_box.handle_input(event, self.player)
                if self.betBox and self.betBox.clicked > 0:
                    self.betBox.handle_enter(event, self.player)
                if self.hand and not self.hand.swapped:
                    self.hand.handle_enter(event, self.deck)
                if self.winning_box and self.winning_box.center_reached:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        self.winning_box.handle_enter(self.player, self.curr_winnings)
                        self.re_init()

    def _process_game_logic(self):
        self.ask_for_start_amount()
        self.ask_for_bet()
        self.create_hand()
        self.analyze_hand()
        self.display_winnings()

    def _draw(self):
        self.screen.blit(self.background, (0,0))

        for model in self.game_objects:
            model.draw(self.screen)

        pg.display.flip()
        self.clock.tick(30)

    def ask_for_start_amount(self):
        if self.name_box.entered and not self.startBox:
            self.game_objects = [self.player]
            self.startBox = StartBox(self.screen, 920, 175, (0, 153, 0), 'Click Bill for Starting Amount:')
            self.game_objects = [self.player, self.startBox]

    def ask_for_bet(self):
        if self.startBox and self.startBox.clicked:
            self.startBox.clicked = False
            self.game_objects = [self.player]
            self.betBox = BetBox(self.screen, 250, 180, (0, 153, 0), 'Click Bet Amount:')
            self.game_objects = [self.player, self.betBox]

    def create_hand(self):
        if self.betBox and self.betBox.entered:
            self.betBox.entered = False
            self.betBox.clicked = 0
            self.init_hand()
            #self.test_init_hand()
            self.game_objects = [self.player, self.hand]

    def analyze_hand(self):
        if self.hand and self.hand.swapped and not self.analyzed:
            self.analyzer = HandAnalyzer(self.hand)
            self.analyzer.analyze()
            self.analyzed = True
            self.curr_winnings = self.player.get_bet() * num_to_hand(self.analyzer.get_hand_type())[1]
            self.winning_box = WinningsBox(self.screen, (775, 775), num_to_hand(self.analyzer.get_hand_type())[0],
                                           self.curr_winnings)

    def display_winnings(self):
        if self.analyzed:
            self.game_objects = [self.player, self.hand, self.winning_box]
            if self.winning_box and not self.winning_box.center_reached:
                self.winning_box.move(self.screen)

    def init_hand(self):
        self.deck.shuffle()
        self.hand = self.deck.deal_hand()
        self.hand.sort_cards()
        #debug
        self.hand.print()

    def re_init(self):
        self.betBox = None
        self.hand = None
        self.deck = Deck()
        self.analyzer = None
        self.winning_box = None
        self.analyzed = False
        self.betBox = None
        self.startBox.clicked = True
        self.player.set_bet(0)

    def test_init_hand(self):
        cards = [Card('A', 'C'), Card('A', 'S'), Card('K', 'D'), Card('6', 'D'), Card('2', 'H')]
        self.hand = Hand(cards)
        self.hand.sort_cards()
        #debug
        self.hand.print()


