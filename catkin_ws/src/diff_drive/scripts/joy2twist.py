#!/usr/bin/env python

import roslib; roslib.load_manifest('diff_drive')
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


LINEAR_SPEED = 0.3
ANGULAR_SPEED = 1.2

class Joy2Twist(object):
    """Joy2Twist ROS Node"""
    def __init__(self):
        # Initialize the Node
        rospy.init_node("Joy2Twist")
        
        # Setup the Joy topic subscription
        self.joy_subscriber = rospy.Subscriber('joy', Joy, self.handleJoyMessage)
        
        # Setup the Twist topic publisher
        self.twist_publisher = rospy.Publisher('twist', Twist)
        
        # Spin
        rospy.spin()
    
    
    def handleJoyMessage(self, data):
        """Handles incoming Joy messages"""
        msg = Twist()
        msg.linear.x = data.axes[1] * LINEAR_SPEED * (1 + data.axes[8]*-6)
        msg.angular.z = data.axes[0] * ANGULAR_SPEED * (1 + data.axes[8]*-6)
        self.twist_publisher.publish(msg)
 
### If Main ###
if __name__ == '__main__':
        Joy2Twist()
