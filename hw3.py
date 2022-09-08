import cv2
import numpy as np


vidcap = cv2.VideoCapture('BookScene.MOV', )

while True:
    ret, frame = vidcap.read()
    cv2.imshow('frame', frame)

    hsvBlue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([0, 100, 100])

    mask = cv2.inRange(hsvBlue, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    print(mask)

    if cv2.waitKey(20) == ord('q'):
        break



vidcap.release()
cv2.destroyAllWindows()
