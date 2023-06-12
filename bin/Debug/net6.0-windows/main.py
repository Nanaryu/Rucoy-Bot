import cv2 as cv
import os
from time import time, sleep, monotonic
from windowcapture import WindowCapture
from vision import Vision
from pyautogui import getWindowsWithTitle, locateOnScreen
from math import sqrt
from hsvfilter import HsvFilter
import sys
from bot_func import kill, exhaustion_check, shuffle_map_points
from random import randint, shuffle
import pytesseract as pts
import win32api
import win32con
import win32gui
from traceback import print_exc
from mobcalc import train

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
    for clickpoint in shuffle_map_points():
        c(clickpoint[0], clickpoint[1], 0.01)
    sleep(0.5)
    # close map
    c(1245, 70)

def self_sustain(statinterval, player_class):
    if statinterval > 10000:
        statinterval = 0
        if player_class == "Melee":
            c(1245, 70)
            c(230, 166, 0.5)
            sleep(1)
            lvlarea = proc_image[200-32-5:245-32+5,1100:1205]
            lvlval = pts.image_to_string(lvlarea)
            print("pts result: ", lvlval)
            lvlval = int(lvlval)
            statarea = proc_image[300-32-5:345-32+5,1100:1205]
            statval = pts.image_to_string(statarea)
            statval = int(statval)
            print(player_class, ": ", statval, end="")
            print(train(lvlval, statval))
            c(1245, 70)
        elif player_class == "Magic":
            c(1245, 70)
            c(230, 166, 0.5)
            lvlarea = proc_image[200-32-5:245-32+5,1100:1205]
            lvlval = pts.image_to_string(lvlarea)
            lvlval = int(lvlval)
            statarea = proc_image[500-32-5:545-32+5,1100:1205]
            statval = pts.image_to_string(statarea)
            statval = int(statval)
            print(player_class, ": ", statval, end="")
            print(train(lvlval, statval))
            c(1245, 70)
        elif player_class == "Distance":
            c(1245, 70)
            c(230, 166, 0.5)
            lvlarea = proc_image[200-32-5:245-32+5,1100:1205]
            lvlval = pts.image_to_string(lvlarea)
            lvlval = int(lvlval)
            statarea = proc_image[400-32-5:445-32+5,1100:1205]
            statval = pts.image_to_string(statarea)
            statval = int(statval)
            print(player_class, ": ", statval, end="")
            print(train(lvlval, statval))
            c(1245, 70)



# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time = time()

# before capturing the window get it focused or else it will throw CreateCompatibleDC failed
# Window Name, i recommend NoxPlayer because the program was made and tested on it
emulator = str(sys.argv[4])
wincap = WindowCapture(emulator)

image_paths = sys.argv[3].split("//") # selected from listed checkbox

# instances of each Vision class with loaded png

mob_instance = Vision(os.path.join('..', '..', 'assets', image_paths[0] + '.png'))



# filter that allows program to only see black and white
blackwhite = HsvFilter(0, 0, 237, 0, 153, 255, 0, 0, 0, 0)

cooldown = 2
last_search_time = 0

debug_mode = eval(sys.argv[1])
automphp = eval(sys.argv[6])
player_class = str(sys.argv[5])

rectangles = []
enemy_present = False
exhausted = cv.imread(os.path.join('..', '..', 'assets', 'exhausted4.png'))
getWindowsWithTitle(emulator)[0].moveTo(0, 0)

statval = 5
lvlval = 1
statarea = []

statinterval = 10001
searchinterval = 0
while True:
    try:
        #statinterval += 1
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        # get image with only black and white elements
        proc_image = mob_instance.apply_hsv_filter(screenshot, blackwhite)
        
        # mob exhaustion
        exhausted_check = screenshot[489:521, 278:1007]
        ex_status = exhaustion_check(exhausted_check)
        if ex_status == True:
            if player_class == "Melee":
                c(1217, 450, 0.5)
                c(1100, 450, 0.5)
                c(60, 450, 0.7)
                c(60, 450, 0.7)
                c(1217, 450, 0.5)
                c(1100, 450, 0.5)
                sleep(5)
            elif player_class == "Distance":
                c(1217, 566, 0.5)
                c(1100, 566, 0.5)
                c(60, 450, 0.7)
                c(60, 450, 0.7)
                c(1217, 566, 0.5)
                c(1100, 566, 0.5)
                sleep(5)
            elif player_class == "Magic":
                c(1217, 690, 0.5)
                c(1100, 690, 0.5)
                c(60, 450, 0.7)
                c(640, 385, 0.7)
                c(60, 450, 0.7)
                c(640, 385, 0.7)
                c(1217, 690, 0.5)
                c(1100, 690, 0.5)
                sleep(5)
        
        # for auto hp and auto mana
        if automphp == True:
            automphp_check = screenshot[0:80, 0:440]
            mana_pixel = automphp_check[40, 220]
            hp_pixel = automphp_check[5, 350]
            if all(mana_pixel == (105, 105, 105)):
                c(65, 580, 2)
            if all(hp_pixel == (105, 105, 105)):
                c(65, 700, 2)
        

        # append each found element coordinates 
        found = mob_instance.find(proc_image, 0.65)
        if len(found) == 0:
            rectangles = []
        else:
            rectangles = found

        # get the noxplayer window to 0,0 coordinates (top left)
        getWindowsWithTitle(emulator)[0].moveTo(0, 0)
        
        if debug_mode == False:    
            # kill enemies only if it found elements
            if len(rectangles) != 0 and len(rectangles[0]) != 0:
                enemy_present = True
                if player_class == "Melee":
                    closest = kill(rectangles)
                    c(closest[0], closest[1])
                elif player_class == "Distance" or player_class == "Magic":
                    closest = kill(rectangles)
                    c(closest[0], closest[1])
                    c(closest[0]+80, closest[1])
                    c(closest[0]-80, closest[1])
                    c(closest[0], closest[1]+80)
                    c(closest[0], closest[1]-80)
                    
                
            # search if cooldown has passed and no enemies are present
            elif searchinterval > 50 and enemy_present == False:
                searchinterval = 0
                map_search()
                # reset rectangles
                rectangles = []
            else:
                enemy_present = False
                searchinterval += 1
            
        elif debug_mode == True:
            # show the region of interest that the program is searching in, with the drawn found elements
            output_enemy = mob_instance.show_found(screenshot, rectangles)
            draw_grid(output_enemy)
            cv.imshow('debug_mode', output_enemy)
            cv.imshow('processed_image', proc_image)
            #cv.imshow('automphp', automphp_check)
            #cv.imshow('exhausted', exhausted_check)
        
        # displays fps    
        #print('FPS {}'.format(1 / (time() - loop_time)))
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