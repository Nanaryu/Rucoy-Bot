import pyautogui as py
from math import sqrt
from time import sleep

def gtv(sublist):
        return sublist[2]

class Bot:
    
    def kill(self, rectangles):
        distances = [] # mega table
        for enemyT in rectangles:
            distances.append(
                    (
                        enemyT[0], # enemy name x
                        enemyT[1], # enemy name y
                        sqrt((enemyT[0] - 633)**2 + (enemyT[1] - 360)**2) # distance from player (633, 360)
                    )
                )
        dSorted = sorted(distances, key=gtv) # sort tables in mega table to get the closest enemy coordinates
            
        if len(dSorted) != 0:
            if dSorted[0][1] < 660:
                py.click(dSorted[0][0] + dSorted[0][2]/2 + 15, dSorted[0][1] + 90) # click the enemy
                sleep(5)
                py.click(dSorted[0][0] + dSorted[0][2]/2 + 15, dSorted[0][1] + 90) # click the enemy

