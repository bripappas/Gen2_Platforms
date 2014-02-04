#!/usr/bin/env python

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy
from visualization_msgs.msg import Marker	#Message Imports
from geometry_msgs.msg import PoseStamped
from nav_msgs.srv import GetPlan

class nodeClass():
	#Class Init Function
	def __init__(self):
		#Setup subscriber for combined searched image
		frontierMarkerSub = rospy.Subscriber('frontierMarkers',Marker,self.markerCallback,queue_size = 1) 
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
		
	def markerCallback(self,data):
		frontierPoints = data.points
		
		start = PoseStamped()
		stop = PoseStamped()
		
		start.header.frame_id = '/robot_0/map'
		start.pose.position = frontierPoints[0]
	
		stop.header.frame_id = '/robot_0/map'
		stop.pose.position = frontierPoints[1]
		
		
		self.determineCost('/robot_0/move_base_node/make_plan',start,stop)
		
	def determineCost(self,serviceName, start, stop):
		rospy.wait_for_service(serviceName)

		try:
			makePath = rospy.ServiceProxy(serviceName, GetPlan)
			path = makePath(start, stop, 0.5)
			print len(path.plan.poses)
			#CALCULATE DISTANCE
		except rospy.ServiceException, e:
			print "Get Plan service call failed: %s" %e
		


# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('frontierPlanner')
	nodeClass()
	
