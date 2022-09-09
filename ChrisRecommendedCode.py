import cv2
import numpy as np

# Part K - Feature Matching Sift model

# number of features to match
MIN_MATCH_COUNT = 10
# read in original image
img = cv2.imread('box_in_scene.png')
# read in query image
img_query = cv2.imread('box_3.png')  # query image
# if no image return
if img_query is None:
    print('Query Image Does Not Exist')
    exit()

# Show Images
cv2.imshow("object", img_query)
cv2.imshow("scene image", img)

key = cv2.waitKey(0)

# detect the feature, SIFT detector, Scale-Invariant Feature Transform
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img_query, None)
kp2, des2 = sift.detectAndCompute(img, None)

# Algorithm Selection
FLANN_INDEX_KDTREE = 1
# get index parameters as dictionary
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# get search parameters
search_params = dict(checks=50)
# Use flann based matcher
flann = cv2.FlannBasedMatcher(index_params, search_params)
# get KNN matches for K value of 2
matches = flann.knnMatch(des1, des2, k=2)
# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    # Get source and destination points and reshape array
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # find homography on source/destination points
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # matched mast to list
    matchesMask = mask.ravel().tolist()
    # get height width and depth
    h, w, d = img_query.shape

    # reshape points array to match height width
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

    dst = cv2.perspectiveTransform(pts, M)
    # draw lines and set color
    img_polylines = cv2.polylines(img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    # show polylines
    cv2.imshow("matching image", img_polylines)

    key = cv2.waitKey(0)

    # draw matches in green color
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)

    # Get Matched Image using drawMatches
    img_matched = cv2.drawMatches(img_query, kp1, img, kp2, good, None, **draw_params)
    # display matched features
    cv2.imshow("Matched Feature Items", img_matched)
    # pause windows until close
    key = cv2.waitKey(0)
