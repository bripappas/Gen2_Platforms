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
		if len(data.points) == 0:
			print "SIMULATION COMPLETE"
			rospy.signal_shutdown("DONE")
		else:
			#Create Cost Matrix (Cost for each robot(row)/frontier(col) pair)
			costMatrix = self.createCostMatrix(data.points)
			
			#Create Position Matrix
			posMatrix = self.createPositionMatrix(costMatrix)
			
			#Create Assign Matrix
			assignMatrix = self.createAssignmentMatrix(posMatrix)
			
			#Break Tie in Assign Matrix based on cost
			minMatrix = assignMatrix * costMatrix
			minMatrix[minMatrix == 0] = 999
			
			#Assign each robot a frontier
			frontierMin0 = numpy.argmin(minMatrix[0,:])
			frontierMin1 = numpy.argmin(minMatrix[1,:])
			frontierMin2 = numpy.argmin(minMatrix[2,:])
			
			#If no assignament, take greedy option
			if min(minMatrix[0,:]) == 999:
				frontierMin0 = numpy.argmin(costMatrix[0,:])
			if min(minMatrix[1,:]) == 999:
				frontierMin1 = numpy.argmin(costMatrix[1,:])
			if min(minMatrix[2,:]) == 999:
				frontierMin2 = numpy.argmin(costMatrix[2,:])
			
			#Print for DEBUG
			print "\nCost Matrix"
			print costMatrix
			print "\nPosition Matrix"
			print posMatrix
			print "\nAssignment Matrix"
			print assignMatrix
			print "\nMin Matrix"
			print minMatrix
			
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
		
	def createAssignmentMatrix(self,P):
		tempMatrix = P.argmin(axis=0)
		assignMatrix = numpy.zeros(P.shape)
		for i in range(0,len(tempMatrix)):
			assignMatrix[tempMatrix[i],i]=1
		return assignMatrix
		
	def createPositionMatrix(self,C):
		P = numpy.zeros((C.shape[0], C.shape[1]))
		for i in range(0,C.shape[0]):
			for j in range(0, C.shape[1]):
				P[i,j] = numpy.sum(C[:,j] < C[i,j])
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
	
