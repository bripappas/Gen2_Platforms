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
		
		#Setup publishers
		self.goalPub0 = rospy.Publisher('robot_0/move_base_simple/goal', PoseStamped)
		self.goalPub1 = rospy.Publisher('robot_1/move_base_simple/goal', PoseStamped)
		self.goalPub2 = rospy.Publisher('robot_2/move_base_simple/goal', PoseStamped)
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
		
	def markerCallback(self,data):
		costMatrix = self.createCostMatrix(data.points)
		posMatrix = self.createPositionMatrix(costMatrix)
		
		minCostMatrix = costMatrix**posMatrix
		print costMatrix
		print posMatrix
		print minCostMatrix
		frontierMin0 = numpy.argmin(minCostMatrix[0,:])
		frontierMin1 = numpy.argmin(minCostMatrix[1,:])
		frontierMin2 = numpy.argmin(minCostMatrix[2,:])
		print frontierMin0
		print frontierMin1
		print frontierMin2
		
		#Pack messages
		goal0 = PoseStamped()
		goal1 = PoseStamped()
		goal2 = PoseStamped()
		
		goal0.header.stamp = rospy.Time.now()
		goal0.header.frame_id = '/map'
		goal1.header.stamp = rospy.Time.now()
		goal1.header.frame_id = '/map'
		goal2.header.stamp = rospy.Time.now()
		goal2.header.frame_id = '/map'
		goal0.pose.position = data.points[frontierMin0]
		goal1.pose.position = data.points[frontierMin1]
		goal2.pose.position = data.points[frontierMin2]
		
		goal0.pose.orientation.x = 0
		goal0.pose.orientation.y = 0
		goal0.pose.orientation.z = 0
		goal0.pose.orientation.w = 1
		
		goal1.pose.orientation.x = 0
		goal1.pose.orientation.y = 0
		goal1.pose.orientation.z = 0
		goal1.pose.orientation.w = 1
		
		goal2.pose.orientation.x = 0
		goal2.pose.orientation.y = 0
		goal2.pose.orientation.z = 0
		goal2.pose.orientation.w = 1
		
		self.goalPub0.publish(goal0)
		self.goalPub1.publish(goal1)
		self.goalPub2.publish(goal2)
		
	def createPositionMatrix(self,C):
		P = numpy.zeros((C.shape[0], C.shape[1]))
		for i in range(0,C.shape[0]):
			for j in range(0, C.shape[1]):
				P[i,j] = numpy.sum(C[:,j] <= C[i,j])
		return P
		
	def createCostMatrix(self,frontierPoints):
		#Make list of robots get_plan services (PUT ON PARAMATER SERVER)
		makePlanList = []
		makePlanList.append('/robot_0/nav/move_base_node_nav/make_plan')
		makePlanList.append('/robot_1/nav/move_base_node_nav/make_plan')
		makePlanList.append('/robot_2/nav/move_base_node_nav/make_plan')
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
	
