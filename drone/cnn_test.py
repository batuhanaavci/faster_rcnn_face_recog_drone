from distutils.log import error
from ftplib import error_temp
import rclpy
from rclpy.node import Node
import cv2

from cv_bridge import CvBridge
import time
from mtcnn import MTCNN

from sensor_msgs.msg import Image

from geometry_msgs.msg import Twist
 
from sensor_msgs.msg import Joy

bridge = CvBridge()


class PidController:
    def __init__(self):
        self.Kp_y = -0.1
        self.Kp_z = -0.6
    def kp_controller(self, error):
        error_z = float(error[1])/230
        error_y = float(error[0])/130

        return (self.Kp_y * error_y, self.Kp_z * error_z)




class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.detector = MTCNN()
        
        # self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        # self.joy_sub

        # self.joy_pub = self.create_publisher(Joy, 'joy', 10)
        # self.joy_pub
        
        self.subscription = self.create_subscription(
            Image,
            'image_raw',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription  # prevent unused variable warning
        self.twist = Twist()
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timmer_callback)
        self.pid_button = 1

        self.PidController = PidController()
    
    # def joy_callback(self, msg):
    #     self.pid_button = msg.buttons[5]
    #     msg.axes[4] = self.twist.linear.y
    #     self.joy_pub.publish(msg)

    def timmer_callback(self):
        if self.pid_button == 1:
            self.publisher_.publish(self.twist)
            self.get_logger().info('Publishing: "%s"' % self.twist)

    def listener_callback(self, msg):

        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        cv_image = cv2.resize(cv_image, (460, 259), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        faces = self.detector.detect_faces(gray)
            
        if len(faces) > 0:
            cv2.circle(cv_image,faces[0]['keypoints']['nose'],radius=10,color=(0, 0, 255), thickness=-1)
            cv2.line(cv_image,faces[0]['keypoints']['nose'],(230,130),color=(0, 0, 255), thickness=1)
            # cv2.putText(cv_image, str(faces[0]['confidence']), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(cv_image, 'Guvenlik Acik'+str(self.pid_button), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            error_y = faces[0]['keypoints']['nose'][0]-230
            error_z = faces[0]['keypoints']['nose'][1]-130
            error_tuple = (error_y,error_z)
            cv2.putText(cv_image, str(error_tuple), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            axis = self.PidController.kp_controller(error_tuple)
            cv2.putText(cv_image, str(axis), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            self.twist.linear.y = axis[0]
            self.twist.linear.z = axis[1]
        else:
            self.twist.linear.y = float(0)
            self.twist.linear.z = float(0)
        cv2.imshow("Detection",cv_image)
        cv2.waitKey(3)

def main(args=None):
    
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


