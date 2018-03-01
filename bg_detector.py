# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 10:43:27 2018

@author: jeru
"""
import cv2
import numpy as np

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
    # I leave some buffer for exception case when bg is nearly white
    return True if (means[0][0] > 250 and stds[0][0] <1) else False

def assert_white_corners(top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi):
    isTopLeftWhite = assert_white_corner(top_left_roi)
    isBottomLeftWhite = assert_white_corner(bottom_left_roi)
    isTopRightWhite = assert_white_corner(top_right_roi)
    isBottomRightWhite = assert_white_corner(bottom_right_roi)
    return (isTopLeftWhite, isBottomLeftWhite, isTopRightWhite, isBottomRightWhite)

def gray2rgb(image):
    channels = np.zeros((image.shape[0], image.shape[1],3))
    channels[:,:,2] = image[:,:]
    channels[:,:,1] = image[:,:]
    channels[:,:,0] = image[:,:]
    return channels

def canny_edge(image, lower=0, upper=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)  
    edge = cv2.Canny(blurred, lower, upper)
    return gray2rgb(edge)

# slice left and right margins 
def find_margins(gray, top, bottom, left, right, n_rows, n_cols):
    # roi = image[y1:y2, x1:x2]
    left_roi = gray[0:n_rows, 0:left]
    right_roi = gray[0:n_rows, right:n_cols]
    return (left_roi, right_roi)

# to find color difference of the margin
def get_margin_means(margin):
    (means, stds) = cv2.meanStdDev(margin)
    print (means[0][0], stds[0][0])
    return means[0][0]

# main entry, the corner rectangle depends on scale
# corner rectangle height = image height divided by scale
# corner rectangle width = image width divided by scale
def detect_bg(image, scale):
    n_rows = image.shape[0]
    n_cols = image.shape[1]
    
    top, bottom, left, right = cal_borders(n_rows, n_cols, scale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # you may want to comment out below four lines which is for demostration only
    '''
    cv2.rectangle(image,(0,0),(left, top),(50, 50, 50),3)
    cv2.rectangle(image,(0,bottom),(left,n_rows),(50, 50, 50),3)
    cv2.rectangle(image,(right,0),(n_cols,top),(50, 50, 50),3)
    cv2.rectangle(image,(right,bottom),(n_cols,n_rows),(50, 50, 50),3) 
    '''
    
    top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi\
        = find_conners(gray, top, bottom, left, right, n_rows, n_cols) 
 
    if (assert_white_corners(top_left_roi, bottom_left_roi, top_right_roi, bottom_right_roi)\
        == (True, True, True, True)):
        return "White"  
    else: 
        edge = canny_edge(image, 0, 50)
        left_roi, right_roi = find_margins(edge, top, bottom, left, right, n_rows, n_cols)
        left_means = get_margin_means(left_roi)
        right_means = get_margin_means(right_roi)
        if (left_means == 0  and right_means == 0):
            return "Pure"
        else:
            return "Complex"
