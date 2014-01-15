#!/usr/bin/env python


import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import std_msgs.msg
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.srv import GetMap
from sensor_msgs.msg import LaserScan
import math

mapList = []						#Working array to calculate searched cells
mapData = mapMsg=OccupancyGrid()	#Ocupancy message to hold map data
robotSearchedPub = rospy.Publisher('robotSearched',OccupancyGrid)	#robot specific searched cell


#Initialize ROS node and setup up Publisher/Subscribers
def robotSearched():
	global mapData
	global mapList
	
	# Initialize the Node
	rospy.init_node('robotSearched')
	
	# Create service client to get map from map server
	rospy.loginfo("Waiting for map to become available")
	rospy.wait_for_service('/static_map')
	try:
		getStaticMap = rospy.ServiceProxy('/static_map',GetMap)

		resp = getStaticMap()
		mapData=resp.map
		
	except rospy.ServiceException, e:
		print "Static map service call failed: %s"%e
	
	#Initial map setup, set all open cells to not searced (cell=100) and other cells to -1
	mapList=list(mapData.data)
	for i in range(len(mapList)):
		if mapList[i]==100:
			mapList[i]=-1;
		if mapList[i]==0:
			mapList[i]=100;	
	rospy.loginfo("The static map has been retrieved")
	
	# Setup aSubscribers
	amclPoseSub = rospy.Subscriber('robot_0/amcl_pose',PoseWithCovarianceStamped,handlePoseMessage,queue_size = 1)
	laserSub = rospy.Subscriber('/robot_0/base_scan',LaserScan,handleLaserScanMessage,queue_size = 1)
	
	# Setup Publishers
	#robotSearchedPub = rospy.Publisher('robotSearched',OccupancyGrid)
	
	rospy.spin()
	
def handlePoseMessage(data):
	global mapData
	global mapList
	global robotSearchedPub
	
	#Pull out needed map paramters
	width=mapData.info.width
	height=mapData.info.height
	resolution=mapData.info.resolution
	
	#Pull out current robot position
	robX=data.pose.pose.position.x*(1.0/resolution)+width/2
	robY=data.pose.pose.position.y*(1.0/resolution)+height/2
	
	# Color area that is seen (THIS IS INCORRECT, For testng purposes)
	for h in range(height):
		for w in range(width):
			if mapList[h*width+w] != -1:
				dist=math.sqrt((w-robX)**2 + (h-robY)**2)
				if dist < 100:
					mapList[h*width+w]=0
				else:
					mapList[h*width+w]=mapList[h*width+w]+0.25
					if mapList[h*width+w] > 100:
						mapList[h*width+w] = 100
			
		
			
	#Use map data to generate message for robotSearched map
	mapMsg=OccupancyGrid()
	mapMsg.header.stamp=rospy.Time.now()
	mapMsg.header.frame_id=mapData.header.frame_id
	mapMsg.info.resolution=mapData.info.resolution
	mapMsg.info.width=mapData.info.width
	mapMsg.info.height=mapData.info.height
	mapMsg.info.origin=mapData.info.origin
	mapMsg.data=mapList
	
	robotSearchedPub.publish(mapMsg)
	
def handleLaserScanMessage(data):
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
	
	for i in range(len(laserList)):
		xList.append(math.sin((angle_min+(angle_inc*i))))
		yList.append(math.cos((angle_min+(angle_inc*i))))
		print yList
	
				
### If Main ###
if __name__ == '__main__':
        robotSearched()
