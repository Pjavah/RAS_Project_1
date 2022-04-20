import cv2
import numpy as np



def contourSquares(img):
    #img = cv2.imread('./pictures/square17.jpeg')
    img = cv2.resize(img, (0, 0), None, .50, .50)

    #### contrast

    alpha = 1.9 # Contrast control (1.0-3.0)
    beta = 0 # Brightness control (0-100)

    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    value = 50

    mat = np.ones(adjusted.shape,dtype = 'uint8')*value
    subtract = cv2.subtract(adjusted,mat)


    ##Making the image clearer


    hsv = cv2.cvtColor(subtract, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([20, 150, 170])
    upper_bound = np.array([55, 250, 215])
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = np.ones((7,7),np.uint8)
    # Remove unnecessary noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Segment only the detected region
    #segmented_img = cv2.bitwise_and(img, img, mask=mask)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.drawContours(subtract, contours, -1, (0, 0, 255), 3)

    threshold = 100

    src_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    src_gray = cv2.blur(src_gray, (3,3))
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)

    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])


    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)


    for i in range(len(contours)):
        color = (255,0,255)
        if cv2.contourArea(contours[i]) > 1000:
            cv2.drawContours(drawing, contours_poly, i, color)
            cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
                (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)


    while True:

    
        cv2.imshow("rectangles", drawing)
        cv2.imshow("original", output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


contourSquares(cv2.imread('green.jpeg'))