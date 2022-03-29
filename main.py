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


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print("Program - ID:", hex(hwnd))
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


timestamp = datetime.now().minute
bluestack_type = "Qt5154QWindowIcon"


def position_to_coordinate(a):
    x = 0.1972 + (a[0] - 1) * 0.3
    y = 0.1109 + (a[1] - 1) * 0.1313
    return x, y


def click(x, y):
    h_wnd = win32gui.FindWindow(None, "BlueStacks")
    l_param = win32api.MAKELONG(int(x), int(y))

    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)


def restart_bluestacks():
    os.system("TASKKILL /F /IM HD-Player.exe")
    time.sleep(5)
    os.startfile(r"C:\Program Files\BlueStacks_bgp64\Bluestacks.exe")


hwnd = win32gui.FindWindow(bluestack_type, "Bluestacks")
hwnd1 = ""
if not hwnd:
    print(hwnd)
    print("Starting Bluestacks")
    os.startfile(r"C:\Program Files\BlueStacks_bgp64\Bluestacks.exe")
    time.sleep(20)
    hwnd = win32gui.FindWindow(bluestack_type, "Bluestacks")
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
    print("Bluestacks is running", hwnd)
else:
    print("Bluestacks is running: ", hwnd)
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
print("Bluestacks is running with id", hwnd)
print("Bluestacks is running with game-screen id", hwnd1)
bs_screen = list(win32gui.GetWindowRect(hwnd))
game_screen = list(win32gui.GetWindowRect(hwnd1))
bs_width = bs_screen[2] - bs_screen[0]
bs_height = bs_screen[3] - bs_screen[1]
game_width = game_screen[2] - game_screen[0]
game_height = game_screen[3] - game_screen[1]
print("Bluestacks position: ", bs_screen)
print("Game screen position: ", game_screen)
print("Bluestacks width: ", bs_width)
print("Bluestacks height: ", bs_height)
print("Bluestacks height: ", game_width)
print("Bluestacks height: ", game_height)

kok = (2, 2)
kok_coor = position_to_coordinate(kok)

print("Percentage ", kok_coor[0], kok_coor[1])
print("Clicking at", kok_coor[0]*game_width, kok_coor[1]*game_height)
time.sleep(1)
print("Click to open KoK")
click(int(kok_coor[0]*game_width), int(kok_coor[1]*game_height))
time.sleep(60)
print("Click to close welcome screen")
click(int(0.5*game_width), int(0.05*game_height))
time.sleep(10)
print("Click to enter server")
click(int(0.5*game_width), int(0.87*game_height))
time.sleep(60)
print("Click to enter event")
click(int(0.45*game_width), int(0.62*game_height))

# hwnd2 = win32gui.FindWindow(None, "Ann - Discord")
# print(win32gui.GetWindowText(hwnd), "is type", win32gui.GetClassName(hwnd), "and has ID", hwnd)
# print(win32gui.GetWindowText(hwnd2), "is type", win32gui.GetClassName(hwnd2), "and has ID", hwnd2)

# os.system("TASKKILL /F /IM BstkSVC.exe")
# hwnd = win32gui.FindWindow(None, "Bluestacks")
# hwnd_1 = win32gui.FindWindowEx(hwnd, None, None, None)
# rect = list(win32gui.GetWindowRect(hwnd))
# game_screen = list(win32gui.GetWindowRect(hwnd_1))
# print(rect)
# print(game_screen)
# if not hwnd:
#     print(hwnd)
#     os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BlueStacks 5.lnk")
#     time.sleep(20)
#     print(hwnd)
# else:
#     print("Bluestacks is running: ", hwnd)

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
