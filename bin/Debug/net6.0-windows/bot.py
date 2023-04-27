import pyautogui as py
from math import sqrt
from time import sleep

def gtv(sublist):
        return sublist[2]

class Bot:
    
    def kill(self, rectangles):
        distances = []
        for (x, y, w, h) in rectangles:
            distances.append(
                    (
                        x, # enemy x
                        y, # enemy y
                        sqrt((x - 640)**2 + (y - 390)**2) # distance from player center(640, 390)
                    )
                )
        # sort lists to get the closest enemy coordinates
        dSorted = sorted(distances, key=gtv) 
            
        if len(dSorted) != 0:
            py.click(dSorted[0][0]+int(w/2), dSorted[0][1] + 140, 0.5) # click the enemy
            sleep(1)
            py.click(dSorted[0][0]+int(w/2), dSorted[0][1] + 140, 0.5) # unclick the enemy, so the next click selects it again

