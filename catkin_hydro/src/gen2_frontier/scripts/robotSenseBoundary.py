#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import tf
import std_msgs.msg
from sensor_msgs.msg import LaserScan
import math
from geometry_msgs.msg import PoseWithCovarianceStamped

robX = []  #Robot X Position
robY = []  #Robot Y Position

#Initialize ROS node and setup up Publisher/Subscribers
def robotSenseBoundary():
	global listener
	
	# Initialize the Node
	rospy.init_node('robotSenseBoundary')
	
	#Setup tf Listenr for Lidar->Map transform
	listener = tf.TransformListener()
	
	# Setup Subscribers
	amclPoseSub = rospy.Subscriber('robot_0/amcl_pose',PoseWithCovarianceStamped,handlePoseMessage,queue_size = 1)
	laserSub = rospy.Subscriber('/robot_0/base_scan',LaserScan,handleLaserScanMessage,queue_size = 1)
	
	# Setup Publishers
	#robotSearchedPub = rospy.Publisher('robotSearched',OccupancyGrid)
	
	
	
	rospy.spin()
	
def handlePoseMessage(data):
	#Pull out current robot position to map coordinates
	global robX
	global robY
	robX=data.pose.pose.position.x
	robY=data.pose.pose.position.y
	
def handleLaserScanMessage(data):
	global listener
	laserScan = []
	angle_min = []
	angle_max = []
	angle_inc = []
	xList = []
	yList = []
	laserScan = data.ranges
	angle_min = data.angle_min
	angle_max = data.angle_max
	angle_inc = data.angle_increment
	laserList = list(laserScan)
	
	#Find (x,y) coordinates of Laser Scanner centered in the Lidar Frame
	for i in range(len(laserList)):
		xList.append(math.sin((angle_min+(angle_inc*i))))
		yList.append(math.cos((angle_min+(angle_inc*i))))
		
	#Transform (x,y) coordinates from Lidar Fram to global frame
	try:
		(trans,rot) = listener.lookupTransform('/robot_0/base_laser_link', '/map', rospy.Time())
	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print 'TF Lookup Failed'
		
	print rot
	print trans
		
		
	
				
### If Main ###
if __name__ == '__main__':
        robotSenseBoundary()
