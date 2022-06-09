import time

from pipelines import *


if __name__ == '__main__':
    running = True
    while running:
        # qt_en_tank_pipeline(64)
        kok_wine_pipeline(64)
        ha_all_tap_pipeline(64)
        # kok_alchemy_pipeline(64)

        # qt_tap_pipeline(64)
        kill_bs(64)
        time.sleep(1200)
