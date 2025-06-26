import win32gui
import win32process
import psutil
import os
import pyautogui as pg
import time
import ctypes

PROCNAME = "Spotify.exe"
user32 = ctypes.WinDLL('user32')
exceptions = ['DDNet Client']

def get_window_title(hwnd):
    if not win32gui.IsWindow(hwnd):
        return ""
    
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""

    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value

def is_spotify_ad_window(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False

    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        if proc.name() != PROCNAME:
            return False
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

    title = get_window_title(hwnd)
    return "-" not in title and title != "Spotify Free"

def open_and_run():
    # Don’t interrupt important stuff
    foreground = ctypes.windll.user32.GetForegroundWindow()
    fg_title = get_window_title(foreground)
    if fg_title in exceptions:
        return

    try:
        # Kill Spotify
        ctypes.windll.user32.BlockInput(True)
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == PROCNAME:
                proc.kill()

        time.sleep(0.5)
        os.system("start spotify")

        def is_spotify_ready():
            hwnds = []
            win32gui.EnumWindows(lambda hwnd, _: hwnds.append(hwnd), None)
            for hwnd in hwnds:
                if win32gui.IsWindowVisible(hwnd):
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        proc = psutil.Process(pid)
                        if proc.name() == PROCNAME:
                            title = get_window_title(hwnd)
                            if "-" in title:
                                return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            return False

        timeout = time.time() + 1
        while not is_spotify_ready():
            if time.time() > timeout:
                break
            time.sleep(0.2)

        pg.press('space')
        time.sleep(0.3)
        pg.press('nexttrack')

        ctypes.windll.user32.ShowWindow(foreground, 6)  # Minimize
        pg.click()

    finally:
        ctypes.windll.user32.BlockInput(False)

def check_window(hwnd, extra):
    if is_spotify_ad_window(hwnd):
        open_and_run()

def main():
    while True:
        win32gui.EnumWindows(check_window, None)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
