from array import array
from distutils.log import error
from ftplib import error_temp
from tkinter import Y
import rclpy
from rclpy.node import Node
import cv2
import math  

from cv_bridge import CvBridge
import time
from mtcnn import MTCNN

from sensor_msgs.msg import Image

from geometry_msgs.msg import Twist
 
from sensor_msgs.msg import Joy

bridge = CvBridge()

import numpy as np

class PidController:
    def __init__(self):
        self.Kp = 0.4
        self.Kd = 0.6
        self.normalized = []
        self.refy = 0
        self.refz = 0
        self.refx = 0
        self.Az = 0
        self.Ay = 0
        self.Ax = 0
        self.last_errz = 0
        self.last_erry = 0
        self.last_errx = 0
        self.dt = 1

    def preprocess(self, box):
        
        z = (box[1] - 130)/130
        y = (box[0] - 260)/260
        x = (box[2] - 10000)/10000
        #left_eye_z = (keypoint['left_eye'][1] - 130)/130
        #left_eye_y = (keypoint['left_eye'][0] - 260)/260
        #right_eye_z = (keypoint['right_eye'][1] - 130)/130
        #right_eye_y = (keypoint['right_eye'][0] - 260)/260
        #eye_dist = math.dist([left_eye_z, left_eye_y], [right_eye_z, right_eye_y])
        #eye_error = eye_dist - 0.03
        #eye_error = (eye_error - 0.25) / 0.25
        return z,y,x #eye_error


    def controller(self, target):
        targetz,targety,targetx= self.preprocess(target)
        errz = targetz-self.refz
        erry = targety-self.refy
        errx = targetx-self.refx
        
        self.Az += self.dt* (errz+self.last_errz)/2
        Pz = errz * self.Kp
        Dz = self.Kd*(errz - self.last_errz) / self.dt
        uz = Pz + Dz
        self.last_errz = errz

        self.Ay += self.dt* (erry+self.last_erry)/2
        Py = erry * self.Kp
        Dy = self.Kd*(erry - self.last_erry) / self.dt
        uy = Py + Dy
        self.last_erry = erry

        self.Ax += self.dt* (errx+self.last_errx)/2
        Px = errx * self.Kp
        Dx = self.Kd*(errx - self.last_errx) / self.dt
        ux = Px + Dx
        self.last_errx = errx





        # uy = math.tanh(uy)
        # uz = math.tanh(uz)

        return uz,uy,ux #eye_error





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
        self.center_box = np.array([230,130])  # center coordinates of the reference box (y,z)
        self.rbox_y = self.center_box[0]
        self.rbox_z = self.center_box[1]
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
            box_x, box_y, box_width, box_height = faces[0]['box']
            box_center_x , box_center_y= ((box_x+int(box_width/2)), int((box_y+int(box_height/2))))
            face_area = box_height*box_width
            ref_box_area = ((self.rbox_y+20)-(self.rbox_y-20))*((self.rbox_z+20)-(self.rbox_z-20))
            
            #cv2.circle(cv_image,faces[0]['keypoints']['nose'],radius=5,color=(0, 0, 255), thickness=-1)
            #cv2.circle(cv_image,faces[0]['keypoints']['left_eye'],radius=5,color=(0, 0, 255), thickness=-1)
            #cv2.circle(cv_image,faces[0]['keypoints']['right_eye'],radius=5,color=(0, 0, 255), thickness=-1)
            cv2.rectangle(cv_image,(box_x,box_y),(box_x+box_width,box_y+box_height),(0,255,0), thickness=1)  # detected face
            cv2.rectangle(cv_image,(self.rbox_y-20,self.rbox_z-20),(self.rbox_y+20,self.rbox_z+20),(255,0,0), thickness=1)  # ref_box  
            #cv2.putText(cv_image, 'ref_box_area'+str(ref_box_area), (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            #cv2.putText(cv_image, 'face_area'+str(face_area), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            

            cv2.line(cv_image,(box_center_x,box_center_y),(230,130),color=(0, 0, 255), thickness=1)
            # cv2.putText(cv_image, str(faces[0]['confidence']), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(cv_image, 'Guvenlik Acik'+str(self.pid_button), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            target = np.array([box_center_x,box_center_y, face_area])
            error_y = box_center_x-230
            error_z = box_center_y-130
            error_x = face_area - ref_box_area 
            error_tuple = (error_y,error_z,error_x)
            cv2.putText(cv_image, str(error_tuple), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            uz,uy, ux = self.PidController.controller(target)
            cv2.putText(cv_image, "{:.2f}".format(uz)+"---{:.2f}".format(uy)+"---{:.2f}".format(ux), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1, cv2.LINE_AA)
            #cv2.putText(cv_image, "{:.2f}".format(eye_dist), (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1, cv2.LINE_AA)
            #cv2.putText(cv_image, 'X AXIS COMMAND'+str(ux), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

            self.twist.linear.z = -uz
            self.twist.angular.z = -uy
            self.twist.linear.x -ux
            #cv2.putText(cv_image, 'twistX'+str(self.twist.linear.x), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # else:
        #     pass
        #     self.twist.linear.y = float(0)
        #     self.twist.linear.z = float(0)

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


