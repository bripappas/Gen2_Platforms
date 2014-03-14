#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	3-14-2014
#Name:			recordData.py			
#Description:  	Dump data from simulation to data file 

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy

class nodeClass():
	#Class Init Function
	def __init__(self):
		x=2

# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('combineSearchSpace')
	nodeClass()
        
