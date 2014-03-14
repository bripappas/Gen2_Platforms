#!/usr/bin/env python

#Author:		Brian Pappas
#Last Modified	3-14-2014
#Name:			resetSearched.py			
#Description:  	Calls the service of all robots to reset their searched space  

import roslib 								#ROS Imports
roslib.load_manifest('gen2_frontier')
import rospy

from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse

		
# Main Function
if __name__ == '__main__':
	# Initialize the Node
	rospy.init_node('resetSearched')
	
	#Call clear searched for each robot in system
	numRobots = rospy.get_param('/num_robots')
	for i in range(0, numRobots):
		#Setup Subscribers to individual robot searched grids
		serviceName = 'robot_' + `i` +'/clearSearched'
		resetSearchedSpace = rospy.ServiceProxy(serviceName,Empty)
		resetSearchedSpace()
		rospy.loginfo('Called' + serviceName)
	
	

