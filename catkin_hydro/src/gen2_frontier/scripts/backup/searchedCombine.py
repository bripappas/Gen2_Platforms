#!/usr/bin/env python


import roslib; roslib.load_manifest('gen2_frontier')
import rospy
from nav_msgs.msg import OccupancyGrid
from nav_msgs.srv import GetMap
import thread
import numpy

#Initialize ROS node and setup up Publisher/Subscribers
def searchedCombine():
	global mapData
	global searchedCombinePub
	
	# Initialize the Node
	rospy.init_node('searchedCombine')
	
	# Create service client to get map from map server
	rospy.loginfo("Waiting for map to become available")
	rospy.wait_for_service('/static_map')
	try:
		getStaticMap = rospy.ServiceProxy('/static_map',GetMap)

		resp = getStaticMap()
		#mapData = OccupancyGrid()
		mapData=resp.map
		
	except rospy.ServiceException, e:
		print "Static map service call failed: %s"%e
		
	
		
	#Get mapData
	rospy.loginfo("The static map has been retrieved")
	width=mapData.info.width
	height=mapData.info.height
	resolution=mapData.info.resolution
	frame_id=mapData.header.frame_id
	
	# Setup aSubscribers
	searched_0 = rospy.Subscriber('robot_0/robotSearched',OccupancyGrid,get0,queue_size = 1)
	searched_1 = rospy.Subscriber('robot_1/robotSearched',OccupancyGrid,get1,queue_size = 1)
	searched_2 = rospy.Subscriber('robot_2/robotSearched',OccupancyGrid,get2,queue_size = 1)
	
	# Setup Publishers
	searchedCombinePub = rospy.Publisher('searchedCombine',OccupancyGrid, latch=True)
	
	thread.start_new_thread(updateCombined, ())
	rospy.spin()
	
	
def get0(data):
	global data0
	data0 = data
	
def get1(data):
	global data1
	data1 = data
	
def get2(data):
	global data2
	data2 = data
	
def updateCombined():
	global data0
	global data1
	global data2
	global mapData
	global searchedCombinePub
	rospy.wait_for_message('robot_0/robotSearched', OccupancyGrid, timeout=None)
	rospy.wait_for_message('robot_1/robotSearched', OccupancyGrid, timeout=None)
	rospy.wait_for_message('robot_2/robotSearched', OccupancyGrid, timeout=None)
	mapMsg=OccupancyGrid()
	while not rospy.is_shutdown():
		map0 = numpy.array(data0.data)
		map1 = numpy.array(data1.data)
		map2 = numpy.array(data2.data)
		
		combined = numpy.minimum(map0,map1)
		combined = numpy.minimum(combined,map2)
	
		mapMsg.header.stamp=rospy.Time.now()
		mapMsg.header.frame_id=mapData.header.frame_id
		mapMsg.info.resolution=mapData.info.resolution
		mapMsg.info.width=mapData.info.width
		mapMsg.info.height=mapData.info.height
		mapMsg.info.origin=mapData.info.origin
		mapMsg.data=combined.tolist()
		
		searchedCombinePub.publish(mapMsg)
		
		rospy.sleep(1.0)

### If Main ###
if __name__ == '__main__':
        searchedCombine()
