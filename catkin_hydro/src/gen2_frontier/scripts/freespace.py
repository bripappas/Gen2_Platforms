#!/usr/bin/env python

import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import std_msgs.msg
from nav_msgs.msg import OccupancyGrid
from nav_msgs.srv import GetMap

#Initialize ROS node and setup up Publisher/Subscribers
def freeSpace():
	# Initialize the Node
	rospy.init_node('freeSpace')
	
	# Create freespace Publisher
	freeSpacePub = rospy.Publisher('freeSpace',OccupancyGrid,latch=True)
	
	# Create service client to get map from map server
	print "waiting for map"
	rospy.wait_for_service('/static_map')
	try:
		getStaticMap = rospy.ServiceProxy('/static_map',GetMap)

		resp = getStaticMap()
		data=resp.map
	except rospy.ServiceException, e:
		print "Static map service call failed: %s"%e
		
	#Use map data to generate message for freespacd map
	mapMsg=OccupancyGrid()
	mapMsg.header.stamp=rospy.Time.now()
	mapMsg.header.frame_id=data.header.frame_id
	mapMsg.info.resolution=data.info.resolution
	mapMsg.info.width=data.info.width
	mapMsg.info.height=data.info.height
	mapMsg.info.origin=data.info.origin
	mapMsg.data=data.data
	
	
	print "publishing"
	freeSpacePub.publish(mapMsg)
	rospy.spin()
	
	
		
				
### If Main ###
if __name__ == '__main__':
        freeSpace()
