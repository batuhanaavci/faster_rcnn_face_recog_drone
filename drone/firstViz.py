
import streamlit as st
import numpy as np
import pandas as pd
import rclpy
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from rclpy.node import Node
import matplotlib.pyplot as plt



class ErrorSubscriber(Node):
    def __init__(self):
        super().__init__('error_subscriber')
        self.error_angular_z_subscription = self.create_subscription(
            Float32,
            'error_angular_z',
            self.error_angular_z_callback,
            10)
        self.error_linear_z_subscription = self.create_subscription(
            Float32,
            'error_linear_z',
            self.error_linear_z_callback,
            10)
        self.error_linear_x_subscription = self.create_subscription(
            Float32,
            'error_linear_x',
            self.error_linear_x_callback,
            10)
        
        self.error_angular_z_subscription # prevent unused variable warning
        self.error_linear_z_subscription
        self.error_linear_x_subscription
        self.arr_err_ang_z = []
        self.arr_err_lin_z = []
        self.arr_err_lin_x = []
        self.chart_ang_z = st.line_chart([])
        self.chart_lin_z = st.line_chart([])
        self.chart_lin_x = st.line_chart([])



    def error_angular_z_callback(self,msg):
        self.error_angular_z = msg.data
        self.arr_err_ang_z.append(self.error_angular_z) 
        np_error = np.array(self.arr_err_ang_z)
        self.chart_ang_z.add_rows(np_error)

    def error_linear_z_callback(self,msg):
        self.error_linear_z = msg.data
        self.arr_err_lin_z.append(self.error_linear_z) 
        np_error = np.array(self.arr_err_lin_z)
        self.chart_lin_z.add_rows(np_error)
    
    def error_linear_x_callback(self,msg):
        self.error_linear_x = msg.data
        self.arr_err_lin_x.append(self.error_linear_x) 
        np_error = np.array(self.arr_err_lin_x)
        self.chart_lin_x.add_rows(np_error)
   
        

def main(args=None):
    
    rclpy.init(args=args)
    error_subscriber = ErrorSubscriber()

    rclpy.spin(error_subscriber)
    error_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':


    main()







## plotting example 

"""
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    last_rows = new_rows
    time.sleep(0.05)
"""

