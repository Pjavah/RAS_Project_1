import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import math

desired_aruco_dictionary = cv2.aruco.DICT_4X4_50
this_aruco_dictionary = cv2.aruco.Dictionary_get(desired_aruco_dictionary)
this_aruco_parameters = cv2.aruco.DetectorParameters_create()

# frame = cv2.imread('.\\pictures\\aruco1.jpeg')

def markAruco(frame):

# Detect ArUco markers in the video frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        frame, this_aruco_dictionary, parameters=this_aruco_parameters)

# Check that at least one ArUco marker was detected
    qr_center = []
    qr_left = qr_right = qr_top = qr_bottom = 0
    frame_height, frame_width, channels = frame.shape
    frame_center = int(frame_width / 2.0), int(frame_height / 2.0)
    position = []
    qr_distance_points = [0,0,0,0]
    qr_distance = 0
    if len(corners) > 0:
        # Flatten the ArUco IDs list
        ids = ids.flatten()
        
        # Loop over the detected ArUco corners
        for (marker_corner, marker_id) in zip(corners, ids):
            # Extract the marker corners
            corners = marker_corner.reshape((4, 2))
            (top_left, top_right, bottom_right, bottom_left) = corners
                
            # Convert the (x,y) coordinate pairs to integers
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
            top_left = (int(top_left[0]), int(top_left[1]))
                
            # Draw the bounding box of the ArUco detection
            cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
            cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
            cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
            cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)
                
            # Calculate and draw the center of the ArUco marker
            center_x = int((top_left[0] + bottom_right[0]) / 2.0)
            center_y = int((top_left[1] + bottom_right[1]) / 2.0)

            if (marker_id == 1):
                qr_distance_points[0] = center_x
                qr_distance_points[1] = center_y
            if (marker_id == 2):
                qr_distance_points[2] = center_x
                qr_distance_points[3] = center_y
            cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

            if qr_left == 0:
                qr_left = qr_right = center_x
                qr_bottom = qr_top = center_y

            if qr_left != 0 and center_x < qr_left :
                qr_left = center_x
            if qr_right != 0 and center_x > qr_right :
                qr_right = center_x
            if qr_top != 0 and center_y < qr_top :
                qr_top = center_y
            if qr_bottom != 0 and center_y > qr_bottom :
                qr_bottom = center_y

                
            # Draw the ArUco marker ID on the video frame
            # The ID is always located at the top_left of the ArUco marker
            cv2.putText(frame, str(marker_id), 
                (top_left[0], top_left[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)

    # Calculate and draw the center of all markers
    qr_center = [int((qr_left + qr_right) / 2.0),int((qr_top + qr_bottom) / 2.0)]
    cv2.circle(frame, (qr_center), 10, (0, 255, 255), -1)
    # Draw the frame center
    cv2.circle(frame, (frame_center), 10, (0, 255, 0), -1)

    # Draw a line from qr center to frame center
    cv2.line(frame, (qr_center), (frame_center), (255, 0, 0), thickness=3, lineType=8)
    distance = str(int(math.hypot(qr_center[0] - frame_center[0], qr_center[1] - frame_center[1])))
    cv2.putText(frame,distance,(qr_center[0],qr_center[1]+frame_center[1]//20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

    # Laskee miten paljon pitäisi liikkua sivulle ja ylös
    position = [int(qr_center[0] - frame_center[0]), int(frame_center[1] - qr_center[1])]
    cv2.putText(frame,"Horizontal: " + str(position[0]),(10,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Vertical: " + str(position[1]),(10,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

    if (qr_distance_points[0] != 0 and qr_distance_points[1] != 0 and qr_distance_points[2] != 0 and qr_distance_points[3] != 0):
        # Lasketaan qr merkkien etäisyys
        qr_distance = math.hypot(qr_distance_points[0] - qr_distance_points[2], qr_distance_points[1] - qr_distance_points[3]) / frame_height
        cv2.putText(frame,"Qr koodien osuus korkeudesta: ",(10,150), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,str(qr_distance),(10,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imwrite('output.jpeg', frame)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return frame, position, qr_distance

# markAruco(frame)