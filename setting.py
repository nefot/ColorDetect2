import cv2
import numpy
import numpy as np

FRAMEWIDTH = 640
FRAMEHEIGHT = 480


def empty(a):
    pass



"""
25,40,72,255,133,255 - yellow
68, 121, 115, 255, 0 ,255 - зеленный
"""

myColors = [[25, 72, 133, 40, 255, 255],  # Желтый
            [68, 115, 0, 121, 255, 255]  # берюзовый

            ]
myColorsValue = [[0,255,255],
                 [255,255,0]

                 ]


cap = cv2.VideoCapture(0)
cap.set(3, FRAMEWIDTH)
cap.set(4, FRAMEHEIGHT)
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
v_max = cv2.getTrackbarPos("Val Max", "TrackBars")