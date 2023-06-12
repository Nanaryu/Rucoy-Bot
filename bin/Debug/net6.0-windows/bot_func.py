import pyautogui as py
from math import sqrt
from time import sleep
from pywinauto import Application, findwindows
import window_input
from random import shuffle
import cv2 as cv
import numpy as np

def exhaustion_check(exhausted_image):
    e = exhausted_image
    red = (61, 61, 255)
    p1 = tuple(e[19,88].astype(np.uint8))
    p3 = tuple(e[13,30].astype(np.uint8))
    if p1==red and p3==red:
        return True
    else:
        return False
    # red is b g r 61 61 255


def gtv(sublist):
    return sublist[2]

def kill(rectangles):
    distances = []
    for (x, y, w, h) in rectangles:
        distances.append(
            [
                x + int(w/2), # enemy x
                y + h + 10 + 40, # enemy y
                sqrt((x - 640)**2 + (y - 390)**2) # distance from player center(640, 390)
            ]
        )
    # sort lists to get the closest enemy coordinates
    dSorted = sorted(distances, key=gtv) 
    if len(dSorted) != 0:
        enemy_x = dSorted[0][0]
        enemy_y = dSorted[0][1]
        return [enemy_x, enemy_y]
            
def shuffle_map_points():
    clicklist = [
        [640, 360+80],
        [640, 360-80],
        [640+80, 360],
        [640+80, 360+80],
        [640+80, 360-80],
        [640-80, 360],
        [640-80, 360+80],
        [640-80, 360-80]
    ]
    shuffle(clicklist)
    return clicklist


        