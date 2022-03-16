import cv2
import numpy as np

img = cv2.imread('./pictures/square4.jpeg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_bound = np.array([0, 220, 150])   
upper_bound = np.array([14, 255, 200])
# find the colors within the boundaries
mask = cv2.inRange(hsv, lower_bound, upper_bound)

kernel = np.ones((7,7),np.uint8)
# Remove unnecessary noise from mask
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Segment only the detected region
segmented_img = cv2.bitwise_and(img, img, mask=mask)

contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)
# Showing the output
cv2.imshow("Output", output)
cv2.imwrite('output.jpeg', output)
cv2.waitKey(0)
cv2.destroyAllWindows()