import os
import time

import win32api
import win32con
import win32gui
import win32process
import wmi

bs_instance = []
bs_infos = []


def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd)\
            and "Blue" in win32gui.GetClassName(hwnd):
        print("Program - ID:", hwnd)
        print("          WindowText:", win32gui.GetWindowText(hwnd))
        print("          ClassName:", win32gui.GetClassName(hwnd))
        print("Class Name Type    :", type(win32gui.GetClassName(hwnd)))
        bs_instance.append(hwnd)


# Return 5 values
# 1 - assigned pyhandle
# 2 - process ID
# 3 - process handle (to get executable path)
# 4 - parent process handle (to force close)
# 5 - process executable path
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


# def kill_bs(bit):
#
#     if bit == 32:
#
#     elif bit == 64:
#         for i in bs_infos:
#             if "bgp64" in i[4]:
#                 win32process.TerminateProcess(i[3], 0)
#                 print("Killed BlueStacks 64-bit")
#     else:
#         print("No BlueStacks is running")

pid = win32gui.FindWindow(None, "BlueStacks")
print(pid)
find_bs_instances()
print(bs_infos)

# os.system("taskkill /f C:\Program Files\BlueStacks_bgp64\Bluestacks.exe")
# win32process.TerminateProcess(infos[0][2], 0)
# get_processes_command_line("HD-Player")
