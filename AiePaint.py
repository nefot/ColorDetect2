import time
import numpy as np
from cv2 import cv2
import HandTrackingModule as htm

prev_x, prev_y = 0, 0
thick = 4

was_first_point_selected = False

pTime = 0
cTime = 0
currentTool = 'Select'
start_draw = False

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

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
detector = htm.HandDetector()
findIndex = [4, 8, 12, 16, 20]


mask = np.ones((FRAME_HEIGHT,FRAME_WIDTH))*255
mask = mask.astype('uint8')



def ShowFps(img):
    global pTime
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
    cv2.imshow("imgResult", img)




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
        #если два пальца то не рисовать
        if fingerState == [0,1,1,0,0]:
            start_draw = False
        # если один палец то рисовать
        if fingerState == [0,1,0,0,0]:
            start_draw = True

        if panal_Xpos < x < pXmax and y < pYmax and not start_draw:
            currentTool = getTool(x)
            # print(id, x, y)
        else:
            if currentTool == "draw":
                if start_draw:
                    cv2.line(mask,(prev_x,prev_y),(x,y),(0,0,0),thick)
                    prev_x,prev_y = x,y
                else:
                    prev_x,prev_y = x,y

            if currentTool == "rect":
                if start_draw:
                    if not was_first_point_selected:
                        prev_x, prev_y = x, y
                        was_first_point_selected = True
                    cv2.line(img, (prev_x, prev_y), (x, y), (0, 0, 0), thick)
                else:
                    if was_first_point_selected:
                        cv2.line(mask, (prev_x, prev_y), (x, y), (0, 0, 0), thick)
                        was_first_point_selected = False

            if currentTool == "line":
                if start_draw:
                    if not was_first_point_selected:

                        prev_x, prev_y = x, y
                        was_first_point_selected =True
                    cv2.line(img, (prev_x, prev_y), (x, y), (0, 0, 0), thick)
                else:
                    if was_first_point_selected:
                        cv2.line(mask, (prev_x, prev_y), (x, y), (0, 0, 0), thick)
                        was_first_point_selected =False


            if currentTool == "circle":
                if start_draw:
                    cv2.circle(mask,(prev_x+20,prev_y+20),40,(0,0,0),thick)
                    prev_x,prev_y = x,y
                else:
                    prev_x,prev_y = x,y

            if currentTool == "eraser":
                if start_draw:
                    cv2.circle(mask, (prev_x + 20, prev_y + 20), 1, (255), 60 )
                    prev_x, prev_y = x, y
                else:
                    prev_x, prev_y = x, y

    finImg = cv2.bitwise_and(img, img, mask=mask)
    cv2.putText(img, currentTool,(500, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        # if x > (panal_Xpos - pXmax) and x < pXmax:
        #     print("ПОПАЛ")
    finImg[:pYmax, panal_Xpos:pXmax] = cv2.addWeighted(tools, 1, img[:pYmax, panal_Xpos:pXmax], 1, 0)
    cv2.imshow("img",finImg)
    #cv2.imshow("mask",mask)

    ShowFps(img)



    if cv2.waitKey(1) & 0xFF == 27:  # ord('q'):
        break
