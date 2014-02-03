#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import cv
import cv2
import numpy as np
import code
import copy
from matplotlib import pyplot as plt
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA

def findFrontiers(): 
	global imagePub
	global markerPub
	# Initialize the Node
	rospy.init_node('findFontiers')
	
	#Setup publishers/subscribers
	searchedCombineSub = rospy.Subscriber('searchedCombineImage',Image,callback,queue_size = 1)
	imagePub = rospy.Publisher('frontierImage', Image)
	markerPub = rospy.Publisher('frontierMarkers',Marker)
	
	#PLT in interactive mode to support resizing plt window
	plt.ion()
	plt.show()
	
	#spin
	rospy.spin()
	
def callback(data):
	global imagePub
	global markerPub
	
	#Convert image to CV image
	bridge=CvBridge()
	cv_image = bridge.imgmsg_to_cv(data, "mono8")
	
	# Convert the image to a Numpy array since most cv2 functionsrequire Numpy arrays.
	searched = np.array(cv_image, dtype=np.uint8)
	
	#Create a copy for sobel comparison
	searchedCopy=copy.copy(searched)
	searchedCopy[searchedCopy==255]=0
	
	#Take Sobel Derivatives
	sobel_x=np.uint8(np.absolute(cv2.Sobel(searched,cv2.CV_16S,1,0,ksize=1)))
	sobel_y=np.uint8(np.absolute(cv2.Sobel(searched,cv2.CV_16S,0,1,ksize=1)))
	sobel_xy=cv2.addWeighted(sobel_x,0.5,sobel_y,0.5,0)
	sobel_x_base=np.uint8(np.absolute(cv2.Sobel(searchedCopy,cv2.CV_16S,1,0,ksize=1)))
	sobel_y_base=np.uint8(np.absolute(cv2.Sobel(searchedCopy,cv2.CV_16S,0,1,ksize=1)))
	sobel_xy_base=cv2.addWeighted(sobel_x_base,0.5,sobel_y_base,0.5,0)
	ret,sobel_xy_thres = cv2.threshold(sobel_xy,0,255,cv2.THRESH_BINARY)
	ret,sobel_xy_base_thres = cv2.threshold(sobel_xy_base,0,255,cv2.THRESH_BINARY)
	
	#Subtract Comparisons for frontiers only
	sobelCombined=sobel_xy_base_thres-sobel_xy_thres
	ret,sobelCombined_thresh = cv2.threshold(sobelCombined,0,255,cv2.THRESH_BINARY)

	#Dialate Combined
	dialate=cv2.dilate(sobelCombined_thresh,np.ones((3,3),'uint8'))
	
	#Find Contour Centorids
	dialateCopy=copy.copy(dialate)
	contours,hier=cv2.findContours(dialateCopy,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	centroids = []
	colors = []
	for i in contours:
		if len(i) > 10:
			moments=cv2.moments(i)
			cx = int(moments['m10']/moments['m00'])
			cy = int(moments['m01']/moments['m00'])
			centroidPoint = Point()
			centroidColor = ColorRGBA()
			centroidPoint.x = cx/20.0-20
			centroidPoint.y = cy/20.0-32.8
			centroidPoint.z = 0
			#centroidColor = (0,0,1,1)
			centroidColor.r = 0
			centroidColor.g = 0
			centroidColor.b = 1
			centroidColor.a = 1
			centroids.append(centroidPoint)
			colors.append(centroidColor)

	#code.interact(local=locals())
	#Display Image in PLT Window
	'''plt.subplot(1,5,1),plt.imshow(searched,cmap='gray'),plt.title('Searched Space'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,5,2),plt.imshow(sobel_xy_thres,cmap='gray'),plt.title('Sobel All'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,5,3),plt.imshow(sobel_xy_base_thres,cmap='gray'),plt.title('Sobel All'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,5,4),plt.imshow(sobelCombined,cmap='gray'),plt.title('Frontiers Map'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,5,5),plt.imshow(dialate,cmap='gray'),plt.title('Dialate'),plt.xticks([]), plt.yticks([])
	plt.draw()
	plt.pause(0.001)'''
	
	#Convert the image back to mat format and publish as ROS image
	frontiers = cv.fromarray(dialate)
	imagePub.publish(bridge.cv_to_imgmsg(frontiers, "mono8"))

	#Publish centorids of frontiers as marker
	markerMsg = Marker()
	markerMsg.header.frame_id = "/map"
	markerMsg.header.stamp = rospy.Time.now()
	markerMsg.ns = ""
	markerMsg.id = 0
	markerMsg.type = 7			#Sphere List
	markerMsg.action = 0		#Add
	markerMsg.scale.x = 0.5
	markerMsg.scale.y = 0.5
	markerMsg.scale.z = 0.5
	markerMsg.points = centroids
	markerMsg.colors = colors
	markerPub.publish(markerMsg)
	print 'yes'
	
if __name__ == '__main__':
    findFrontiers()
