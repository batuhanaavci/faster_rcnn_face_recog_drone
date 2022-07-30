import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
import cv2
import time
from mtcnn import MTCNN

from sensor_msgs.msg import Image
bridge = CvBridge()

global rframe
rframe = 11
global faces

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        self.detector = MTCNN()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.subscription = self.create_subscription(
            Image,
            'image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        

        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        cv_image = cv2.resize(cv_image, (460, 259), interpolation = cv2.INTER_AREA)
        
        (rows,cols,channels) = cv_image.shape

        global rframe
        rframe +=1
        if  rframe > 2:
            
            rframe = 0
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            

            global faces
            faces = self.detector.detect_faces(gray)
            
        if len(faces) > 0:
            cv2.circle(cv_image,faces[0]['keypoints']['nose'],radius=10,color=(0, 0, 255), thickness=-1)
        

        cv2.imshow("asdada",cv_image)
        cv2.waitKey(3)

def main(args=None):
    
    print("asdasda")
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()