#!/usr/bin/env python

import roslib; roslib.load_manifest('gen2_frontier')
import rospy
from nav_msgs.msg import OccupancyGrid


#Initialize ROS node and setup up Publisher/Subscribers
def findFrontierCells():
	global findFrontierPub
	# Initialize the Node
	rospy.init_node('findFrontierCells')
	
	# Create freespace Publisher
	findFrontierPub = rospy.Publisher('fontiers',OccupancyGrid,latch=True)
	
	# Setup Subscribers
	searchedSub = rospy.Subscriber('searchedCombine',OccupancyGrid,handleSearchedCombinedMessage,queue_size = 1)
	
	rospy.spin()
	
def handleSearchedCombinedMessage(data):
	global findFrontierPub
	#get map dimensions data
	
	width=data.info.width
	height=data.info.height
	searchedMap = data.data
	
	frontier = [0] * (width * height)
	
	for h in range(height):
		for w in range(width):
			if searchedMap[h*width+w] == -1:
				frontier[h*width+w]=-1
			if searchedMap[h*width+w] == 100:
				if isFrontier(searchedMap,h,w,height,width):
					frontier[h*width+w]=100
			
	mapMsg=OccupancyGrid()				
	mapMsg.header.stamp=rospy.Time.now()
	mapMsg.header.frame_id=data.header.frame_id
	mapMsg.info.resolution=data.info.resolution
	mapMsg.info.width=width
	mapMsg.info.height=height
	mapMsg.info.origin=data.info.origin
	mapMsg.data=frontier
	findFrontierPub.publish(mapMsg)
	
def isFrontier(searchedMap,h,w,height,width):
	for x in range (-1,2):
		for y in range (-1,2):
			if searchedMap[(h+y)*width+(w+x)] < 100 and searchedMap[(h+y)*width+(w+x)] > -1:
				return True
	return False

### If Main ###
if __name__ == '__main__':
        findFrontierCells()
