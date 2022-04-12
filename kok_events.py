import time
import random

from bs_functions import click


def to_kok_event(game_width, game_height, hwnd):
    time.sleep(10)
    print("Click to close event splash")
    click(hwnd, 0.5 * game_width, 0.06 * game_height)
    time.sleep(5)
    print("Click to enter server")
    click(hwnd, 0.5 * game_width, 0.875 * game_height)
    time.sleep(10)
    print("Click to close Mihime sale")
    click(hwnd, 0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    click(hwnd, 0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    click(hwnd, 0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    print("Click to close return to Main")
    click(hwnd, 0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
    click(hwnd, 0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
    click(hwnd, 0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
    print("Click to enter KoK event")
    click(hwnd, 0.455 * game_width, 0.625 * game_height)


def kok_alchemy_event_tap(game_width, game_height, hwnd):
    time.sleep(10)
    print("Click to open Alchemy Urn")
    click(hwnd, 0.1222 * game_width, 0.8562 * game_height)
    time.sleep(5)
    print("Click to claim Alchemy")
    click(hwnd, 0.6777 * game_width, 0.7437 * game_height)
    time.sleep(5)
    print("Click to close Alchemy claim notice")
    click(hwnd, 0.5 * game_width, 0.22 * game_height)


def kok_alchemy_tap(game_width, game_height, hwnd):
    print("Click to claim Alchemy")
    i = 0
    while i < 200:
        time.sleep(3)
        random_width = random.uniform(-0.4, 0.4)
        random_height = random.uniform(-0.12, 0.12)
        click(hwnd, (0.5+random_width) * game_width, (0.1875 + random_height) * game_height)
        i += 1
        if i % 100 == 0:
            print("Click number:", i)


def kok_wine(game_width, game_height, hwnd):
    print("Click to open wine urn")
    click(hwnd, 0.1 * game_width, 0.875 * game_height)
    time.sleep(3)
    print("Click to collect wine")
    click(hwnd, 0.75 * game_width, 0.7 * game_height)

