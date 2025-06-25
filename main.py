import win32gui
import win32process
import psutil
import os
import pyautogui as pg
import time
import ctypes

PROCNAME = "Spotify.exe"

user32 = ctypes.WinDLL('user32')

# add games and such so you don't get interrupted during a match
exceptions = []

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

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            proc.kill()

    # start spotify and skip so it doesn't restart the same song
    time.sleep(0.2)
    os.system("start spotify")
    time.sleep(2)
    pg.press('space')
    time.sleep(0.3)
    pg.hotkey('fn', 'f9')

    #minimize
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
