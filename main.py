import time

from bs_functions import *
from kok_events import *
from ha_events import *
from qt_events import *


def kok_alchemy_pipeline(bit):
    start_app("kok", bit)
    hwnd = get_bs_hwnd(bit)
    game_width, game_height = get_game_dimension(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    to_kok_event(game_width, game_height, hwnd)
    kok_alchemy_event_tap(game_width, game_height, hwnd)
    kok_alchemy_tap(game_width, game_height, hwnd)
    time.sleep(30)


def ha_all_tap_pipeline(bit):
    start_app("ha", bit)
    hwnd = get_bs_hwnd(bit)
    game_width, game_height = get_game_dimension(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    ha_enter_game(game_width, game_height, hwnd)
    to_char_list(game_width, game_height, hwnd)
    all_tap(game_width, game_height, hwnd)


def qt_en_tank_pipepline(bit):
    start_app("qt", bit)
    hwnd = get_bs_hwnd(bit)
    game_width, game_height = get_game_dimension(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    enter_qt_main_screen(game_width, game_height, hwnd)
    enter_qt_event(game_width, game_height, hwnd)
    qt_energy_tank(game_width, game_height, hwnd)


def qt_tap_pipepline(bit):
    start_app("qt", bit)
    hwnd = get_bs_hwnd(bit)
    game_width, game_height = get_game_dimension(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    enter_qt_main_screen(game_width, game_height, hwnd)
    enter_qt_event(game_width, game_height, hwnd)
    qt_tap(game_width, game_height, hwnd)


def kok_wine_pipeline(bit):
    start_app("kok", bit)
    hwnd = get_bs_hwnd(bit)
    game_width, game_height = get_game_dimension(hwnd)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    to_kok_event(game_width, game_height, hwnd)
    kok_wine(game_width, game_height, hwnd)
    time.sleep(30)


if __name__ == '__main__':
    running = True
    while running:
        # qt_en_tank_pipeline(64)
        # kok_alchemy_pipeline(64)
        qt_tap_pipepline(64)
        ha_all_tap_pipeline(64)
        # start_app("kok", 64)
        time.sleep(1200)
