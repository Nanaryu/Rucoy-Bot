import cv2 as cv
import numpy as np
import pyautogui as py
from hsvfilter import HsvFilter
import sys
from math import sqrt

class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"


    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match  
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_COLOR)

        # Save the dimensions of the needle image

        self.needle_h, self.needle_w = self.needle_img.shape[:2]
        '''
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        '''
        
        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method
   
    def find(self, haystack_img, threshold=0.5):
        roi = haystack_img[80:80+560, 120:120+1040]
        height, width, _ = roi.shape #1040x560
        h, w, _ = self.needle_img.shape
        # rucoy area viewable by player
        # 13 squares 80x80 width
        # 7 squares 80x80 height
        
        rectangles = []
        # resize for
        resized_roi = cv.resize(roi, (int(width/2), int(height/2)))
        res_needle = cv.resize(self.needle_img, (int(w/2), int(h/2)))
        # Perform template matching 
                
        result = cv.matchTemplate(resized_roi, res_needle, self.method)

                
        # Get the positions from the match result that exceed threshold

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Add the rectangles for the to the list
        for loc in locations:
            rect = [int(loc[0])*2 + 120, int(loc[1])*2 + 80, res_needle.shape[1]*2, res_needle.shape[0]*2]
            rectangles.append(rect)

        # Apply group rectangles to eliminate overlapping rectangles
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        # convert from array() to list() for better data manipulation
        rectangle_list = []
        for rectangle in rectangles:
            rectangle_list.append(list(rectangle))
        
        return rectangle_list

    
    def get_click_points(self, rectangles):
        points = []
        x, y, w, h = rectangles
        # Determine the center position
        center_x = x + int(w/2)
        center_y = y + int(h/2)
        # Save the points
        points.append((center_x, center_y))
        return points


    def gtv(self, sublist):
            return sublist[2]

    def show_found(self, haystack_img, rectangles):
        line_color = (0, 0, 255)
        line_type = cv.LINE_4
        player_x_roi = 520
        player_y_roi = 280
        player_x = 640
        player_y = 360

        #cv.rectangle(haystack_img, (480, 240), (560, 320), (0, 255, 0), 2)

        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + h + 10 + 40
            top_left = (center_x - 40, y + h + 10)
            bottom_right = (center_x + 40, y + h + 10 + 80)
            
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, lineType=line_type, thickness=3)
            cv.line(haystack_img, (player_x, player_y), (center_x, center_y), (0, 255, 0), 2)
                    

        return haystack_img



    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c