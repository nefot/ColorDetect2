from cv2 import cv2
import HandTrackingModule as htm

FRAMEWIDTH = 640
FRAMEHEIGHT = 480
cap = cv2.VideoCapture(0)
cap.set(3, FRAMEWIDTH)
cap.set(4, FRAMEHEIGHT)
detector = htm.HandDetector()
findIndex = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img,draw = True)
    landMarksList = detector.findPosition(img,draw = True)
    # print(landMarksList)
    if landMarksList:
        fingers=[]
        if landMarksList[findIndex[0]][1]>landMarksList[findIndex[0]-2][1]:
            fingers.append(0)

        else:
            fingers.append(1)

        for id in range(1,5):
            if landMarksList[findIndex[id]][2]>landMarksList[findIndex[id]-2][2]:
                fingers.append(0)

            else:
                fingers.append(1)

        print(fingers)
    cv2.imshow("Orig", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
        break
