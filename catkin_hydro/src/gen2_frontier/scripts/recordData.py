#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	3-14-2014
#Name:			recordData.py			
#Description:  	Dump data from simulation to data file 

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy
from std_msgs.msg import Header				#Message Imports
from std_msgs.msg import Float32
import time							#Other Imports

class nodeClass():
	#Class Init Function
	def __init__(self):
		#Setup subscriber for start and stop message
		self.startSub = rospy.Subscriber('startTime', Header, self.startTimeCallback)
		self.stopSub  = rospy.Subscriber('stopTime', Header, self.stopTimeCallback)
		
		#Wait for subscribed messages to start arriving
		rospy.spin()
		
	def startTimeCallback(self, data):
		self.startTime = data.stamp
		rospy.loginfo('Started At: ' + str(self.startTime))
		
		#Reset Data Storage
		self.searchedTimeStamp = []
		self.percentSearched = []
		
		#Subscribe to data after start
		self.percentSum=rospy.Subscriber('percentSearched', Float32, self.percentCallback)
		
	def stopTimeCallback(self, data):
		self.stopTime = data.stamp
		rospy.loginfo('Stopped At: ' + str(self.stopTime))
		totalTime = self.stopTime-self.startTime
		
		#Unsubscribe to data after stop
		self.percentSum.unregister()
		
		#Write Data to File 
		currentTime = str(time.time())
		resultsFile = open("res_" + currentTime, "w")
		resultsFile.write(str(totalTime.to_sec()) + "\n")
		
		for i in range(0,len(self.searchedTimeStamp)):
			resultsFile.write(str(self.searchedTimeStamp[i]) + ' ' + str(self.percentSearched[i]) + "\n")
		
		resultsFile.close()
		
		
		
		#print totalTime.to_sec()
		#for i in range(0,len(self.searchedTimeStamp)):
			#print str(self.searchedTimeStamp[i]) + ' ' + str(self.percentSearched[i])
		
	def percentCallback(self, data):
		time = rospy.get_rostime()
		elapsedTime = time-self.startTime
		rospy.loginfo(str(elapsedTime.to_sec()) + ': ' + str(data.data)) 
		self.searchedTimeStamp.append(elapsedTime.to_sec())
		self.percentSearched.append(data.data)
		
		
		

# Main Function
if __name__ == '__main__':
	# Initialize the Node and Call nodeClass()
	rospy.init_node('recordData')
	nodeClass()
        
