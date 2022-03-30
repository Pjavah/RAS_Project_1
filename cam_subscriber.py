import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import String


class CamSubscriber(Node):

#    def __init__(self):
 #       super().__init__('camera_subscriber')
  #      self.subscription = self.create_subscription(
   #         String,
    #        'topic',
     #       self.listener_callback,
      #      10)
       # self.subscription  # prevent unused variable warning

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

   # def listener_callback(self, msg):
    #    self.get_logger().info('I heard: "%s"' % msg.data)



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