import cv2
import numpy as np

vidcap = cv2.VideoCapture('BookScene.MOV', )

while True:
    ret, frame = vidcap.read()
    #cv2.imshow('frame', frame)

    hsvBlue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([10, 10, 10])
    upper_blue = np.array([344, 150, 150])

    mask = cv2.inRange(hsvBlue, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100000:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            #cv2.rectangle(frame, )

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    if cv2.waitKey(20) == ord('q'):
        break

vidcap.release()
cv2.destroyAllWindows()
