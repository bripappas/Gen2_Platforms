#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	2-3-2014
#Name:			combineSearchSpace.py			
#Description:  	Combine occupancy searched space for multiple robots.  

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy
from nav_msgs.msg import OccupancyGrid		#Message Imports
from nav_msgs.srv import GetMap
from sensor_msgs.msg import Image
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
			
		#Initialize Robot Occupance Grids
		self.data0 = copy.copy(self.mapData)
		self.data1 = copy.copy(self.mapData)
		self.data2 = copy.copy(self.mapData)
			
		#Setup Subscribers to individual robot searched grids
		searched_0 = rospy.Subscriber('robot_0/robotSearched',OccupancyGrid,self.get0,queue_size = 1)
		searched_1 = rospy.Subscriber('robot_1/robotSearched',OccupancyGrid,self.get1,queue_size = 1)
		searched_2 = rospy.Subscriber('robot_2/robotSearched',OccupancyGrid,self.get2,queue_size = 1)	
			
		#Setup Publisher for combined searched grid	and image
		self.searchedCombinePub = rospy.Publisher('searchedCombine',OccupancyGrid, latch=True)
		self.imagePub = rospy.Publisher('searchedCombineImage', Image)	
		
		#Launch standalone thread for publishing
		thread.start_new_thread(self.publishCombined, ())
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
	
	#Publish Occupancy Map for Rviz and Image for OpenCV	
	def publishCombined(self):
		#Enter Main Loop
		while not rospy.is_shutdown():
			#Convert Searched Grids to Numpy Arrays
			map0 = numpy.array(self.data0.data)
			map1 = numpy.array(self.data1.data)
			map2 = numpy.array(self.data2.data)
			
			#Combine Searched Areas
			combined = numpy.minimum(map0,map1)
			combined = numpy.minimum(combined,map2)
			
			#Pack Occupancy Grid Message
			mapMsg=OccupancyGrid()
			mapMsg.header.stamp=rospy.Time.now()
			mapMsg.header.frame_id=self.mapData.header.frame_id
			mapMsg.info.resolution=self.mapData.info.resolution
			mapMsg.info.width=self.mapData.info.width
			mapMsg.info.height=self.mapData.info.height
			mapMsg.info.origin=self.mapData.info.origin
			mapMsg.data=combined.tolist()
			
			#Convert combined Occupancy grid values to grayscal image values
			combined[combined == -1] = 150			#Unknown -1->150 		(gray)
			combined[combined == 100] = 255			#Not_Searched 100->255	(white)
													#Searched=0				(black)
			#Pack Image Message
			imageMsg=Image()
			imageMsg.header.stamp = rospy.Time.now()
			imageMsg.header.frame_id = self.mapData.header.frame_id
			imageMsg.height = self.mapData.info.height
			imageMsg.width = self.mapData.info.width
			imageMsg.encoding = 'mono8'
			imageMsg.is_bigendian = 0
			imageMsg.step = self.mapData.info.width
			imageMsg.data = combined.tolist()
			
			#Publish Combined Occupancy Grid and Image
			self.searchedCombinePub.publish(mapMsg)
			self.imagePub.publish(imageMsg)
			
			#Update Every 0.5 seconds
			rospy.sleep(0.5)
		
	#Subscriber CallBacks	
	def get0(self,data):
		self.data0=data
	def get1(self,data):
		self.data1=data
	def get2(self,data):
		self.data2=data
		

# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('combineSearchSpace')
	nodeClass()
        
