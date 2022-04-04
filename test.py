import win32gui

from bs_functions import *

bs_hwnd = []
chrome = []


def get_pname(pname):
    bs_hwnd.clear()
    chrome.clear()
    win32gui.EnumWindows(winEnumHandler, pname)


def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd):
        print("Program - ID:", hwnd)
        print("          WindowText:", win32gui.GetWindowText(hwnd))
        print("          ClassName:", win32gui.GetClassName(hwnd))
        process_id = get_process_id(hwnd)
        process = psutil.Process(process_id)
        path = process.exe()
        cmdline = process.cmdline()
        print("path", path)
        print("cmd", cmdline)
        if "BlueStacks" in pname:
            bs_hwnd.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})
        elif "Chrome" in pname:
            chrome.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})


get_pname("BlueStacks")
print(bs_hwnd)
variable = get_game_dimension(133168)
# print(variable)
# if chrome:
#     hwnd = chrome[0]["hwnd"]
#     win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
#                       win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#     win32gui.SetWindowPos(chrome[0]["hwnd"], win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
#                           win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
