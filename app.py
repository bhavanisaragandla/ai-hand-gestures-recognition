import cv2
import numpy as np
import pyautogui
from hand_tracking import HandDetector
from volume_control import VolumeControl

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector()
volume = VolumeControl()

screen_w, screen_h = pyautogui.size()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        x1, y1 = lmList[8][1], lmList[8][2]   # index
        x2, y2 = lmList[12][1], lmList[12][2] # middle
        x3, y3 = lmList[4][1], lmList[4][2]   # thumb

        # Mouse Movement
        screen_x = np.interp(x1, (0, wCam), (0, screen_w))
        screen_y = np.interp(y1, (0, hCam), (0, screen_h))
        pyautogui.moveTo(screen_x, screen_y)

        # Click (index + middle)
        dist_click = detector.findDistance(8, 12, lmList)
        if dist_click < 30:
            pyautogui.click()

        # Scroll (index + thumb)
        dist_scroll = detector.findDistance(8, 4, lmList)
        if dist_scroll < 25:
            pyautogui.scroll(30)

        # Volume (thumb + index distance)
        dist_vol = detector.findDistance(4, 8, lmList)
        volume.setVolume(dist_vol)

    cv2.imshow("Hand Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()