#!/usr/bin/env python
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
import cv
import cv2
import numpy as np

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
	rospy.spin()
	
def callback(data):
	global imagePub
	
	#Convert image to CV image
	bridge=CvBridge()
	cv_image = bridge.imgmsg_to_cv(data, "mono8")
	
	# Convert the image to a Numpy array since most cv2 functionsrequire Numpy arrays.
	cv_image = np.array(cv_image, dtype=np.uint8)
	
	#Take Sobel Derivatives
	sobel_x=np.uint8(np.absolute(cv2.Sobel(cv_image,cv2.CV_16S,1,0,ksize=1)))
	sobel_y=np.uint8(np.absolute(cv2.Sobel(cv_image,cv2.CV_16S,0,1,ksize=1)))
	sobel_xy=cv2.addWeighted(sobel_x,0.5,sobel_y,0.5,0)

	#Apply Threshold
	ret,thresh = cv2.threshold(sobel_xy,254,255,cv2.THRESH_BINARY)
	#cv.Threshold(laplacian,thresh,254,255,cv.CV_THRESH_BINARY)
	
	#Display Image in CV Window
	#cv2.namedWindow("Image window")
	#cv2.imshow("Image window", thresh)
	#cv2.waitKey(1)
	
	#Dialate Thresholds
	dialate=cv2.dilate(thresh,np.ones((5,5),'uint8'))
	
	#Convert the image back to mat format
	frontiers = cv.fromarray(dialate)
	
	#Convert back to ROS image
	imagePub.publish(bridge.cv_to_imgmsg(frontiers, "mono8"))
	
if __name__ == '__main__':
    findFrontiers()
