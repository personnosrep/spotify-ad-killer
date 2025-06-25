import win32gui
import win32process
import psutil
import os
import pyautogui as pg
import time
import ctypes

PROCNAME = "Spotify.exe"

user32 = ctypes.WinDLL('user32')

# add
exceptions = ['DDNet CLient']

def get_window_title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)

    # incase spotify freezes or something
    if length == 0:
        return ""

    #get the name
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value

def is_spotify_ad_window(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    
    # Get the process ID from window handle
    i, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        proc = psutil.Process(pid)
        if proc.name() != PROCNAME:
            return False
        
    except psutil.NoSuchProcess:
        return False

    # Check for ad keywords in the window title
    title = get_window_title(hwnd)

    #ads don't have a dash in their name
    return "-" not in title and title != "Spotify Free"

def open_and_run():
    # Don't wanna interrupt a match
    for exception in exceptions:
        if get_window_title(ctypes.windll.user32.GetForegroundWindow()) == exception:
            return False

    ctypes.windll.user32.BlockInput(True)

    # Kill existing Spotify
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()

    time.sleep(0.5)
    os.system("start spotify")

    # Wait until Spotify window is fully open
    
    def is_spotify_ready():
        hwnds = []

        def collect(hwnd, _):
            hwnds.append(hwnd)
        win32gui.EnumWindows(collect, None)

        for hwnd in hwnds:
            if win32gui.IsWindowVisible(hwnd):
                i, pid = win32process.GetWindowThreadProcessId(hwnd)
                
                try:
                    
                    proc = psutil.Process(pid)
                    if proc.name() == PROCNAME:
                        title = get_window_title(hwnd)
                        # Ads don't have a dash
                        if "-" in title:
                            return True
                        
                except psutil.NoSuchProcess:
                    continue
        return False

	#extra 2 seconds
    timeout = time.time() + 2
    while not is_spotify_ready():
        if time.time() > timeout:
            break
        time.sleep(0.2)

    pg.press('space')
    time.sleep(0.3)
    pg.hotkey('fn', 'f9')

    ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), 6)
    pg.click()
    ctypes.windll.user32.BlockInput(False)


def check_window(hwnd, extra):
    if is_spotify_ad_window(hwnd):
        open_and_run()

def main():
    while True:
        win32gui.EnumWindows(check_window, None)
        time.sleep(0.1)
