# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:15:18 2018

@author: jeru
"""
import cv2
import numpy as np

image = cv2.imread('D:/dev/bg/1044900258-225256454181249031-225256454181249106-5.jpg')

n_rows = image.shape[0]
n_cols = image.shape[1]

print ('number of rows: {}'.format(n_rows))
print ('number of cols: {}'.format(n_cols))

# calculate the position of surrounding borders with specified space from the edge
def cal_borders(y, x, n_slice):
    yspan, xspan  = int(y / n_slice), int(x / n_slice)
    return (yspan, y - yspan, xspan, x - xspan)

top, bottom, left, right = cal_borders(n_rows, n_cols, 50)


cv2.line(image, (0, top), (n_cols, top), (255,0,0), 2)
cv2.line(image, (0, bottom), (n_cols, bottom), (255,0,0), 2)
cv2.line(image, (left, 0), (left, n_rows), (255,0,0), 2)
cv2.line(image, (right, 0), (right, n_rows), (255,0,0), 2)

cv2.imshow("Output", image)
cv2.waitKey(0)

