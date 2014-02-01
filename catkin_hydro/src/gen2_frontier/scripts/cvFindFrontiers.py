#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import cv
import cv2
import numpy as np
import code
import copy
from matplotlib import pyplot as plt

#import sys
#from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def findFrontiers(): 
	global imagePub
	# Initialize the Node
	rospy.init_node('findFontiers')
	
	#Setup subscribers
	searchedCombineSub = rospy.Subscriber('searchedCombineImage',Image,callback,queue_size = 1)
	
	#Setup publishers
	imagePub = rospy.Publisher('frontierImage', Image)
	
	#spind
	plt.ion()
	plt.show()
	rospy.spin()
	
def callback(data):
	global imagePub
	
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
	dialate=cv2.dilate(sobelCombined_thresh,np.ones((5,5),'uint8'))
	
	#Find Contour Centorids
	dialateCopy=copy.copy(dialate)
	contours,hier=cv2.findContours(dialateCopy,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	centroids = []
	for i in contours:
		if len(i) > 10:
			moments=cv2.moments(i)
			cx = int(moments['m10']/moments['m00'])
			cy = int(moments['m01']/moments['m00'])
			centroids.append([cx,cy])
			
	print centroids
	#code.interact(local=locals())
	
	'''#Display Image in PLT Window
	plt.subplot(1,3,1),plt.imshow(sobel_xy,cmap='gray'),plt.title('SOBEL'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,3,2),plt.imshow(sobelCombined,cmap='gray'),plt.title('SUBTRACT FILTER'),plt.xticks([]), plt.yticks([])
	plt.subplot(1,3,3),plt.imshow(dialate,cmap='gray'),plt.title('DIALATE'),plt.xticks([]), plt.yticks([])
	plt.draw()
	plt.pause(0.001)'''
	
	#Convert the image back to mat format
	frontiers = cv.fromarray(dialate)
	
	#Convert back to ROS image
	imagePub.publish(bridge.cv_to_imgmsg(frontiers, "mono8"))
	
if __name__ == '__main__':
    findFrontiers()
