import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui as py
from math import sqrt
from hsvfilter import HsvFilter
import sys
from bot import Bot
from random import randint

if cv.ocl.haveOpenCL():
    cv.ocl.setUseOpenCL(True)
    print("OpenCL is enabled")
else:
    print("OpenCL is not available")


def draw_grid(img):
    for i in range(40, 1281, 80):
        cv.line(img, (i, 0), (i, 720), (255, 255, 0), 1)

    for i in range(0, 721, 80):
        cv.line(img, (0, i), (1280, i), (255, 255, 0), 1)

    for i in range(120, 1161, 80):
        cv.line(img, (i, 80), (i, 640), (255, 0, 0), 1)
    
    for i in range(80, 641, 80):
        cv.line(img, (120, i), (1160, i), (255, 0, 0), 1)

def draw_grid_nohalf(img):
    for i in range(0, 1040, 80):
        cv.line(img, (i, 0), (i, 560), (255, 0, 0), 1)
    
    for i in range(0, 560, 80):
        cv.line(img, (0, i), (1040, i), (255, 0, 0), 1)
    


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

loop_time = time()

# initialize the WindowCapture class
wincap = WindowCapture('NoxPlayer')

image_paths = sys.argv[3].split("//")

vision_instances = []

for path in image_paths:
    vision_instances.append(Vision(path + "c.png"))


bot = Bot()



blackwhite = HsvFilter(0, 0, 237, 0, 153, 255, 0, 0, 0, 0)


MAP_OPEN = False #1000 70, close 1245 70

if sys.argv[1] == "True":
    debug_mode = True
elif sys.argv[1] == "False":
    debug_mode = False

while True:
    try:
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        
        proc_image = vision_instances[0].apply_hsv_filter(screenshot, blackwhite)
        rectangles = []

        for vision_instance in vision_instances:
            rectangles.append(vision_instance.find(proc_image, 0.65))
            
            

        #enemy_proc_img = enemy.apply_hsv_filter(screenshot, blackwhite)
        #rectangles = enemy.find(enemy_proc_img, 0.46)

        if debug_mode == False:
            py.getWindowsWithTitle("NoxPlayer")[0].moveTo(0, 0)
            if len(rectangles[0]) != 0:
                for i in range(len(rectangles)):
                    bot.kill(rectangles[i])
            else:
                r = randint(0, 4)
                if r == 1:
                    py.click(633 + 80, 360)
                elif r == 2:
                    py.click(633 - 80, 360)
                elif r == 3:
                    py.click(633, 360 + 80)
                else:
                    py.click(633, 360 - 80)
        else:
            #print(rectangles)
            for vision_instance in vision_instances:
                for i in range(len(rectangles)):
                    output_enemy = vision_instance.show_found(screenshot[80:80+560, 120:120+1040], rectangles[i])
                    #output_enemy = vision_instance.find_sift(screenshot)
                    draw_grid_nohalf(output_enemy)
                    cv.imshow('debug_mode', output_enemy)
            draw_grid(proc_image)
            cv.imshow('processed_image', proc_image)
            
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # press 'q' with the output window focused to exit.
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to continue...")

print('Done.')