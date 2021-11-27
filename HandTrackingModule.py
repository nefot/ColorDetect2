import time
from cv2 import cv2
import  mediapipe as mp


class HandDetector:
    def __init__(self,
                 mode=False,
                 maxHands=2,
                 complexity=1,
                 detectConf=0.5,
                 trackingConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectConf = detectConf
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode,
            self.maxHands,
            self.complexity,
            self.detectConf,
            self.trackingConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        lm_list = self.results.multi_hand_landmarks
        if lm_list:
            for handLm in lm_list:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLm, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo =0, draw = True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    # cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

                    cv2.putText(img,str(id),(cx, cy),cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 0), 2)
        return lmList

def main():
    cTime =0
    pTime =0
    frameWidth = 640
    frameHight = 480

    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHight)
    cap.set(10,-50) #яркость камеры
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img  = detector.findHands(img, draw= True)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255), 4)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        cv2.imshow("imgResult", img)
        if cv2.waitKey(1) & 0xFF == 27:  # ord('q'): # 27 - это Esc
            break


if __name__ == "__main__":
    main()