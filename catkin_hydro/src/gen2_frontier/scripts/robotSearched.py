#!/usr/bin/env python


import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import std_msgs.msg
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion
from nav_msgs.srv import GetMap
import math

mapList = []						#Working array to calculate searched cells
mapData = mapMsg=OccupancyGrid()	#Ocupancy message to hold map data

#Initialize ROS node and setup up Publisher/Subscribers
def robotSearched():
	global mapData
	global mapList
	global robotSearchedPub
	
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
	amclPoseSub = rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,handlePoseMessage,queue_size = 1)
	
	# Setup Publishers
	robotSearchedPub = rospy.Publisher('robotSearched',OccupancyGrid, latch=True)
	
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
	robX=int(data.pose.pose.position.x*(1.0/resolution)+width/2)
	robY=int(data.pose.pose.position.y*(1.0/resolution)+height/2)
	quat=data.pose.pose.orientation
	
	# Color area that is seen (THIS IS INCORRECT, For testng purposes)
	senseDist = 100
	(roll,pitch,yaw) = euler_from_quaternion([quat.x,quat.y,quat.z,quat.w])
	for h in xrange(robY-senseDist,robY+senseDist+1):
		for w in xrange(robX-senseDist,robX+senseDist+1):
			if mapList[h*width+w] != -1:
				dist=math.sqrt((w-robX)**2 + (h-robY)**2)
				if dist < senseDist:
				#	if yaw < 0:
				#		yaw = yaw+(math.pi*2)
				#	angleRelYaw = math.atan2(w-robX,h-robY)+yaw
				#	if angleRelYaw >= 0 and angleRelYaw <= math.pi:
						if LOS(robX,w,robY,h,width):
							mapList[h*width+w]=0
				#Decay used for patrolling
				#else:
				#	mapList[h*width+w]=mapList[h*width+w]+0.50  #<--Decay Rate################
				#	if mapList[h*width+w] > 100:
				#		mapList[h*width+w] = 100
			
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
	#rospy.sleep(0.1)
	
def LOS(x0, x1, y0, y1, width):
	dx = abs(x1-x0)
	dy = abs(y1-y0)
	sx = 1 if x0<x1 else -1
	sy = 1 if y0<y1 else -1
	err = dx/2 if dx>dy else -dy/2
	
	while(True):
		if(mapList[y0*width+x0] == -1):
			return 0
		if(x0==x1 and y0==y1):
			return 1
		e2=err
		if(e2 > -dx):
			err = err - dy
			x0 = x0 + sx
		if(e2 < dy):
			err = err + dx
			y0 = y0 + sy
			
	
### If Main ###
if __name__ == '__main__':
        robotSearched()
