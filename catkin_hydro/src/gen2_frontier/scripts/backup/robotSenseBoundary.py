#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import tf
import std_msgs.msg
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseWithCovarianceStamped, PolygonStamped, Point32
from tf.transformations import euler_from_quaternion
import math

#Initialize ROS node and setup up Publisher/Subscribers
def robotSenseBoundary():
	global listener, lidarPointsPub
	
	# Initialize the Node
	rospy.init_node('robotSenseBoundary')
	
	#Setup tf Listenr for Lidar->Map transform
	listener = tf.TransformListener()
	
	# Setup Subscribers
	laserSub = rospy.Subscriber('base_scan',LaserScan,handleLaserScanMessage,queue_size = 1)
	
	# Setup Publishers
	lidarPointsPub = rospy.Publisher('lidarInMap',PolygonStamped)
	rospy.spin()
	
#Convert LaserScan readings into discrete map coordinates and publish as polygon
def handleLaserScanMessage(data):
	global listener,trans,quat, lidarPointsPub
	xListXfrm =[]
	yListXfrm =[]
	angle_min = data.angle_min
	angle_max = data.angle_max
	angle_inc = data.angle_increment
	range_max = data.range_max
	laserList = list(data.ranges)
		
	#Look up transfrom from Lidar to map
	try:
		(trans,quat) = listener.lookupTransform('/map',rospy.get_param('lidarLinkFrame'), rospy.Time())
	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print 'TF Lookup Failed'
		return
		
	lidarPoints = PolygonStamped()
	#Convert Lidar Cooridinates to map frame cartesian coordiantes(meters)
	(roll,pitch,yaw) = euler_from_quaternion(quat)
	for i in range(len(laserList)):
		xi = math.sin((angle_min+(angle_inc*i)))*laserList[i]
		yi = -math.cos((angle_min+(angle_inc*i)))*laserList[i]
		xi_Xfrm = trans[0]+(xi*math.sin(-yaw)-yi*math.cos(-yaw))
		yi_Xfrm = trans[1]+(xi*math.cos(-yaw)+yi*math.sin(-yaw))
		point_i=Point32()
		point_i.x = xi_Xfrm
		point_i.y = yi_Xfrm;
		lidarPoints.polygon.points.append(point_i)
	
	lidarPoints.header.stamp=rospy.Time.now()
	lidarPoints.header.frame_id='/map'	
	lidarPointsPub.publish(lidarPoints)
				
### If Main ###
if __name__ == '__main__':
        robotSenseBoundary()
