import os
import random
import time

import win32api
import win32con
import win32gui
import win32process
import wmi


bs_instance = []
bs_infos = []


def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd):
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

# os.remove("windows.txt")
# /win32gui.EnumWindows(winEnumHandler, None)


def click(x, y):
    h_wnd = win32gui.FindWindow(None, "BlueStacks")
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


def get_processes_command_line(txt):
    c = wmi.WMI()
    for process in c.Win32_Process():
        if isinstance(process.CommandLine, str) and txt in process.CommandLine:
            print("process.id", process.id)
            print("process.ProcessID", process.ProcessID)
            print("Command line", process.CommandLine)
            # for i in process.properties:
            #     print(i, getattr(process, i))


def find_bs_instances():
    win32gui.EnumWindows(winEnumHandler, "BlueStacks")
    get_bs_infos()


def kill_bs_2(bit):
    find_bs_instances()
    if bit == 32:
        for i in bs_infos:
            if "BlueStacks" in i[4] and "bgp64" not in i[4]:
                terminate_handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, i[1])
                win32api.TerminateProcess(terminate_handle, 0)
                print("Killed BlueStacks 32-bit")
    elif bit == 64:
        for i in bs_infos:
            if "BlueStacks" in i[4] and "bgp64" in i[4]:
                terminate_handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, i[1])
                win32api.TerminateProcess(terminate_handle, 0)
                print("Killed BlueStacks 64-bit")
    else:
        print("No BlueStacks is running")
    time.sleep(5)


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


def start_app(name, bit):
    if name.lower() == "kok" and bit == 32:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\King of Kinks - 32-bit.lnk")
    elif name.lower() == "kok" and bit == 64:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\King of Kinks - 64-bit.lnk")
    elif name.lower() == "qt" and bit == 32:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\Project QT - 32-bit.lnk")
    elif name.lower() == "qt" and bit == 64:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\Project QT - 64-bit.lnk")
    elif name.lower() == "ha" and bit == 32:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\Horny Arcana - 32-bit.lnk")
    elif name.lower() == "ha" and bit == 64:
        os.startfile(r"C:\Users\phanm\OneDrive\Desktop\Horny Arcana - 64-bit.lnk")
    else:
        pass
    time.sleep(40)
    find_bs_instances()
    time.sleep(10)


def to_kok_event(hwnd):
    game_width, game_height = get_game_dimension(hwnd)
    time.sleep(10)
    print("Click to close event splash")
    click(0.5 * game_width, 0.06 * game_height)
    time.sleep(5)
    print("Click to enter server")
    click(0.5 * game_width, 0.875 * game_height)
    time.sleep(5)
    print("Click to close Mihime sale")
    click(0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    click(0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    click(0.9055 * game_width, 0.05125 * game_height)
    time.sleep(2)
    print("Click to close return to Main")
    click(0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
    click(0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
    click(0.1 * game_width, 0.95 * game_height)
    time.sleep(2)
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
    print("Starting Tap")
    while i < 600:
        time.sleep(5)

        random_width = random.uniform(-0.4, 0.4)
        random_height = random.uniform(-0.14, 0.14)
        click((0.5+random_width) * game_width, (0.155 + random_height) * game_height)
        i += 1
        if i % 100 == 0:
            print("Tap times:", i)


def restart_bluestacks():
    pid = win32gui.FindWindow(None, "BlueStacks")
    if pid and pid != "985696":
        # win32gui.PostMessage(pid, win32con.WM_CLOSE, 0, 0)
        t, p = win32process.GetWindowThreadProcessId(pid)
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        win32api.TerminateProcess(handle, 0)
    time.sleep(5)
    os.startfile(r"C:\Users\phanm\OneDrive\Desktop\King of Kinks - 64-bit.lnk")
    time.sleep(50)


def kok_alchemy_pipeline():
    kill_bs_2(64)
    start_app("kok", 64)
    # restart_bluestacks()
    pid = 0
    for i in bs_infos:
        if "bgp64" in i[4]:
            pid = i[0]
    pid2 = win32gui.FindWindow(None, "BlueStacks")
    time.sleep(1)
    print("ID from bs_infos:", pid)
    print("ID from find windows:", pid2)
    # to_kok_event(pid)
    # kok_alchemy_event_tap(pid)
    # kok_tap(pid)
    time.sleep(30)



if __name__ == '__main__':
    # win32gui.EnumWindows(winEnumHandler, None)
    running = False
    # time.sleep(2)
    # restart_bluestacks()
    bs_instance = []
    bs_infos = []
    kok_alchemy_pipeline()
    times = 1
    while running:
        print("Starting run", times)
        kok_alchemy_pipeline()
        print("Finished run", times)
        times += 1

