import time
import random
from bs_functions import click

tap_char_list = [(1, 1),  # Gill
                 (3, 1),  # Seila
                 (2, 2),  # Juno
                 (4, 2),  # Emma
                 (5, 2),  # Mimi
                 (3, 3),  # Scarlett
                 (5, 3),  # Celia
                 (2, 4),  # Rita
                 (5, 4),  # Lan
                 (1, 5),  # T3-5
                 (3, 5),  # Xaville
                 (4, 5),  # Ann
                 (1, 6),  # Vannessa
                 ]


# Various functions to enter game and automate event clickers


def pos_to_coordinate(a):
    x = 0.112 + (a[0] - 1) * 0.19
    y = 0.195 + (a[1] - 1) * 0.106
    return x, y


def ha_enter_game(game_width, game_height, hwnd):
    time.sleep(1)
    print("Click to update game")
    click(hwnd, 0.5 * game_width, 0.618 * game_height)
    time.sleep(5)
    print("Click to enter game")
    click(hwnd, 0.5 * game_width, 0.956 * game_height)
    time.sleep(50)
    print("Click to close event splash game")
    click(hwnd, 0.5 * game_width, 0.9375 * game_height)
    time.sleep(5)
    print("Click to return to main")
    click(hwnd, 0.5 * game_width, 0.95 * game_height)
    time.sleep(5)


def to_char_list(game_width, game_height, hwnd):
    print("Click to enter character menu")
    click(hwnd, 0.277 * game_width, 0.96 * game_height)
    time.sleep(5)
    print("Click to enter character listings")
    click(hwnd, 0.5 * game_width, 0.525 * game_height)
    time.sleep(5)


def all_tap(game_width, game_height, hwnd):
    for i in tap_char_list:
        a, b = pos_to_coordinate(i)
        print("Click to enter character number", tap_char_list.index(i)+1)
        click(hwnd, a * game_width, b * game_height)
        time.sleep(5)
        tap_single_char(game_width, game_height, hwnd)


def tap_single_char(game_width, game_height, hwnd):
    print("Click to enter tap event page")
    click(hwnd, 0.933 * game_width, 0.334375 * game_height)
    time.sleep(2)
    for i in range(4):
        for j in range(30):
            random_width = random.uniform(-0.2, 0.2)
            random_height = random.uniform(-0.1125, 0.1125)
            click(hwnd, (0.5 + random_width) * game_width, (0.44375 + random_height) * game_height)
            time.sleep(0.8)
        print("Click to confirm out of stamina")
        click(hwnd, 0.5 * game_width, 0.6125 * game_height)
        time.sleep(2)
        print("Click to cancel buying stamina")
        click(hwnd, 0.3222 * game_width, 0.671875 * game_height)
        time.sleep(2)
    print("Click to exit tap event page")
    click(hwnd, 0.0667 * game_width, 0.875 * game_height)
    time.sleep(3)
    print("Click to exit character page")
    click(hwnd, 0.07222 * game_width, 0.96875 * game_height)
    time.sleep(2)