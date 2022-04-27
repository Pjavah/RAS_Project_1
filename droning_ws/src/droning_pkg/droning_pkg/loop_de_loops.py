import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import sys
import time

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Empty
from arucomarkers import markAruco
from gettingcontours import contourSquares

camList = []

desired_aruco_dictionary = cv2.aruco.DICT_4X4_50
this_aruco_dictionary = cv2.aruco.Dictionary_get(desired_aruco_dictionary)
this_aruco_parameters = cv2.aruco.DetectorParameters_create()



class CamSubscriber(Node):
    camcounter = 0
    

    def __init__(self):
        super().__init__('image_listener')
        
        self.cnt = 0
        #self.shape.array = []
        self.image_sub = self.create_subscription(Image, "/camera",self.cam_callback, 10)
        self.cmdvel_publisher = self.create_publisher(Twist, '/control', 10)   #'/cmd_vel
        self.land_publisher = self.create_publisher(Empty, '/land', 10)
        self.through = 0
        self.start = 1

    def cam_callback(self, msg):                                                             

        self.camcounter += 1
        if(self.camcounter % 5 == 0):
            camList.append(msg)
    
            # Convert ROS Image message to OpenCV2
            cv2_img = self.imgmsg_to_cv2(msg)
            #markAruco(cv2_img)
            frame, position, qr_distance = markAruco(cv2_img)
            drawing, position_sq, relative_size = contourSquares(cv2_img)

        

            if(self.start):
                end_time = time.time()+13
                msg = Twist()
                msg.linear.z = 16.0
                msg.angular.z = 0.0
                print("starting position")
                self.start=0
                while(time.time() < end_time):
                    self.cmdvel_publisher.publish(msg)
                    print("UPUPUP!")
                    time.sleep(0.2)

            #First through qr gate
            if self.through == 0:
                print(position)
                cv2.imshow("Result",frame)
                cv2.waitKey(1)
                #Moving towards the center
                if(-30 > position[0] > -480):
                    print("moving X to center")
                    msg = Twist()
                    msg.linear.x = -10.0
                    self.cmdvel_publisher.publish(msg)
                if(30 < position[0]):
                    print("Moving X to center from negative")
                    msg = Twist()
                    msg.linear.x = 10.0
                    self.cmdvel_publisher.publish(msg)
                if(150 < position[1] < 360):
                    print("Going vertically up")
                    msg = Twist()
                    msg.linear.z = 15.0
                    self.cmdvel_publisher.publish(msg)
                if(100 > position[1]):
                    print("Going vertically down")
                    msg = Twist()
                    msg.linear.z = -15.0
                    self.cmdvel_publisher.publish(msg)
                if(qr_distance < 0.8 and abs(position[0])<100 and abs(position[1])<190):
                    print("Going forward closer to gate!")
                    msg = Twist()
                    msg.linear.y = 15.0
                    self.cmdvel_publisher.publish(msg)

                if(qr_distance > 0.75 and abs(position[0])<100 and abs(position[1])<190):
                    msg = Twist()
                    msg.linear.y = 22.0
                    end_time = time.time()+6.5
                    while(time.time() < end_time):
                        self.cmdvel_publisher.publish(msg)
                        print("Going through gate!")
                        time.sleep(0.2)
                        
                    self.through = 1

            #second the colored gate
            if(self.through==1):
                
                cv2.imshow("Result",drawing)
                cv2.waitKey(1)
                print(position_sq)
                if(position_sq == [0,0]):
                    print("can't see nuffin, spinning around and up?")
                    msg = Twist()
                    msg.angular.z = -15.0
                    msg.linear.z = 5.0
                    self.cmdvel_publisher.publish(msg)

                #Moving towards the center
                elif(-30 > position_sq[0] > -480):
                    print("moving X to center")
                    msg = Twist()
                    msg.linear.x = -10.0
                    self.cmdvel_publisher.publish(msg)
                elif(30 < position_sq[0]):
                    print("Moving X to center from negative")
                    msg = Twist()
                    msg.linear.x = 10.0
                    self.cmdvel_publisher.publish(msg)
                elif(100 < position_sq[1] < 360):
                    print("Going vertically up")
                    msg = Twist()
                    msg.linear.z = 15.0
                    self.cmdvel_publisher.publish(msg)
                elif(50 > position_sq[1]):
                    print("Going vertically down")
                    msg = Twist()
                    msg.linear.z = -15.0
                    self.cmdvel_publisher.publish(msg)
                elif(relative_size < 0.8 and abs(position_sq[0])<100 and abs(position_sq[1])<190):
                    print("Going forward closer to gate!")
                    msg = Twist()
                    msg.linear.y = 15.0
                    self.cmdvel_publisher.publish(msg)

                print(relative_size)

                if(relative_size > 0.50 and abs(position_sq[0])<100 and abs(position_sq[1])<190):
                    msg = Twist()
                    msg.linear.y = 22.0
                    end_time = time.time()+7
                    while(time.time() < end_time):
                        self.cmdvel_publisher.publish(msg)
                        print("Going through gate!")
                        time.sleep(0.2)
                        
                    self.through = 2

            if(self.through==2):
                print("And now landing?")
                msg1 = Twist()
                msg1.linear.z = 0.0
                msg1.linear.x = 0.0
                msg1.linear.y = 0.0
                self.cmdvel_publisher.publish(msg1)
                msg = Empty()
                self.land_publisher.publish(msg)
                #print("found nothing?")
                

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


def main(args=None):

    rclpy.init(args=args)
    camera_subscriber = CamSubscriber()
    rclpy.spin(camera_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
