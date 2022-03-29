import os
import random
import time

import win32api
import win32con
import win32gui
import win32process


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == "BlueStacks":
        print("Program - ID:", hwnd)
        print("        - WindowText:", win32gui.GetWindowText(hwnd))
        print("        - ClassName:", win32gui.GetClassName(hwnd))
    # with open("windows.txt", "a") as f:
    #     prog_id = "Program - ID: " + str(hex(hwnd))
    #     windowtext = "        - WindowText: " + str(win32gui.GetWindowText(hwnd))
    #     classname = "        - ClassName: " + str(win32gui.GetClassName(hwnd))
    #     str1 = " this is a test line"
    #     f.write(prog_id)
    #     f.write(windowtext)
    #     f.write(classname)

# os.remove("windows.txt")
# win32gui.EnumWindows(winEnumHandler, None)


def click(x, y):
    h_wnd = win32gui.FindWindow(None, "BlueStacks")
    l_param = win32api.MAKELONG(int(x), int(y))

    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)

# while True:
#     time.sleep(2)
#     click(200, 200)
# def restart_bluestacks():
#     os.system("TASKKILL /F /IM Bluestacks.exe")
#     time.sleep(5)
#     os.startfile(r"C:\Program Files\BlueStacks_bgp64\Bluestacks.exe")
# restart_bluestacks()


def get_bs_dimension(hwnd):
    bs_screen = list(win32gui.GetWindowRect(hwnd))
    bs_width = bs_screen[2] - bs_screen[0]
    bs_height = bs_screen[3] - bs_screen[1]
    return bs_width, bs_height


def print_bs_info(hwnd):
    bs_type = win32gui.GetClassName(hwnd)
    print("Bluestacks 4.0 is running with id", hwnd)
    print("Bluestacks 4.0 is of type", bs_type)
    bs_screen = list(win32gui.GetWindowRect(hwnd))
    bs_width = bs_screen[2] - bs_screen[0]
    bs_height = bs_screen[3] - bs_screen[1]
    print("Bluestacks position: ", bs_screen)
    print("Bluestacks width: ", bs_width)
    print("Bluestacks height: ", bs_height)


def get_game_dimension(hwnd):
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
    game_screen = list(win32gui.GetWindowRect(hwnd1))
    game_width = game_screen[2] - game_screen[0]
    game_height = game_screen[3] - game_screen[1]
    print("Game screen position: ", game_screen)
    print("Game screen height: ", game_width)
    print("Game screen height: ", game_height)
    return game_width, game_height


def print_game_info(hwnd):
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
    game_screen = list(win32gui.GetWindowRect(hwnd1))
    game_type = win32gui.GetClassName(hwnd1)
    print("Game Screen 4.0 is running with id", hwnd1)
    print("Game screen 4.0 is of type", game_type)
    game_width, game_height = get_game_dimension(hwnd1)
    print("Game screen position: ", game_screen)
    print("Game screen height: ", game_width)
    print("Game screen height: ", game_height)


def restart_bluestacks():
    pid = win32gui.FindWindow(None, "BlueStacks")
    if pid and pid != "985696":
        # win32gui.PostMessage(pid, win32con.WM_CLOSE, 0, 0)
        t, p = win32process.GetWindowThreadProcessId(pid)
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        win32api.TerminateProcess(handle, 0)
    time.sleep(5)
    os.startfile(r"C:\Users\phanm\OneDrive\Desktop\King of Kinks.lnk")
    time.sleep(50)


def to_kok_event(hwnd):
    game_width, game_height = get_game_dimension(hwnd)
    time.sleep(10)
    print("Click to close event splash")
    click(0.5 * game_width, 0.06 * game_height)
    time.sleep(5)
    print("Click to enter server")
    click(0.5 * game_width, 0.875 * game_height)
    time.sleep(10)
    print("Click to enter KoK event")
    click(0.455 * game_width, 0.625 * game_height)


def kok_alchemy_event_tap(hwnd):
    game_width, game_height = get_game_dimension(hwnd)
    time.sleep(10)
    print("Click to open Alchemy Urn")
    click(0.1222 * game_width, 0.8562 * game_height)
    time.sleep(5)
    print("Click to claim Alchemy")
    click(0.6777 * game_width, 0.7437 * game_height)
    time.sleep(5)
    print("Click to close Alchemy claim notice")
    click(0.5 * game_width, 0.22 * game_height)


def kok_tap(hwnd):
    game_width, game_height = get_game_dimension(hwnd)
    i = 0
    while i < 600:
        time.sleep(5)
        print("Click to claim Alchemy")
        random_width = random.uniform(-0.4, 0.4)
        random_height = random.uniform(-0.14, 0.14)
        click((0.5+random_width) * game_width, (0.155 + random_height) * game_height)
        i += 1


def kok_alchemy_pipeline():
    restart_bluestacks()
    pid = win32gui.FindWindow(None, "BlueStacks")
    to_kok_event(pid)
    kok_alchemy_event_tap(pid)
    kok_tap(pid)
    time.sleep(30)


if __name__ == '__main__':
    # win32gui.EnumWindows(winEnumHandler, None)
    time.sleep(2)
    # restart_bluestacks()
    i = 1
    while True:
        print("Starting run", i)
        kok_alchemy_pipeline()
        print("Finished run", i)
        i += 1

