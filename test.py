import win32api
import win32con
import win32gui
import win32process
import wmi

bs_instance = []


def winEnumHandler(hwnd, pname):
    if win32gui.IsWindowVisible(hwnd) and pname in win32gui.GetWindowText(hwnd):
        print("Program - ID:", hwnd)
        print("          WindowText:", win32gui.GetWindowText(hwnd))
        print("          ClassName:", win32gui.GetClassName(hwnd))
        bs_instance.append(hwnd)


def get_bs_instance():
    pinfo = []
    for hwnd in bs_instance:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
        handle2 = win32api.OpenProcess(1, False, pid)
        path = win32process.GetModuleFileNameEx(handle, 0)
        # path2 = win32process.GetModuleFileNameEx(handle2, 0)
        pinfo.append([hwnd, pid, handle, handle2, path])
    return pinfo


def get_processes_command_line(txt):
    c = wmi.WMI()
    for process in c.Win32_Process():
        if isinstance(process.CommandLine, str) and txt in process.CommandLine:
            print("process.id", process.id)
            print("process.ProcessID", process.ProcessID)
            for i in process.properties:
                print(i, getattr(process, i))


# hld = win32gui.FindWindow(None, i for "Notepad" in i)
# print(hld)
win32gui.EnumWindows(winEnumHandler, "BlueStacks")
infos = get_bs_instance()
print(type(infos[0][0]), infos[0][0])
print(type(infos[0][1]), infos[0][1])
print(type(infos[0][2]), infos[0][2])
print(type(infos[0][3]), infos[0][3])
# win32process.TerminateProcess(infos[0][2], 0)
get_processes_command_line("BlueStacks")
