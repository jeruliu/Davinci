# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 07:39:55 2018
### Make sure you have dlib installed and predictor data downloaded 
### before making use of this API
@author: Jeru
"""
from imutils import face_utils
import dlib
import cv2

# return a list of rectangles hover on the face
def detect_face_rects(image):
    detector = dlib.get_frontal_face_detector()   
    return detector(image, 1)

# return the number of the faces captured
def count_faces(image):
    return len(detect_face_rects(image))

# draw rectangle over the face  
def box_face(image, rect): 
    # convert dlib's rectangle to a OpenCV-style bounding box
    # [i.e., (x, y, w, h)], then draw the face bounding box
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return (image, x, y)

# optional function, only envoked after box_face
def tag_face_number(image, index, x, y):
    cv2.putText(image, "Face #{}".format(index), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# optional function, only envoked after box_face
def draw_face_landmarks(image, predictor, rect, x, y):
    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy array
    shape = predictor(image, rect)
    shape = face_utils.shape_to_np(shape)
    for (x, y) in shape:
        cv2.circle(image, (x, y), 1, (255, 0, 0), -1)

# put everything together, loop over all faces and draw everything.     
def mark_all_faces(image):
    # loop over the face detections
    for (i, rect) in enumerate(detect_face_rects(image)):
    	  (image, x, y) = box_face(image, rect)
    	  tag_face_number(image, i + 1, x, y)
    	  draw_face_landmarks(image, predictor, rect, x, y)
	
'''
### below is the demo of the usage ###
--------------------------------------
image = cv2.imread("C:/dev/uw0.jpg")
# make sure you have the data file downloaded
predictor = dlib.shape_predictor("C:/dev/shape_predictor_68_face_landmarks.dat")

image = imutils.resize(image, width=500)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("Number of faces captured: {}".format(count_faces(image)))
mark_all_faces(image)

cv2.imshow("Output", image)
cv2.waitKey(0)
'''
