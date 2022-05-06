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


def get_all_bs():
    bs_hwnd.clear()
    win32gui.EnumWindows(winEnumHandler, "BlueStacks")


def get_pname(pname):
    bs_hwnd.clear()
    chrome.clear()
    win32gui.EnumWindows(winEnumHandler, pname)


def winEnumHandler(hwnd, pname):
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


# def winEnumHandler(hwnd, pname):
#     if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd) and \
#             ("Qt5154" in win32gui.GetClassName(hwnd) or "Hwnd" in win32gui.GetClassName(hwnd)) :
#         process_id = get_process_id(hwnd)
#         process = psutil.Process(process_id)
#         path = process.exe()
#         cmdline = process.cmdline()
#         if "Blue" in pname:
#             bs_hwnd.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})
#         elif "Chrome" in pname:
#             chrome.append({"hwnd": hwnd, "pid": process_id, "path": path, "cmd": cmdline})


def get_process_id(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def get_process(hwnd):
    return psutil.Process(get_process_id(hwnd))


def get_exe_path(hwnd):
    return get_process(hwnd).exe()


def get_command_line(hwnd):
    return get_process(hwnd).cmdline()


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


def get_bs64_hwnd():
    get_all_bs()
    for i in bs_hwnd:
        if "64" in i["path"]:
            print("BlueStacks 64-bit is running with ID", i["hwnd"])
            return i["hwnd"]
        else:
            print("No BlueStacks 64-bit is running")


def get_bs32_hwnd():
    get_all_bs()
    for i in bs_hwnd:
        if "64" not in i["path"]:
            print("BlueStacks 32-bit is running with ID", i["hwnd"])
            return i["hwnd"]
        else:
            print("No BlueStacks 32-bit is running")


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


def kill_bs64():
    get_all_bs()
    for i in bs_hwnd:
        if "64" in i["path"]:
            get_process(i["hwnd"]).kill()


def kill_bs32():
    get_all_bs()
    for i in bs_hwnd:
        if "64" not in i["path"]:
            get_process(i["hwnd"]).kill()


def start_app(name, bit):
    qt32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Project QT\",\"app_url\":\"\",\"app_pkg\":\"com.ignite.qt\"}"'
    qt64 = r'"C:\Program Files\BlueStacks_bgp64\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Project QT\",\"app_url\":\"\",\"app_pkg\":\"com.ignite.qt\"}"'
    kok32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
            r'-json "{\"app_icon_url\":\"\",\"app_name\":\"King of Kinks\",\"app_url\":\"\",\"app_pkg\":\"com.hmagic.kingofkinks\"}"'
    kok64 = r'"C:\Program Files\BlueStacks_bgp64\HD-RunApp.exe" ' \
            r'-json "{\"app_icon_url\":\"\",\"app_name\":\"King of Kinks\",\"app_url\":\"\",\"app_pkg\":\"com.hmagic.kingofkinks\"}"'
    ha32 = r'"C:\Program Files\BlueStacks\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Horny Arcana\",\"app_url\":\"\",\"app_pkg\":\"com.superhgame.ha.nutaku\"}"'
    ha64 = r'"C:\Program Files\BlueStacks_bgp64\HD-RunApp.exe" ' \
           r'-json "{\"app_icon_url\":\"\",\"app_name\":\"Horny Arcana\",\"app_url\":\"\",\"app_pkg\":\"com.superhgame.ha.nutaku\"}"'
    time.sleep(1)
    if bit == 32:
        kill_bs(bit)
        if name.lower() == "kok":
            subprocess.Popen(kok32)
        elif name.lower() == "qt":
            subprocess.Popen(qt32)
        elif name.lower() == "ha":
            subprocess.Popen(ha32)
        else:
            print("Invalid game name")
    elif bit == 64:
        kill_bs(bit)
        if name.lower() == "kok":
            subprocess.Popen(kok64)
        elif name.lower() == "qt":
            subprocess.Popen(qt64)
        elif name.lower() == "ha":
            subprocess.Popen(ha64)
        else:
            print("Invalid bit")
    time.sleep(30)
    time.sleep(60)
    get_all_bs()
    print(bs_hwnd)
    time.sleep(10)


def click(h_wnd, x, y):
    l_param = win32api.MAKELONG(int(x), int(y))
    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)


def click_no_ex(h_wnd, x, y):
    l_param = win32api.MAKELONG(int(x), int(y))
    win32gui.SendMessage(h_wnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.SendMessage(h_wnd, win32con.WM_LBUTTONUP, None, l_param)


def click2(h_wnd, x, y):
    l_param = win32api.MAKELONG(int(x), int(y))
    h_wnd1 = win32gui.FindWindowEx(h_wnd, None, None, None)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, l_param)
    win32gui.PostMessage(h_wnd1, win32con.WM_LBUTTONUP, None, l_param)


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
