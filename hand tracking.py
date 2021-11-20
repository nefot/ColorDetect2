import cv2
import numpy as np
import mediapipe as mp
import numpy as np
from setting import *

FRAMEWIDTH = 640
FRAMEHEIGHT = 480
cap = cv2.VideoCapture(0)
cap.set(3, FRAMEWIDTH)
cap.set(4, FRAMEHEIGHT)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    landMarksList = result.multi_hand_landmarks
    if landMarksList:
        for landmark in landMarksList:
            for id, lm in enumerate(landmark.landmark):

    cv2.imshow("Orig", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
        break
