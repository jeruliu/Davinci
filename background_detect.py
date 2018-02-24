# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:15:18 2018

@author: jeru
"""
import cv2

# calculate the position of surrounding borders with specified space from the edge
def cal_borders(y, x, n_slice):
    yspan, xspan  = int(y / n_slice), int(x / n_slice)
    return (yspan, y - yspan, xspan, x - xspan)

# slice four rectangles from the edge
def find_recs(top, bottom, left, right, n_rows, n_cols):
    # roi = image[y1:y2, x1:x2]
    top_roi = gray[0:top, 0:n_cols]
    bottom_roi = gray[bottom:n_rows, 0:n_cols]
    left_roi = gray[0:n_rows, 0:left]
    right_roi = gray[0:n_rows, right:n_cols]
    return (top_roi, bottom_roi, left_roi, right_roi)

def assert_rec(rec):
    (means, stds) = cv2.meanStdDev(rec)
    return True if (means[0][0] == 255 and stds[0][0] == 0) else False
    
def assert_recs(top_roi, bottom_roi, left_roi, right_roi):
    isTopWhite = assert_rec(top_roi)
    isBottomWhite = assert_rec(bottom_roi)
    isLeftWhite = assert_rec(left_roi)
    isRightWhite = assert_rec(right_roi)
    return (isTopWhite, isBottomWhite, isLeftWhite, isRightWhite)

image = cv2.imread('D:/dev/bg/1044900258-225256454181249031-225256454181249106-5.jpg')

n_rows = image.shape[0]
n_cols = image.shape[1]
    
top, bottom, left, right = cal_borders(n_rows, n_cols, 50)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
top_roi, bottom_roi, left_roi, right_roi = find_recs(top, bottom, left, right, n_rows, n_cols)

print (assert_recs(top_roi, bottom_roi, left_roi, right_roi))
