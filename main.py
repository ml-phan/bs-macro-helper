# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
import time
from datetime import datetime
import win32api
import win32con
import win32gui

# def winEnumHandler( hwnd, ctx ):
#     if win32gui.IsWindowVisible( hwnd ):
#         print (hex(hwnd), win32gui.GetWindowText( hwnd ))
#
# win32gui.EnumWindows( winEnumHandler, None )

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

timestamp = datetime.now().minute


def position_to_coordinate(a, b):
    x = 0.1972 + (a - 1) * 0.3
    y = 0.1109 + (b - 1) * 0.1313
    return x, y


def click(x, y):
    h_wnd = win32gui.FindWindow(None, "BlueStacks")
    l_param = win32api.MAKELONG(x, y)

    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)


def restart_bluestacks():
    os.system("TASKKILL /F /IM HD-Player.exe")

    time.sleep(5)
    os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BlueStacks 5.lnk")


os.system("TASKKILL /F /IM BstkSVC.exe")
hwnd = win32gui.FindWindow(None, "Bluestacks")
# if not hwnd:
#     print(hwnd)
#     os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BlueStacks 5.lnk")
#     time.sleep(20)
#     print(hwnd)
# else:
#     print("Bluestacks is running: ", hwnd)
print(hwnd)

# print("Bluestacks position: ", rect)
# print("Button position: ", rect[2]-15, rect[3]-15)
# print("Game screen position: ", game_screen)
# print("Bluestacks width: ", width)
# print("Bluestacks height: ", height)
# print("Bluestacks height: ", game_width)
# print("Bluestacks height: ", game_height)
# while True:
#     time.sleep(2)
#     print("Clicking: ", rect[2]-15, rect[3]-15)
#     click(rect[2]-15, rect[3]-15)

# while True:
#     hwnd_1 = win32gui.FindWindowEx(hwnd, None, None, None)
#     rect = list(win32gui.GetWindowRect(hwnd))
#     game_screen = list(win32gui.GetWindowRect(hwnd_1))
#     print(rect)
#     print(game_screen)
#     game_width = game_screen[2] - game_screen[0]
#     game_height = game_screen[3] - game_screen[1]
#     time.sleep(2)
#     click(int(game_width*0.5), int(game_height*0.5))
#     time.sleep(2)