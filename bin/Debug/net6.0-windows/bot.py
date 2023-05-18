import pyautogui as py
from math import sqrt
from time import sleep
from pywinauto import Application, findwindows
import window_input
from random import shuffle
import cv2 as cv
import numpy as np



class Bot:
    def gtv(self, sublist):
        return sublist[2]

    def kill(self, rectangles):
        distances = []
        for (x, y, w, _) in rectangles:
            distances.append(
                [
                    x, # enemy x
                    y, # enemy y
                    sqrt((x - 640)**2 + (y - 390)**2) # distance from player center(640, 390)
                ]
            )
            # sort lists to get the closest enemy coordinates
            dSorted = sorted(distances, key=self.gtv) 

            if len(dSorted) != 0:
                enemy_x = dSorted[0][0] + int(w/2)
                enemy_y = dSorted[0][1] + 140
                return [enemy_x, enemy_y]
            
    def shuffle_map_points(self):
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

    def exhaustion_check(self, exhausted_check, exhausted_path, threshold):
        result = cv.matchTemplate(exhausted_check, exhausted_path, cv.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), exhausted_path.shape[1], exhausted_path.shape[0]]
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        rectangle_list = []
        for rectangle in rectangles:
            rectangle_list.append(list(rectangle))
        return rectangle_list           


