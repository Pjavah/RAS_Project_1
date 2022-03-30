from gettingcontours import contourSquares
import cv2
#

#use ros2 node from topics

#tello = Tello()

#img = tello.get_frame_read()
img = cv2.imread('./pictures/square16.jpeg')

cv2.imshow(img.frame)

cv2.waitKey(1)

contourSquares(img.frame)