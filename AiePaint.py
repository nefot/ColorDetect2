import time

from cv2 import cv2
import HandTrackingModule as htm

pTime = 0
cTime = 0
currentTool = 'Select'


def getTool(x):
    if x < panal_Xpos +50:
        return "line"
    elif x < panal_Xpos +2*50:
        return "rect"
    elif x < panal_Xpos +3*50:
        return "draw"
    elif x < panal_Xpos +4*50:
        return "circle"
    elif x < panal_Xpos +5*50:
        return "eraser"


tools = cv2.imread('tools.png')
panel_h, panel_w, _ = tools.shape
panal_Xpos = 100
pXmax = panal_Xpos + panel_w
pYmax = panel_h


def ShowFps(img):
    global pTime
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
    cv2.imshow("imgResult", img)


FRAME_WIDTH = 640
FRAME_HEIGHT = 480
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
detector = htm.HandDetector()
findIndex = [4, 8, 12, 16, 20]


def GetFingerState(landMarksList):
    fingers = []
    if landMarksList[findIndex[0]][1] > landMarksList[findIndex[0] - 2][1]:
        fingers.append(0)

    else:
        fingers.append(1)

    for id in range(1, 5):
        if landMarksList[findIndex[id]][2] > landMarksList[findIndex[id] - 2][2]:
            fingers.append(0)

        else:
            fingers.append(1)
    return fingers


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    landMarksList = detector.findPosition(img, draw=True)
    # print(landMarksList)
    if landMarksList:

        fingerState = GetFingerState(landMarksList)
        id, x, y = landMarksList[8]
        if panal_Xpos < x < pXmax and y < pYmax:
            currentTool = getTool(x)
            # print(id, x, y)
    cv2.putText(img, currentTool,(500, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        # if x > (panal_Xpos - pXmax) and x < pXmax:
        #     print("ПОПАЛ")
    img[:pYmax, panal_Xpos:pXmax] = cv2.addWeighted(tools, 1, img[:pYmax, panal_Xpos:pXmax], 1, 0)
    ShowFps(img)
    if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
        break
