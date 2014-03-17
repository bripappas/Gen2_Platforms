#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	3-14-2014
#Name:			combineSearchSpace.py			
#Description:  	Combine occupancy searched space for multiple robots.  

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy
from nav_msgs.msg import OccupancyGrid		#Message Imports
from nav_msgs.srv import GetMap
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import copy								#Other imports
import thread
import numpy

class nodeClass():
	#Class Init Function
	def __init__(self):
		#Create service client to retrieve map from map server
		rospy.loginfo("Waiting for map to become available")
		rospy.wait_for_service('/static_map')
		try:
			#Call get map service
			getStaticMap = rospy.ServiceProxy('/static_map',GetMap)
			resp = getStaticMap()
			self.mapData=resp.map
			rospy.loginfo("The static map has been retrieved")
		except rospy.ServiceException, e:
			print "Static map service call failed: %s"%e
			
		#Get Current Number of Robots
		self.numRobots = rospy.get_param('/num_robots')
		self.searchedData = []
			
		#Initialize Robot Occupancy Grids and Subscribers
		for i in range(0, self.numRobots):
			#Setup Occupany Grids
			self.searchedData.append(copy.copy(self.mapData))
			
			#Setup Subscribers to individual robot searched grids
			topicName = 'robot_' + `i` +'/robotSearched'
			rospy.Subscriber(topicName,OccupancyGrid,self.get,queue_size = 1)
			
		#Setup Publisher for combined searched grid	and image
		self.searchedCombinePub = rospy.Publisher('searchedCombine',OccupancyGrid, latch=True)
		self.imagePub = rospy.Publisher('searchedCombineImage', Image)	
		
		#Setup Publisher for percentage searched
		self.percentPub = rospy.Publisher('percentSearched', Float32)	
		
		#Launch standalone thread for publishing
		thread.start_new_thread(self.publishCombined, ())
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
	
	#Publish Occupancy Map for Rviz and Image for OpenCV	
	def publishCombined(self):
		#Enter Main Loop
		while not rospy.is_shutdown():
			
			#Convert to Numpy  Arrays
			map = []
			for i in range(0, self.numRobots):
				map.append(numpy.array(self.searchedData[i].data))
				
			combined2 = map[0]
			if self.numRobots > 1:
				#Find Minimum of all maps
				for i in range(1, self.numRobots):
					combined2 = numpy.minimum(combined2,map[i])
					
			#Pack Occupancy Grid Message
			mapMsg=OccupancyGrid()
			mapMsg.header.stamp=rospy.Time.now()
			mapMsg.header.frame_id=self.mapData.header.frame_id
			mapMsg.info.resolution=self.mapData.info.resolution
			mapMsg.info.width=self.mapData.info.width
			mapMsg.info.height=self.mapData.info.height
			mapMsg.info.origin=self.mapData.info.origin
			mapMsg.data=combined2.tolist()
			
			#Convert combined Occupancy grid values to grayscal image values
			combined2[combined2 == -1] = 150			#Unknown -1->150 		(gray)
			combined2[combined2 == 100] = 255			#Not_Searched 100->255	(white)
														#Searched=0				(black)
														
			#Calculate percentage of open area searched
			numNotSearched = combined2[combined2==255].size
			numSearched = combined2[combined2==0].size
			percentSearched = 100*float(numSearched)/(numNotSearched+numSearched)
			percentSearchedMsg = Float32()
			percentSearchedMsg.data = percentSearched
			self.percentPub.publish(percentSearchedMsg)
			
			#Pack Image Message
			imageMsg=Image()
			imageMsg.header.stamp = rospy.Time.now()
			imageMsg.header.frame_id = self.mapData.header.frame_id
			imageMsg.height = self.mapData.info.height
			imageMsg.width = self.mapData.info.width
			imageMsg.encoding = 'mono8'
			imageMsg.is_bigendian = 0
			imageMsg.step = self.mapData.info.width
			imageMsg.data = combined2.tolist()
			
			#Publish Combined Occupancy Grid and Image
			self.searchedCombinePub.publish(mapMsg)
			self.imagePub.publish(imageMsg)
			
			#Update Every 0.5 seconds
			rospy.sleep(1.0)
		
	def get(self,data):
		topic = data._connection_header['topic']
		ns = topic.split('_')
		numRobot = int(ns[1][0])
		self.searchedData[numRobot] = data
		
# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('combineSearchSpace')
	nodeClass()
        
