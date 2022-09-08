import cv2
import numpy as np

vidcap = cv2.VideoCapture('BookScene.MOV')



# open template
templateT = cv2.imread('Book 4.png', cv2.IMREAD_COLOR)

while True:
    ret, frame = vidcap.read()

    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # create copy
    #img_copy = img.copy()
    img_c = frame

    hsvBlue = cv2.cvtColor(img_c, cv2.COLOR_BGR2HSV)
    hsvBlueT = cv2.cvtColor(templateT, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([0, 30, 30])
    upper_blue = np.array([175, 80, 80])

    img_copy = cv2.inRange(hsvBlue, lower_blue, upper_blue)
    template = cv2.inRange(hsvBlueT, lower_blue, upper_blue)

    # cv2.imshow("Orginal Image", img)
    # cv2.imshow("Template", template)

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    width, height = template.shape[::-1]

    for method in methods:
        img = img_copy.copy()
        method_eval = eval(method)

        # Apply template Matching
        result = cv2.matchTemplate(img, template, method_eval)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # threshold = 0
        # loc = np.where(result >= threshold)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(img, pt, (pt[0] + width, pt[1] + height), (0,0,255), 2)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method_eval in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + width, top_left[1] + height)
        space = cv2.rectangle(frame, top_left, bottom_right, 255, 2)  # mark the face on the image

    pic = cv2.resize(space, (450, 690))
    cv2.imshow("Matched Result", pic)

    if cv2.waitKey(20) == ord('q'):
        break
