import datetime
import os
import subprocess
import time

import psutil
import win32api
import win32con
import win32gui
import win32process

bs_hwnd = []
chrome = []


# return handler of all bs instances
def get_all_bs():
    bs_hwnd.clear()
    win32gui.EnumWindows(win_enum_handler, "BlueStacks")


# Find all bs instance handles
def win_enum_handler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd) and \
            ("Qt5154" in win32gui.GetClassName(hwnd) or "Hwnd" in win32gui.GetClassName(hwnd) or
             "Chrome" in win32gui.GetClassName(hwnd)):
        process_id = get_process_id(hwnd)
        process = psutil.Process(process_id)
        path = process.exe()
        cmdline = process.cmdline()
        if "Blue" in pname and ("Qt5154" in win32gui.GetClassName(hwnd) or
                                "Hwnd" in win32gui.GetClassName(hwnd)):
            bs_hwnd.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})
        elif "Chrome" in pname:
            chrome.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})


# Get the process ID of a given handle "hwnd"
def get_process_id(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


# Get the process from process ID
def get_process(hwnd):
    return psutil.Process(get_process_id(hwnd))


# Get the executable path of a bs instance with handle "hwnd"
def get_exe_path(hwnd):
    return get_process(hwnd).exe()


# Get the command line of a bs instance with the handle "hwnd"  to parse for bit mode
def get_command_line(hwnd):
    return get_process(hwnd).cmdline()


# Get handles of all bs instance, either 32-bit or 64-bit
def get_bs_hwnd(bit):
    get_all_bs()
    for i in bs_hwnd:
        if str(bit) == "64" and any(str(64) in s for s in i["cmd"]):
            print("BlueStacks 64-bit is running with ID", i["hwnd"])
            return i["hwnd"]
        elif str(bit) == "32" and all(str(64) not in s for s in i["cmd"]):
            print("BlueStacks 32-bit is running with ID", i["hwnd"])
            return i["hwnd"]
        else:
            print("Wrong bit number")


# Shutdown all bs instances
# bit: 32-bit or 64-bit bs instances
def kill_bs(bit):
    get_all_bs()
    for i in bs_hwnd:
        if bit == 64 and any(str(64) in s for s in i["cmd"]):
            print("Killing BlueStacks 64-bit with ID", i["hwnd"])
            get_process(i["hwnd"]).kill()
        elif bit == 32 and all(str(64) not in s for s in i["cmd"]):
            print("Killing BlueStacks 32-bit with ID", i["hwnd"])
            get_process(i["hwnd"]).kill()
        else:
            print("Wrong bit number ?")


# Start a program that is installed within a bs instance
# name : short name of the program
# bit : start bs in either 32-bit or 64-bit mode
def start_app(name, bit):
    cc32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Clash of Clans\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.supercell.clashofclans\"}"'
    cc64 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Clash of Clans\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.supercell.clashofclans\"}"'
    sl32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Soul Land\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.soullandrl.gp\"}"'
    sl64 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Soul Land\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.soullandrl.gp\"}"'
    ic32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"ILLUSION CONNECT\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.superprism.illusion\"}"'
    ic64 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"ILLUSION CONNECT\",\"app_url\":\"\",' \
           r'\"app_pkg\":\"com.superprism.illusion\"}"'
    time.sleep(1)
    if bit == 32:
        kill_bs(bit)
        if name.lower() == "sl":
            subprocess.Popen(sl32)
        elif name.lower() == "cc":
            subprocess.Popen(cc32)
        elif name.lower() == "ic":
            subprocess.Popen(ic32)
        else:
            print("Invalid game name")
    elif bit == 64:
        kill_bs(bit)
        if name.lower() == "sl":
            subprocess.Popen(sl64)
        elif name.lower() == "cc":
            subprocess.Popen(cc64)
        elif name.lower() == "ic":
            subprocess.Popen(ic64)
        else:
            print("Invalid bit")
    time.sleep(10)
    hwnd = get_bs_hwnd(bit)
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    time.sleep(60)
    get_all_bs()
    print(bs_hwnd)
    return hwnd
    time.sleep(10)


# Send a left-click to a game windows in bs
# hwnd : handle of the bs instance
# x, y: position of mouse click in integer
# Out the timestamp of each click to console
def click(hwnd, x, y):
    l_param = win32api.MAKELONG(int(x), int(y))
    h_wnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)
    now = datetime.datetime.now().replace(microsecond=0)
    print(now)


# return the game resolution of the game screen:
# game_width, game_height in integer
def get_game_dimension(hwnd):
    print("Getting Resolution from hwnd", hwnd)
    hwnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
    game_screen = list(win32gui.GetWindowRect(hwnd1))
    game_width = game_screen[2] - game_screen[0]
    game_height = game_screen[3] - game_screen[1]
    print("Game screen position: ", game_screen)
    print("Game screen height: ", game_width)
    print("Game screen height: ", game_height)
    return game_width, game_height
