import cv2
import numpy as np
import math



def contourSquares(img):
    #img = cv2.imread('./pictures/square17.jpeg')
    img = cv2.resize(img, (0, 0), None, .50, .50)
    img_h, img_w, channels = img.shape
    img_center = int(img_w / 2.0), int(img_h / 2.0)

    position = [0,0]
    relative_size = 0
    boundRect = []
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
            cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), 
                (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        print(int(boundRect[i][0]))
        print(int(boundRect[i][1]))
        print(int(boundRect[i][0])+int(boundRect[i][2]))
        print(int(boundRect[i][1])+int(boundRect[i][3]))
        print(img_h)
        #calculate center of rectangle
        rect_center = [int((boundRect[i][0] + (boundRect[i][0] + boundRect[i][2])) / 2.0),int(boundRect[i][1] + boundRect[i][3] / 2.0)]
        #draw the center of rectangle (yellow)
        cv2.circle(drawing, (rect_center), 5, (0, 255, 255), -1)
        #draw the center of image (orange)
        cv2.circle(drawing, (img_center), 5, (0, 100, 255), -1)
        #line between these two points
        cv2.line(drawing, (rect_center), (img_center), (255, 0, 0), thickness=3, lineType=8)

        distance = str(int(math.hypot(rect_center[0] - img_center[0], rect_center[1] - img_center[1])))
        cv2.putText(drawing,distance,(rect_center[0],rect_center[1]+img_center[1]//20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

        position = [int(rect_center[0] - img_center[0]), int(img_center[1] - rect_center[1])]
        print("position :" + str(position))
        cv2.putText(drawing,"Horizontal: " + str(position[0]),(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(drawing,"Vertical: " + str(position[1]),(10,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2,cv2.LINE_AA)
        rectArea=int(boundRect[i][2]*boundRect[i][3])
        print(rectArea)
        imgArea = img_h*img_w
        print(imgArea)
        relative_size = rectArea/imgArea
        print(relative_size)



    #while True:
#
    #
    #    cv2.imshow("rectangles", drawing)
    #    cv2.imshow("original", output)
#
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break

    return drawing, position, relative_size


#contourSquares(cv2.imread('green.jpeg'))