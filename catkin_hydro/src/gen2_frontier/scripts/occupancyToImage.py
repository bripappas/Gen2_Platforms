#!/usr/bin/env python
#Node to convert an Occupancy Grid to an Image
import roslib; roslib.load_manifest('gen2_frontier')
import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Image


#Initialize ROS node and setup up Publisher/Subscribers
def occupancyToImage():
	global searchedCombineSub
	global imagePub
	# Initialize the Node
	rospy.init_node('robotSearched')
	
	#Setup subscribers
	searchedCombineSub = rospy.Subscriber('searchedCombine',OccupancyGrid,convert,queue_size = 1)
	
	#Setup publishers
	imagePub = rospy.Publisher('searchedCombineImage', Image)
	
	#spin
	rospy.spin()
	
def convert(data):
	width=data.info.width
	height=data.info.height
	pixelList = [0] *width*height
	
	imageMsg=Image()
	imageMsg.header.stamp = rospy.Time.now()
	imageMsg.header.frame_id = '1'
	imageMsg.height = height
	imageMsg.width = width
	imageMsg.encoding = 'mono8'
	imageMsg.is_bigendian = 0
	imageMsg.step = width
	
	for h in range(height):
		for w in range(width):
			if data.data[h*width+w]==-1:
				pixelList[h*width+w] = 150
			elif data.data[h*width+w]==0:
				pixelList[h*width+w] = 0
			elif data.data[h*width+w]==100:
				pixelList[h*width+w] = 255	
			else:
				pixelList[h*width+w]=data.data[h*width+w]
				print 'ERROR'
				
	imageMsg.data = pixelList
	imagePub.publish(imageMsg)
	
### If Main ###
if __name__ == '__main__':
        occupancyToImage()
