from pygame.image import load
import pygame as pg
import os

BASE = os.path.dirname(os.path.abspath(__file__))
#may have to change path
def load_sprite(name, with_alpha=True):
    #path = f"C:/Users/acgfo/PycharmProjects/video_poker/assets/media/{name}.png"
    path = os.path.join(BASE, 'assets', 'media', name + '.png')
    print(BASE)
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

#may have to change path
def load_font(name, size):
    #path = f"C:/Users/acgfo/PycharmProjects/video_poker/assets/media/{name}.ttf"
    path = os.path.join(BASE, 'assets', 'media', name + '.ttf')
    return pg.font.Font(path, size)

def rank_to_num(rank):
    rankdict = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13
    }
    return rankdict[rank]

def num_to_hand(num):
    hand_dict = {
        0: ("Nothing", 0),
        1: ("a Pair", 1),
        2: ("Two Pairs", 2),
        3: ("a Three of a Kind", 3),
        4: ("a Straight", 4),
        5: ("a Flush", 6),
        6: ("a Full House", 9),
        7: ("a Four of a Kind", 25),
        8: ("a Straight Flush", 50),
        9: ("a Royal Flush", 250)
    }
    return hand_dict[num]