import rclpy
from rclpy.node import Node
import cv2
import numpy as np
import sys

from sensor_msgs.msg import Image
from arucomarkers import markAruco

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
        self.image_sub = self.create_subscription(
            Image, 
            #'/image_raw', 
            "/camera",
            self.cam_callback, 
            10)


    def cam_callback(self, msg):

        self.camcounter += 1
        if(self.camcounter % 5 == 0):
            camList.append(msg)
    
            # Convert ROS Image message to OpenCV2
            cv2_img = self.imgmsg_to_cv2(msg)
            #markAruco(cv2_img)
            frame, position, qr_distance = markAruco(cv2_img)
            cv2.imshow("Result",frame)
            cv2.waitKey(1)
            #cv2.destroyAllWindows()

            if(qr_distance > 0.8 and abs(position[0]) < 50 and abs(position[1]) < 50):
                print("forward!!")

            

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
