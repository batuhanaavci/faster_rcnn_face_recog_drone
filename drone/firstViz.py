
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
        self.test_subscription = self.create_subscription(
            Float32,
            'test_publisher',
            self.test_callback,
            10
        )

        self.test_subscription

    def test_callback(self,msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

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

