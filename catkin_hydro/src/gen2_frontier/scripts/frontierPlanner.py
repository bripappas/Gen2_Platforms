#!/usr/bin/env python

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy
from visualization_msgs.msg import Marker	#Message Imports
from geometry_msgs.msg import PoseStamped
from nav_msgs.srv import GetPlan
import math									#Other Imports
import numpy

class nodeClass():
	#Class Init Function
	def __init__(self):
		#Setup subscriber for combined searched image
		frontierMarkerSub = rospy.Subscriber('frontierMarkers',Marker,self.markerCallback,queue_size = 1) 
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
		
	def markerCallback(self,data):
		
		costMatrix = self.createCostMatrix(data.points)
		print costMatrix
		
	def createCostMatrix(self,frontierPoints):
		#Make list of robots get_plan services (PUT ON PARAMATER SERVER)
		makePlanList = []
		makePlanList.append('/robot_0/move_base_node/make_plan')
		makePlanList.append('/robot_1/move_base_node/make_plan')
		makePlanList.append('/robot_2/move_base_node/make_plan')
		PlanFrameId = []
		PlanFrameId.append('/robot_0/map')
		PlanFrameId.append('/robot_1/map')
		PlanFrameId.append('/robot_2/map')
		
		C = numpy.zeros((len(makePlanList), len(frontierPoints)))
		
		for i in range(0,len(frontierPoints)):
			for j in range(0,len(makePlanList)):
				stop = PoseStamped()
				stop.header.frame_id = PlanFrameId[j]
				stop.pose.position = frontierPoints[i]
				serviceName = makePlanList[j]
				C[j,i] = self.determineCost(serviceName,PoseStamped(),stop)
		return C
				
		
	def determineCost(self,serviceName, start, stop):
		rospy.wait_for_service(serviceName)
		try:
			dist = 0
			makePath = rospy.ServiceProxy(serviceName, GetPlan)
			path = makePath(start, stop, 0.5)
			poseArray = path.plan.poses
			for i in range(0,len(poseArray)-1):
				xDiff = poseArray[i].pose.position.x-poseArray[i+1].pose.position.x
				yDiff = poseArray[i].pose.position.y-poseArray[i+1].pose.position.y
				dist += math.sqrt(xDiff**2+yDiff**2)
			return dist
		except rospy.ServiceException, e:
			print "Get Plan service call failed: %s" %e
			
# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('frontierPlanner')
	nodeClass()
	
