#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, Float32

rVel=0;
lVel=0;
gyroRaw=0;


def gyroCallback(msg):
    rospy.loginfo("I heard %s" % msg.data)
    
def lVelCallback(msg):
	lVel=msg.data
	rospy.loginfo("I heard %s" % lVel)
    
def rVelCallback(msg):
	rVel=msg.data
	rospy.loginfo("I heard %s" % rVel)


def gyro():
    rospy.init_node('gyro2imu')
    rospy.Subscriber("gyro_val", Int16, gyroCallback)
    rospy.Subscriber("lwheel_vel", Float32, lVelCallback);
    rospy.Subscriber("rwheel_vel", Float32, rVelCallback);
    rospy.spin()


if __name__ == '__main__':
    gyro()
