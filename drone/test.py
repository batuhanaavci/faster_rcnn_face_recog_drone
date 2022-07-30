from glob import glob
from sre_constants import GROUPREF_LOC_IGNORE
import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge
import cv2
import time 
from sensor_msgs.msg import Image
bridge = CvBridge()

global rframe
rframe = 11
global faces

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        
        
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.subscription = self.create_subscription(
            Image,
            'image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        

        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        
        
        (rows,cols,channels) = cv_image.shape

        global rframe
        rframe +=1
        if  rframe > 10:
            
            rframe = 0
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            global faces
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5,
            minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        

        cv2.imshow("asdada",cv_image)
        cv2.waitKey(3)

def main(args=None):
    
<<<<<<< HEAD
    print("asdasda")
=======

>>>>>>> bc3132788d894da69f0270f20b7757533e3e3070
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