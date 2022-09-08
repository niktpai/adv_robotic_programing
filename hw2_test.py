import cv2
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

frame = cv2.imread('Book 3.PNG', cv2.IMREAD_COLOR)

while True:

    hsvBlue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    print(hsvBlue)

    lower_blue = np.array([0, 30, 30])
    upper_blue = np.array([175, 80, 80])

    mask = cv2.inRange(hsvBlue, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('frame', frame)
    pic = cv2.resize(mask, (450, 690))
    cv2.imshow('Pic', pic)


    if cv2.waitKey(20) == ord('q'):
        break

cv2.destroyAllWindows()