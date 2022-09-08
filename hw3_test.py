import cv2
import numpy as np

frame = cv2.imread('Book.PNG', cv2.IMREAD_COLOR)

while True:

    hsvBlue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([10, 10, 10])
    upper_blue = np.array([344, 150, 150])

    mask = cv2.inRange(hsvBlue, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('frame', frame)
    pic = cv2.resize(mask, (450, 690))
    cv2.imshow('Pic', pic)


    if cv2.waitKey(20) == ord('q'):
        break

vidcap.release()
cv2.destroyAllWindows()