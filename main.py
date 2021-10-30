import cv2
import numpy
import numpy as np
from setting import *


def findColor(img, myColors, myColorsValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# img: numpy.ndarray = cv2.imread('robot.jpeg', cv2.IMREAD_COLOR)
# h, w, _ = img.shape
# shrine_kof = 2
# img = cv2.resize(img, (w // shrine_kof, h // shrine_kof), cv2.INTER_NEAREST)


def getCont(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgCounturs, contours, -1, [255, 100, 100], 10, cv2.LINE_8, hierarchy)
            P = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * P, True)
            x, y, w, h = cv2.boundingRect(approx)


while True:
    success, img = cap.read()
    imgCounturs = img.copy()
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("imgResult", imgResult)
    cv2.imshow("Orig", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
        break
