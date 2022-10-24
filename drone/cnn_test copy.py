import rclpy
from rclpy.node import Node
import cv2
import math  
# import panda as pd
from cv_bridge import CvBridge
import time
from mtcnn import MTCNN
import json
from sensor_msgs.msg import Image

from geometry_msgs.msg import Twist
from std_msgs.msg import String
 
from sensor_msgs.msg import Joy

bridge = CvBridge()

import numpy as np
class PidController:
    def __init__(self):
        self.Kpy = 0.5
        self.Kdy = 0.3
        self.Kpz = 0.4
        self.Kdz = 0.5
        self.Kpx = 0.7
        self.Kdx = 0.4
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
        self.last_posy = 0
        self.last_posz = 0
        self.last_posx = 0
        self.dt = 1

    def preprocess(self, box):
        z = (box[1] - 130)/130
        y = (box[0] - 260)/260
        min_value = 25  # this is      the minimum value of the distance, i.e. distance measured when the face is furthest away from drone.
        x = ((box[2]+min_value) - 25)/25

        return z,y,x #normalized error

    def controller(self, target):
        targetz,targety,targetx= self.preprocess(target)
        errz = targetz-self.refz
        erry = targety-self.refy
        errx = targetx - self.refx
        
        self.Az += self.dt* (errz+self.last_errz)/2
        Pz = errz * self.Kpz
        Dz = self.Kdz*(errz - self.last_errz) / self.dt
        uz = Pz + Dz
        self.last_errz = errz

        self.Ay += self.dt* (erry+self.last_erry)/2
        Py = erry * self.Kpy
        Dy = self.Kdy*(erry - self.last_erry) / self.dt
        uy = Py + Dy
        self.last_erry = erry

        self.Ax += self.dt* (errx+self.last_errx)/2
        Px = errx * self.Kpx
        Dx = self.Kdx*(errx - self.last_errx) / self.dt
        ux = Px + Dx
        self.last_errx = errx

        return uz,uy,ux #controller output
    
    def face_velocity(self,target): 
        dt = 1 
        targety,targetz,targetx= target
        
        self.dY = (targety - self.last_posy) / dt
        self.last_posy = targety

        self.dZ = (targetz - self.last_posz) / dt
        self.last_posz = targetz

        return self.dY, self.dZ



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
        
        self.faces_sub = self.create_subscription(
            String,
            'faces',
            self.faces_callback,
            10)
        
        self.faces_sub
        self.faces_data = {}
        self.faces = {}
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
        self.Vy = 1
        self.Vz = 1
    # def joy_callback(self, msg):
    #     self.pid_button = msg.buttons[5]
    #     msg.axes[4] = self.twist.linear.y
    #     self.joy_pub.publish(msg)

    def faces_callback(self, msg):
        faces_data = json.loads(msg.data)
        print(faces_data)
        print(type(faces_data['labels']))

        if type(faces_data['labels']) == str:
            self.faces[1] = dict()
            self.faces[1]['labels'] = faces_data['labels']
            self.faces[1]['boxes'] = faces_data['boxes']
            self.faces[1]['scores'] = faces_data['scores']
            
        else:
            for i in range(len(faces_data['labels'])):
                self.faces[i] = dict()
                self.faces[i]['labels'] = faces_data['labels'][i]
                self.faces[i]['box'] = faces_data['boxes'][i]
                self.faces[i]['scores'] = faces_data['scores'][i]

        

        self.get_logger().info('I heard: "%s"' % str(self.faces))


    def timmer_callback(self):
        if self.pid_button == 1:
            self.publisher_.publish(self.twist)
            # self.get_logger().info('Publishing: "%s"' % self.twist)

    def detect_faces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces=self.detector.detect_faces(gray)
        print(faces)
        return faces

    def listener_callback(self, msg):
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        cv_image = cv2.resize(cv_image, (460, 259), interpolation = cv2.INTER_AREA)



        _Kref = 20  # reference box constant, half of the reference box's one side

        # if len(faces) > 0:
        #     box_x, box_y, box_width, box_height = faces[0]['box']
        #     box_center_x , box_center_y= ((box_x+int(box_width/2)), int((box_y+int(box_height/2))))
            
        #     cv2.rectangle(cv_image,(box_x,box_y),(box_x+box_width,box_y+box_height),(0,255,0), thickness=1)  # detected face
        #     cv2.rectangle(cv_image,(box_center_x-_Kref,box_center_y-_Kref),(box_center_x+_Kref,box_center_y+_Kref),(255,0,0), thickness=1)  # ref_box  
        #     cv2.line(cv_image,(box_center_x,box_center_y),(230,130),color=(0, 0, 255), thickness=1)
        #     cv2.putText(cv_image, 'Guvenlik Acik'+str(self.pid_button), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        #     error_y = box_center_x-230
        #     error_z = box_center_y-130
        #     d = (box_center_x-_Kref) - box_x
        #     error_tuple = (error_y,error_z,d)

        #     target = np.array([box_center_x,box_center_y, d])
            
        #     cv2.putText(cv_image, str(error_tuple), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        #     uz,uy,ux = self.PidController.controller(target)
            
        #     cv2.putText(cv_image, "{:.2f}".format(uz)+"---{:.2f}".format(uy)+"---{:.2f}".format(ux), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1, cv2.LINE_AA)

        #     self.twist.linear.z = -uz
        #     self.twist.angular.z = -uy
        #     self.twist.linear.x = -ux
        
        #     self.Vy, self.Vz = self.PidController.face_velocity(target)
        #     #cv2.putText(cv_image, "{:.2f}".format(self.Vy)+"---{:.2f}".format(self.Vz), (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1, cv2.LINE_AA)
        # if len(faces) <= 0 :
        #     uy2 = ((self.Vy+50) - 50)/50 # normalize command between -1 and 1
        #     self.twist.angular.z = -uy2

        #     cv2.putText(cv_image, "{:.2f}".format(self.Vy)+"---{:.2f}".format(uy2), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1, cv2.LINE_AA)
            

        # else:
        #     pass
        #     self.twist.linear.y = float(0)
        #     self.twist.linear.z = float(0)

        cv2.imshow("Detection",cv_image)
        cv2.waitKey(3)
    def test(self):
        data = pd.DataFrame(np.random.randn(20, 2), columns=['a', 'b'])
        return data


def main(args=None):
    
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


