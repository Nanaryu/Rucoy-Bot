import pyautogui
import pydirectinput as pdi
from pymouse import PyMouse

pyautogui.getWindowsWithTitle("NoxPlayer")[0].moveTo(0, 0)

import win32api
import win32con
import win32gui

# Set the position to simulate a mouse click
x, y = 1000, 70

# Get the handle of the window to send the mouse click to
hwnd = win32gui.FindWindowEx(None, None, None, 'NoxPlayer')

# Convert the position to screen coordinates
screen_x, screen_y = win32gui.ClientToScreen(hwnd, (x, y))

# Simulate a left mouse button down event at the specified position
win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, screen_y * 0x10000 + screen_x)
win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, screen_y * 0x10000 + screen_x)

