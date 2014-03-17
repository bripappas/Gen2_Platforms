#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	2-10-2014
#Name:			findFrontiers.py			
#Description:  	Use OpenCV to find frontier waypoints from searched image

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy

from sensor_msgs.msg import Image			#Message Imports
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from nav_msgs.srv import GetMap

from matplotlib import pyplot as plt		#Other imports
from cv_bridge import CvBridge
import numpy as np
import copy
import cv
import cv2

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
			mapData=resp.map
			rospy.loginfo("The static map has been retrieved")
		except rospy.ServiceException, e:
			print "Static map service call failed: %s"%e
		
		#Retrieve needed mapData
		self.mapRes = mapData.info.resolution
		self.mapOrigin = mapData.info.origin	
		
		#Setup subscriber for combined searched image
		searchedCombineSub = rospy.Subscriber('searchedCombineImage',Image,self.imageCallback,queue_size = 1) 

		#Setup Publisher for frontier image and frontier markers
		self.imagePub = rospy.Publisher('frontierImage', Image)
		self.markerPub = rospy.Publisher('frontierMarkers',Marker)
		
		#PLT in interactive mode, can resize plt window on the fly
		plt.ion()
		plt.show()
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
		
	def imageCallback(self,data):
		#Convert image to CV2 supported numpy array
		bridge=CvBridge()
		cv_image = bridge.imgmsg_to_cv(data, "mono8")
		searched = np.array(cv_image, dtype=np.uint8)
		
		#Create copy and clear searched space in copy (leaving map only)
		searchedCopy=copy.copy(searched)
		searchedCopy[searchedCopy==255]=0
		
		#Take Sobel Derivatives of searched and map only
		sobel_x=np.uint8(np.absolute(cv2.Sobel(searched,cv2.CV_16S,1,0,ksize=1)))
		sobel_y=np.uint8(np.absolute(cv2.Sobel(searched,cv2.CV_16S,0,1,ksize=1)))
		sobel_xy=cv2.addWeighted(sobel_x,0.5,sobel_y,0.5,0)
		sobel_x_base=np.uint8(np.absolute(cv2.Sobel(searchedCopy,cv2.CV_16S,1,0,ksize=1)))
		sobel_y_base=np.uint8(np.absolute(cv2.Sobel(searchedCopy,cv2.CV_16S,0,1,ksize=1)))
		sobel_xy_base=cv2.addWeighted(sobel_x_base,0.5,sobel_y_base,0.5,0)
		ret,sobel_xy_thres = cv2.threshold(sobel_xy,0,255,cv2.THRESH_BINARY)
		ret,sobel_xy_base_thres = cv2.threshold(sobel_xy_base,0,255,cv2.THRESH_BINARY)
		
		#Subtract Sobel Derivatives (Leaves Frontiers Only)
		sobelCombined=sobel_xy_base_thres-sobel_xy_thres
		ret,sobelCombined_thresh = cv2.threshold(sobelCombined,0,255,cv2.THRESH_BINARY)
		
		#Dialate Frontiers To Form Continuous Contours
		dialate=cv2.dilate(sobelCombined_thresh,np.ones((3,3),'uint8'))
		
		#Find Contours (make copy since dialate destorys original image)
		dialateCopy=copy.copy(dialate)
		contours,hier=cv2.findContours(dialateCopy,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

		#Convert the image back to mat format for publishing as ROS image
		frontiers = cv.fromarray(dialate)
		
		#Create List Data for Marker Message
		centroids = []
		colors = []
		#Filter Frontier Contour by number of pixels
		for i in contours:
			if len(i) > 50:
				moments=cv2.moments(i)
				cx = int(moments['m10']/moments['m00'])
				cy = int(moments['m01']/moments['m00'])
				centroidPoint = Point()
				centroidColor = ColorRGBA()
				centroidPoint.x = cx*self.mapRes+self.mapOrigin.position.x
				centroidPoint.y = cy*self.mapRes+self.mapOrigin.position.y
				centroidPoint.z = 0; 
				centroidColor.r = 0 
				centroidColor.g = 0 
				centroidColor.b = 1 
				centroidColor.a = 1
				centroids.append(centroidPoint)
				colors.append(centroidColor)
				
		#Pack Marker Message
		markerMsg = Marker()
		markerMsg.header.frame_id = "/map"
		markerMsg.header.stamp = rospy.Time.now()
		markerMsg.ns = ""
		markerMsg.id = 0
		markerMsg.type = 7			#Sphere List Type
		markerMsg.action = 0		#Add Mode
		markerMsg.scale.x = 0.5
		markerMsg.scale.y = 0.5
		markerMsg.scale.z = 0.5
		markerMsg.points = centroids
		markerMsg.colors = colors
	
		#Publish Marker and Image messages
		self.imagePub.publish(bridge.cv_to_imgmsg(frontiers, "mono8"))
		self.markerPub.publish(markerMsg)
		
		#Dispaly images for debug
		#self.displayImages(searched,sobel_xy_thres,sobel_xy_base_thres,sobelCombined,dialate)
		#plt.subplot(1,1,1),plt.imshow(dialate,cmap='gray'),plt.title('Searched Space'),plt.xticks([]), plt.yticks([])
		#plt.subplot(1,2,2),plt.imshow(searchedCopy,cmap='gray'),plt.title('Searched Space'),plt.xticks([]), plt.yticks([])
		#plt.subplot(1,5,3),plt.imshow(sobel_xy_thres,cmap='gray'),plt.title('Sobel All'),plt.xticks([]), plt.yticks([])
		#plt.subplot(1,5,4),plt.imshow(sobel_xy_base_thres,cmap='gray'),plt.title('Frontiers Map'),plt.xticks([]), plt.yticks([])
		#plt.subplot(1,5,5),plt.imshow(sobelCombined_thresh,cmap='gray'),plt.title('Dialate'),plt.xticks([]), plt.yticks([])
		#plt.draw()
		#plt.pause(0.01)
		
	#Dispaly OpenCV images in PLT windows			
	#def displayImages(self,searched,sobelOrig,sobelBase,sobelBoth,dialate,searchedCopy,sobel_xy_thres,sobel_xy_base_thres,sobelCombined_thresh):
		
		
# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('findFontiers')
	nodeClass()

