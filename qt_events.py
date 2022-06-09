import time
import random
from bs_functions import click

# Various functions to enter game and automate event clickers

def enter_qt_main_screen(game_width, game_height, hwnd):
    time.sleep(10)
    print("Click to update game")
    click(hwnd, 0.5 * game_width, 0.61875 * game_height)
    time.sleep(30)
    print("Click to enter server")
    click(hwnd, 0.5 * game_width, 0.90625 * game_height)
    time.sleep(30)
    print("Click to close event splash")
    click(hwnd, 0.5 * game_width, 0.909375 * game_height)
    time.sleep(3)
    print("Click to close carneval splash")
    click(hwnd, 0.7777 * game_width, 0.79375 * game_height)
    time.sleep(3)
    print("Click to close event splash")
    click(hwnd, 0.5 * game_width, 0.909375 * game_height)
    time.sleep(3)
    print("Click to close carneval splash")
    click(hwnd, 0.7777 * game_width, 0.79375 * game_height)
    time.sleep(3)
    print("Click to close event splash")
    click(hwnd, 0.5 * game_width, 0.909375 * game_height)
    time.sleep(3)
    print("Click to close carneval splash")
    click(hwnd, 0.7777 * game_width, 0.79375 * game_height)
    time.sleep(3)
    print("Click to close return to Main")
    click(hwnd, 0.1 * game_width, 0.96 * game_height)
    time.sleep(3)
    click(hwnd, 0.1 * game_width, 0.96 * game_height)
    time.sleep(3)


def enter_qt_event(game_width, game_height, hwnd):
    print("Click to enter QT event")
    click(hwnd, 0.5 * game_width, 0.56875 * game_height)
    time.sleep(10)
    print("Click to close event instruction")
    click(hwnd, 0.5 * game_width, 0.9 * game_height)
    time.sleep(5)


def qt_energy_tank(game_width, game_height, hwnd):
    print("Click to open energy tank")
    click(hwnd, 0.1333 * game_width, 0.8 * game_height)
    time.sleep(3)
    print("Click to open collect energy")
    click(hwnd, 0.8055 * game_width, 0.778125 * game_height)
    time.sleep(3)
    print("Click to close collect pop-up")
    click(hwnd, 0.5 * game_width, 0.6875 * game_height)
    time.sleep(3)
    print("Click to close energy tank windows")
    click(hwnd, 0.5 * game_width, 0.90625 * game_height)
    time.sleep(3)


def qt_tap(game_width, game_height, hwnd):
    print("Click to tap x5")
    click(hwnd, 0.0733 * game_width, 0.80625 * game_height)
    time.sleep(3)
    print("Click to tap 30")
    for i in range(30):
        click(hwnd, 0.5 * game_width, 0.5 * game_height)
        time.sleep(1)
