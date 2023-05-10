import cv2 as cv
import numpy as np
import os
from time import time, sleep, monotonic
from windowcapture import WindowCapture
from vision import Vision
from pyautogui import getWindowsWithTitle
from math import sqrt
from hsvfilter import HsvFilter
import sys
from bot import Bot
from random import randint, shuffle
import pytesseract as pts
import win32api
import win32con
import win32gui
from traceback import print_exc
import threading

if cv.ocl.haveOpenCL():
    cv.ocl.setUseOpenCL(True)
    print("OpenCL is enabled")
else:
    print("OpenCL is not available")

pts.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'


def draw_grid(img):
    for i in range(40, 1281, 80):
        cv.line(img, (i, 0), (i, 720), (255, 255, 0), 1)

    for i in range(0, 721, 80):
        cv.line(img, (0, i), (1280, i), (255, 255, 0), 1)

    for i in range(120, 1161, 80):
        cv.line(img, (i, 80), (i, 640), (255, 0, 0), 1)
    
    for i in range(80, 641, 80):
        cv.line(img, (120, i), (1160, i), (255, 0, 0), 1)

# fullscreen is made from 16 tiles, just at start there is half grid cell, 
# and at the end there is another half grid cell, this function draws it without the halves
def draw_grid_nohalf(img): 
    for i in range(0, 1040, 80):
        cv.line(img, (i, 0), (i, 560), (255, 0, 0), 1)
    
    for i in range(0, 560, 80):
        cv.line(img, (0, i), (1040, i), (255, 0, 0), 1)


hwnd = win32gui.FindWindowEx(None, None, None, 'NoxPlayer')

def c(x, y, delay=0.1):
    global hwnd
    screen_x, screen_y = win32gui.ClientToScreen(hwnd, (x, y))
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, screen_y * 0x10000 + screen_x)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, screen_y * 0x10000 + screen_x)
    sleep(delay)

def map_search():
    # open map
    c(1000, 70)
    # click every point around player randomly
    for clickpoint in bot.shuffle_map_points():
        c(clickpoint[0], clickpoint[1], 0.01)
    sleep(0.5)
    # close map
    c(1245, 70)


# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time = time()

# before capturing the window get it focused or else it will throw CreateCompatibleDC failed
# Window Name, i recommend NoxPlayer because the program was made and tested on it
wincap = WindowCapture('NoxPlayer')

image_paths = sys.argv[3].split("//") # selected from listed checkbox

# instances of each Vision class with loaded png
vision_instances = []

for path in image_paths:
    vision_instances.append(Vision("assets/" + path + ".png"))


bot = Bot()

# filter that allows program to only see black and white
blackwhite = HsvFilter(0, 0, 237, 0, 153, 255, 0, 0, 0, 0)


MAP_OPEN = False #1000 70, close 1245 70

cooldown = 5
last_search_time = 0

debug_mode = eval(sys.argv[1])

rectangles = []
enemy_present = False

while True:
    try:
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        # get image with only black and white elements
        proc_image = vision_instances[0].apply_hsv_filter(screenshot, blackwhite)

        # append each found element coordinates 
        for vision_instance in vision_instances:
            found = vision_instance.find(proc_image, 0.7)
            if len(found) == 0:
                rectangles = []
            else:
                rectangles = found

        if debug_mode == False:
            # get the noxplayer window to 0,0 coordinates (top left)
            getWindowsWithTitle("NoxPlayer")[0].moveTo(0, 0)
            print(rectangles)
            
            # kill enemies only if it found elements
            if len(rectangles) != 0 and len(rectangles[0]) != 0:
                enemy_present = True
                for enemy in rectangles:
                    closest = bot.kill(enemy)
                    c(closest[0], closest[1])
            
            # search if cooldown has passed and no enemies are present
            if monotonic() - last_search_time > cooldown and enemy_present == False:
                map_search()
                last_search_time = monotonic()
                
                # reset rectangles
                rectangles = []

            # reset enemy_present after killing enemies
            enemy_present = False
            
        else:
            for vision_instance in vision_instances:
                for i in range(len(rectangles)):
                    # show the region of interest that the program is searching in, with the drawn found elements
                    output_enemy = vision_instance.show_found(screenshot, rectangles[i])
                    draw_grid(output_enemy)
                    cv.imshow('debug_mode', output_enemy)
            draw_grid(proc_image)
            cv.imshow('processed_image', proc_image)
        
        # displays fps    
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # press 'q' with the output window focused to exit.
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    # catch errors because if ran from external application the window will immediately close without showing the error
    except Exception as e:
        print_exc()
        input("Press Enter to continue...")
        

print('Done.')