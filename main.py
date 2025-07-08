# UPDATED SCRIPT
# Mutes Spotify during ads instead of restarting

import win32gui
import win32process
import psutil
import time
import ctypes
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
import comtypes

PROCNAME = "Spotify.exe"
user32 = ctypes.WinDLL('user32')
exceptions = []
running = True

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
		i, pid = win32process.GetWindowThreadProcessId(hwnd)
		proc = psutil.Process(pid)
		if proc.name() != PROCNAME:
			return False
		
	except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
		return False

	title = get_window_title(hwnd)
	return "-" not in title and title != "Spotify Free"

def get_spotify_sessions():
	sessions = AudioUtilities.GetAllSessions()
	return [s for s in sessions if s.Process and s.Process.name() == PROCNAME]

def mute_spotify(mute=True):

	for session in get_spotify_sessions():
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		volume.SetMute(mute, None)

def check_window(hwnd, extra):
	global was_muted

	if is_spotify_ad_window(hwnd):
		if not was_muted:
			mute_spotify(True)
			was_muted = True
	else:
		if was_muted:
			mute_spotify(False)
			was_muted = False

def get_hwnd():
	hwnds = []
	win32gui.EnumWindows(lambda hwnd, _: hwnds.append(hwnd), None)
	for hwnd in hwnds:
		if win32gui.IsWindowVisible(hwnd):
			try:
				_, pid = win32process.GetWindowThreadProcessId(hwnd)
				proc = psutil.Process(pid)
				if proc.name() == PROCNAME:
					title = get_window_title(hwnd)
					if title:  # skip empty titles
						return hwnd
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				continue
	return None


def main():
	import comtypes
	comtypes.CoInitialize()

	global was_muted
	was_muted = False

	while True:
		if not running:
			continue

		hwnd = get_hwnd()
		if hwnd:
			if is_spotify_ad_window(hwnd):
				if not was_muted:
					mute_spotify(True)
					was_muted = True
					print("Muted")
			else:
				if was_muted:
					mute_spotify(False)
					was_muted = False
					print("Unmuted")

		time.sleep(0.3)


if __name__ == "__main__":
	main()
