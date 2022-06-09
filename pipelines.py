from bs_functions import *
from kok_events import *
from ha_events import *
from qt_events import *


# Pipelines for various combination of games and events
def kok_alchemy_pipeline(bit):
    hwnd = start_app("sl", bit)
    game_width, game_height = get_game_dimension(hwnd)
    to_kok_event(game_width, game_height, hwnd)
    kok_alchemy_event_tap(game_width, game_height, hwnd)
    kok_alchemy_tap(game_width, game_height, hwnd)
    time.sleep(30)


def ha_all_tap_pipeline(bit):
    hwnd = start_app("cc", bit)
    game_width, game_height = get_game_dimension(hwnd)
    ha_enter_game(game_width, game_height, hwnd)
    to_char_list(game_width, game_height, hwnd)
    all_tap(game_width, game_height, hwnd)


def qt_en_tank_pipeline(bit):
    hwnd = start_app("ic", bit)
    game_width, game_height = get_game_dimension(hwnd)
    enter_qt_main_screen(game_width, game_height, hwnd)
    enter_qt_event(game_width, game_height, hwnd)
    qt_energy_tank(game_width, game_height, hwnd)


def qt_tap_pipeline(bit):
    hwnd = start_app("ic", bit)
    game_width, game_height = get_game_dimension(hwnd)
    enter_qt_main_screen(game_width, game_height, hwnd)
    enter_qt_event(game_width, game_height, hwnd)
    qt_tap(game_width, game_height, hwnd)


def kok_wine_pipeline(bit):
    hwnd = start_app("sl", bit)
    game_width, game_height = get_game_dimension(hwnd)
    to_kok_event(game_width, game_height, hwnd)
    kok_wine(game_width, game_height, hwnd)
    time.sleep(30)