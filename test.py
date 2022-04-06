import pprint

import win32gui

import bs_functions
from bs_functions import *

bs_hwnd = []
chrome = []


def get_pname(pname):
    bs_hwnd.clear()
    chrome.clear()
    win32gui.EnumWindows(winEnumHandler, pname)


def winEnumHandler2(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print("Program - ID:", hwnd)
        print("        - WindowText:", win32gui.GetWindowText(hwnd))
        print("        - ClassName:", win32gui.GetClassName(hwnd))


def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd) and \
            ("Qt5154" in win32gui.GetClassName(hwnd) or "Hwnd" in win32gui.GetClassName(hwnd) or
             "Chrome" in win32gui.GetClassName(hwnd)):
        print("Program - ID:", hwnd)
        print("          WindowText:", win32gui.GetWindowText(hwnd))
        print("          ClassName:", win32gui.GetClassName(hwnd))
        process_id = get_process_id(hwnd)
        process = psutil.Process(process_id)
        path = process.exe()
        cmdline = process.cmdline()
        # print("path", path)
        # print("cmd", cmdline)
        if "Blue" in pname and ("Qt5154" in win32gui.GetClassName(hwnd) or
                                      "Hwnd" in win32gui.GetClassName(hwnd)):
            bs_hwnd.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})
        elif "Chrome" in pname:
            chrome.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})

# win32gui.EnumWindows(winEnumHandler2, None)
get_all_bs()
# pprint.pprint(bs_functions.bs_hwnd[0]["hwnd"])
pprint.pprint(bs_functions.bs_hwnd)
hwnd = bs_functions.bs_hwnd[0]["hwnd"]
hwnd1 = win32gui.FindWindowEx(bs_functions.bs_hwnd[0]["hwnd"], None, None, None)
print(hwnd)
print(hwnd1)
print(win32gui.GetWindowText(hwnd1))
child_handles = []
def all_ok(hwnd, param):
    child_handles.append(hwnd)

win32gui.EnumChildWindows(hwnd, all_ok, None)
print(win32gui.GetWindowText(722852))
print(child_handles)
# print(get_game_dimension(hwnd))
# print(get_game_dimension(hwnd1))
for i in range(10):
    handle = hwnd
    time.sleep(2)
    print("CLicking on hwnd", handle)
    click2(handle, 50, 50)



# get_pname("BlueStacks")
# pprint.pprint(bs_hwnd)
# pprint.pprint(chrome)
# variable = get_game_dimension(133168)
# print(variable)
# if chrome:
#     hwnd = chrome[0]["hwnd"]
#     win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
#                       win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#     win32gui.SetWindowPos(chrome[0]["hwnd"], win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
#                           win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
