# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:15:18 2018

@author: jeru
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

# calculate the position of surrounding borders with specified space from the edge
def cal_borders(y, x, n_slice):
    yspan, xspan  = int(y / n_slice), int(x / n_slice)
    return (yspan, y - yspan, xspan, x - xspan)

# slice four corners
def find_conners(gray, top, bottom, left, right, n_rows, n_cols):
    top_left_roi = gray[0:top, 0:left]
    bottom_left_roi = gray[bottom:n_rows, 0:left]
    top_right_roi = gray[0:top, right:n_cols]
    bottom_right_roi = gray[bottom:n_rows, right:n_cols]
    return (top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi)

def assert_white_corner(corner):
    (means, stds) = cv2.meanStdDev(corner)
    print(means[0][0], stds[0][0])
    # I leave some buffer for exception case when bg is nearly white
    return True if (means[0][0] > 250 and stds[0][0] <1) else False

def assert_white_corners(top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi):
    isTopLeftWhite = assert_white_corner(top_left_roi)
    isBottomLeftWhite = assert_white_corner(bottom_left_roi)
    isTopRightWhite = assert_white_corner(top_right_roi)
    isBottomRightWhite = assert_white_corner(bottom_right_roi)
    return (isTopLeftWhite, isBottomLeftWhite, isTopRightWhite, isBottomRightWhite)

# slice four margins 
def find_margins(gray, top, bottom, left, right, n_rows, n_cols):
    # roi = image[y1:y2, x1:x2]
    top_roi = gray[0:top, 0:n_cols]
    bottom_roi = gray[bottom:n_rows, 0:n_cols]
    left_roi = gray[0:n_rows, 0:left]
    right_roi = gray[0:n_rows, right:n_cols]
    return (top_roi, bottom_roi, left_roi, right_roi)

# to find color difference of the margin
def get_margin_stds(margin):
    (means, stds) = cv2.meanStdDev(margin)
    return stds[0][0]
    
def cal_margins_average_stds(top_roi, bottom_roi, left_roi, right_roi):
    topStds = get_margin_stds(top_roi)
    bottomStds = get_margin_stds(bottom_roi)
    leftStds = get_margin_stds(left_roi)
    rightStds = get_margin_stds(right_roi)
    averageStds = np.average((topStds, bottomStds, leftStds, rightStds))
    return averageStds

# main entry
def detect_bg(image):
    n_rows = image.shape[0]
    n_cols = image.shape[1]
    
    top, bottom, left, right = cal_borders(n_rows, n_cols, 50)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    top_roi, bottom_roi, left_roi, right_roi = find_margins(gray, top, bottom, left, right, n_rows, n_cols)
    top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi = find_conners(gray, top, bottom, left, right, n_rows, n_cols)
    
    averageMarginStds = cal_margins_average_stds(top_roi, bottom_roi, left_roi, right_roi)
    #print(averageMarginStds)
    
    if (assert_white_corners(top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi) == (True, True, True, True)):
        return "White"  
    elif (averageMarginStds<25.0): # 25 as a threashold
        return "Pure"
    elif (assert_white_corners(top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi) == (False, False, False, False)):
        return "Complex"      
    else: 
        return "Not Sure"

#image = cv2.imread('D:/dev/bg/2f00f298-2edb-418f-a5a5-afedee44b505.jpg')
#detect_bg(image)

'''
#cv2.imshow("Output", hist)
#cv2.waitKey(0)

cv2.imshow("Output", bottom_roi)
cv2.waitKey(0)

cv2.line(image, (0, top), (n_cols, top), (255,0,0), 2)
cv2.line(image, (0, bottom), (n_cols, bottom), (255,0,0), 2)
cv2.line(image, (left, 0), (left, n_rows), (255,0,0), 2)
cv2.line(image, (right, 0), (right, n_rows), (255,0,0), 2)
'''

#45701197-08dd-4738-b7cf-99afbda3d38d_t.jpg
