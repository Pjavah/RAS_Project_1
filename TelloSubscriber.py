import base64
import cv2
import numpy as np
from std_msgs.msg import String
import rclpy
from rclpy.node import Node
import sys
import imutils
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import matplotlib.pyplot as plt



class TelloCamSubscriber(Node):

    def __init__(self):
        super().__init__('image_listener')
        
        self.cnt = 0
        self.shape.array = []

        self.image_sub = self.create_subscription(
            Image, 
            #'/image_raw', 
            "/camera",
            self.shape_cam_callback, 
            10)

        self.shape_publisher = ShapePublisher()


        self.drone_publisher = self.create_publisher( #publishes to /cmd_vel to publish the commands.
            Twist,
            #"/cmd_vel", #or control_vel. If control multiply by 100. 
            "/control",
            10
        )

        self.drone_publisher
        #start by rotating
        
        
        


    def shape_cam_callback(self, msg):

        # Convert ROS Image message to OpenCV2
        cv2_img = self.imgmsg_to_cv2(msg)
        
        hsv = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2HSV) 

        lower_bound = np.array([0, 170, 130])   
        upper_bound = np.array([13, 255, 255])

        # find the colors within the boundaries
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        kernel = np.ones((7,7),np.uint8)
        # Remove unnecessary noise from mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Segment only the detected region
        segmented_img = cv2.bitwise_and(cv2_img, cv2_img, mask=mask)

        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)
        outputS = cv2.resize(output, (960,540)) # resize output image

        cv2.imshow("Output", outputS)
        cv2.imwrite('output.jpeg', outputS)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#Size chart
# 3m 4000
# 2m 6000 - 7000
# 1,5m 17000
# 1m 20000 
#        
        
        #here we determine the moves the drone makes

        if self.face_size < 6000 and (len(faces) == 1):
            #move forwards
            msg = Twist()
            Ly = 0.15*100 #times hundred if if controll
            msg.linear.y = Ly
            self.drone_publisher.publish(msg)
            
            
        
        elif self.face_size > 17000 and (len(faces) == 1):
            #move backwards
            msg = Twist()
            Ly = -0.15*100 #times hundred if if controll
            msg.linear.y = Ly
            self.drone_publisher.publish(msg)
            

        elif(len(faces) != 1):
            #drone rotates if more than one face or no faces are detected
            msg = Twist()
            Az = 0.25*100 #times hundred if if controll
            msg.angular.z = Az
            self.drone_publisher.publish(msg)

        elif():
            # drone positions vertically to match the height the gate is
            msg.Twist()
            Lx = 0.15*100
            msg.linear.x = Lx
            self.drone_publisher.publish(msg)


        
# THIS IS JUST THE IMAGE CONVERSION

    def imgmsg_to_cv2(self, img_msg):
        n_channels = len(img_msg.data) // (img_msg.height * img_msg.width)
        dtype = np.uint8

        img_buf = np.asarray(img_msg.data, dtype=dtype) if isinstance(img_msg.data, list) else img_msg.data

        if n_channels == 1:
            cv2_img = np.ndarray(shape=(img_msg.height, img_msg.width),
                            dtype=dtype, buffer=img_buf)
        else:
            cv2_img = np.ndarray(shape=(img_msg.height, img_msg.width, n_channels),
                            dtype=dtype, buffer=img_buf)

        # If the byte order is different between the message and the system.
        if img_msg.is_bigendian == (sys.byteorder == 'little'):
            cv2_img = cv2_img.byteswap().newbyteorder()

        return cv2_img
    

# THIS PUBLISHES A MESSAGE WHEN THE DRONE FINDS A SHAPE (square)

class ShapePublisher(Node):

    def __init__(self):
        super().__init__("Shape_publisher")
        self.publisher_ = self.create_publisher(String, "/shape_found", 10)
        self.i = 0

    def publish(self):
        msg = String()
        msg.data = "Face has been found!" 
        self.publisher_.publish(msg)
        self.i += 1
        



def main():
    rclpy.init()
    cam_subscriber = TelloCamSubscriber()

    # Spin until ctrl + c
    rclpy.spin(cam_subscriber)
  

    cam_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()