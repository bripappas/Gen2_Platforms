#!/usr/bin/env python

import roslib; roslib.load_manifest('gen2_joystick')
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


LINEAR_SPEED = 0.3			#maximum normal linear speed (m/s)
ANGULAR_SPEED = 1.2			#maximum normal angualr speed (rad/s)
MODE = 0					#Mode selects which topic to publish to				

#The Joy2MultiRobot node
class Joy2MultiRobot(object):
    def __init__(self):
        # Initialize the Node
        rospy.init_node("Joy2MultiRobot")
        
        # Setup the Joy topic subscription
        self.joy_subscriber = rospy.Subscriber('joy', Joy, self.handleJoyMessage)
        
        # Setup the multiple Twist topic publishers
        self.twist_publisher_0 = rospy.Publisher('twist_0', Twist)
        self.twist_publisher_1 = rospy.Publisher('twist_1', Twist)
        self.twist_publisher_2 = rospy.Publisher('twist_2', Twist)
        self.twist_publisher_3 = rospy.Publisher('twist_3', Twist)
        
        # Spin
        rospy.spin()
    
    #callback is called each time the joystick state changes
    def handleJoyMessage(self, data):
		global MODE
		if data.buttons[7] and MODE!=0:
			MODE = 0; 
			rospy.loginfo("Output 0 selected")
		if data.buttons[4] and MODE!=1:
			MODE = 1; 
			rospy.loginfo("Output 1 selected")
		if data.buttons[5] and MODE!=2:
			MODE = 2; 
			rospy.loginfo("Output 2 selected")
		if data.buttons[6] and MODE!=3:
			MODE = 3; 
			rospy.loginfo("Output 3 selected")
		msg = Twist()
		msg.linear.x = data.axes[1] * LINEAR_SPEED * (1 + data.axes[8]*-6)
		msg.angular.z = data.axes[0] * ANGULAR_SPEED * (1 + data.axes[8]*-6)
		
		if MODE==0:
			self.twist_publisher_0.publish(msg)
		if MODE==1:
			self.twist_publisher_1.publish(msg)
		if MODE==2:
			self.twist_publisher_2.publish(msg)
		if MODE==3:
			self.twist_publisher_3.publish(msg)
				
### If Main ###
if __name__ == '__main__':
        Joy2MultiRobot()
