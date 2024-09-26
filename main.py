import cv2
import numpy as np

# FRAME SETTINGS
FRAMEWIDTH = 640
FRAMEHEIGHT = 480

def empty(a):
    pass

"""
25,40,72,255,133,255 - yellow
68, 121, 115, 255, 0, 255 - green
"""

def findColor(img, myColors, myColorsValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Video Capture and Trackbars setup
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

def getCont(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgCounturs, contours, -1, [255, 100, 100], 10, cv2.LINE_8, hierarchy)
            P = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * P, True)
            x, y, w, h = cv2.boundingRect(approx)

# Main loop
while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("imgResult", imgResult)

    if cv2.waitKey(1) & 0xFF == 27:  # 27 - это Esc
        break
