import pyautogui as py
from math import sqrt
from time import sleep
from pywinauto import Application, findwindows
import window_input
from random import shuffle



class Bot:
    def gtv(self, sublist):
        return sublist[2]

    def kill(self, rectangles):
        distances = []
        x, y, w, _ = rectangles
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

               


