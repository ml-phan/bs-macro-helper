from bs_functions import *
from kok_events import *
from ha_events import *


def kok_alchemy_pipeline():
    start_app("kok", 64)
    hwnd = get_bs64_hwnd()
    game_width, game_height = get_game_dimension(hwnd)
    to_kok_event(game_width, game_height, hwnd)
    kok_alchemy_event_tap(game_width, game_height, hwnd)
    kok_tap(game_width, game_height, hwnd)
    time.sleep(30)


def ha_all_tap_pipeline():
    start_app("ha", 32)
    hwnd = get_bs32_hwnd()
    game_width, game_height = get_game_dimension(hwnd)
    ha_enter_game(game_width, game_height, hwnd)


if __name__ == '__main__':
    running = True
    while running:
        kok_alchemy_pipeline()
# ha_all_tap_pipeline()

