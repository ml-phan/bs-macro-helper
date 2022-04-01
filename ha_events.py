import time
import random
from bs_functions import click, get_game_dimension

tap_char_list = [(1, 1),
                 (2, 1),
                 (2, 2),
                 (4, 2),
                 (5, 2),
                 (1, 3),
                 (4, 3),
                 (2, 4),
                 (4, 4),
                 (2, 5),
                 (4, 5),
                 (5, 5),
                 ]


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
    time.sleep(30)


def char_list(game_width, game_height, hwnd):
    print("Click to enter character menu")
    click(hwnd, 0.277 * game_width, 0.96 * game_height)
    time.sleep(5)
    print("Click to enter character listings")
    click(hwnd, 0.5 * game_width, 0.525 * game_height)
    time.sleep(5)


def all_tap(game_width, game_height, hwnd):
    for i in tap_char_list:
        a, b = pos_to_coordinate(i)
        print("Click to enter character number", i.index()+1)
        click(hwnd, a * game_width, b * game_height)
        time.sleep(5)
        tap_single_char(game_width, game_height, hwnd)


def tap_single_char(game_width, game_height, hwnd):
    print("Click to enter tap event page")
    for i in range(4):
        for i in range(10):
            random_width = random.uniform(-0.4, 0.4)
            random_height = random.uniform(-0.1125, 0.1125)
            click(hwnd, (0.5 + random_width) * game_width, (0.44375 + random_height) * game_height)
            time.sleep(5)
        print("Click to confirm out of stamina")
        click(hwnd, 0.5 * game_width, 0.6125 * game_height)
        time.sleep(5)
        tap_single_char(game_width, game_height, hwnd)
        print("Click to cancel buying stamina")
        click(hwnd, 0.3222 * game_width, 0.671875 * game_height)
        time.sleep(5)
        tap_single_char(game_width, game_height, hwnd)
    print("Click to exit tap event page")
    click(hwnd, 0.0667 * game_width, 0.875 * game_height)
    time.sleep(5)