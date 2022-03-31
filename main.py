
import os
import sys
import time
from datetime import datetime
import win32api
import win32con
import win32gui
import win32process
import psutil
import pprint

bs_instance = []
bs_infos = []

def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd) and \
            "WindowIcon" in win32gui.GetClassName(hwnd):
        print("Program - ID:", hwnd)
        print("          WindowText:", win32gui.GetWindowText(hwnd))
        print("          ClassName:", win32gui.GetClassName(hwnd))
        bs_instance.append(hwnd)
    # with open("windows.txt", "a") as f:
    #     prog_id = "Program - ID: " + str(hex(hwnd))
    #     windowtext = "        - WindowText: " + str(win32gui.GetWindowText(hwnd))
    #     classname = "        - ClassName: " + str(win32gui.GetClassName(hwnd))
    #     str1 = " this is a test line"
    #     f.write(prog_id)
    #     f.write(windowtext)
    #     f.write(classname)


def click(h_wnd, x, y):
    l_param = win32api.MAKELONG(int(x), int(y))
    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)


def get_bs_infos():
    for hwnd in bs_instance:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
        handle2 = win32api.OpenProcess(1, False, pid)
        path = win32process.GetModuleFileNameEx(handle, 0)
        bs_infos.append([hwnd, pid, handle, handle2, path])
    return bs_infos
# os.remove("windows.txt")


def get_process_id(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def get_exe_path(hwnd):
    pass


win32gui.EnumWindows(winEnumHandler, "Blue")
get_bs_infos()
pprint.pprint(bs_infos)
print(bs_instance)
for i in bs_instance:
    pid = get_process_id(i)
    p = psutil.Process(pid)
    print("process id:", pid)
    print("num_handles:", p.num_handles())




# hwnd = win32gui.FindWindow(None, "BlueStacks")
# print(hwnd)