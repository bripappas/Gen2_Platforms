#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import tf
import std_msgs.msg
from sensor_msgs.msg import LaserScan
import math
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion

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
	global listener,trans,rot
	laserScan = []
	angle_min = []
	angle_max = []
	angle_inc = []
	xList = []
	yList = []
	xListXfrm =[]
	yListXfrm =[]
	laserScan = data.ranges
	angle_min = data.angle_min
	angle_max = data.angle_max
	angle_inc = data.angle_increment
	laserList = list(laserScan)
	
	#Find (x,y) coordinates of Laser Scanner centered in the Lidar Frame
	for i in range(len(laserList)):
		xList.append(-math.sin((angle_min+(angle_inc*i)))*laserList[i])
		yList.append(math.cos((angle_min+(angle_inc*i)))*laserList[i])
		
	#Transform (x,y) coordinates from Lidar Fram to global frame
	try:
		(trans,quat) = listener.lookupTransform('/map','/robot_0/base_laser_link', rospy.Time())
	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print 'TF Lookup Failed'
		
	#Convert Cooridinates to map frame cartesian coordiantes(meters)
	(roll,pitch,yaw) = euler_from_quaternion(quat)
	for i in range(len(laserList)):
		yListXfrm.append(trans[1]+(-xList[i]*math.cos(-yaw)+yList[i]*math.sin(-yaw)))
		xListXfrm.append(trans[0]+(-xList[i]*math.sin(-yaw)-yList[i]*math.cos(-yaw)))
		
	print xListXfrm[0]
	print yListXfrm[0]
	
	#Pull out needed map paramters
	#width=mapData.info.width
	#height=mapData.info.height
	#resolution=mapData.info.resolution
	
	#Pull out current robot position
	#robX=data.pose.pose.position.x*(1.0/resolution)+width/2
	#robY=data.pose.pose.position.y*(1.0/resolution)+height/2
	
		

		
		
	
				
### If Main ###
if __name__ == '__main__':
        robotSenseBoundary()
