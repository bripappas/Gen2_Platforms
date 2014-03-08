#!/usr/bin/env python
import rospy
import numpy
import math
from std_msgs.msg import Int16, Float32
from sensor_msgs.msg import Imu

rVel=0					#Right Wheel Vel (m/s)
lVel=0					#Left Wheel Vel (m/s)
gyroRaw=0				#Analog Gyro  Reading

buffer_length=500		#Maximum number to calculate calibrated average
buffer=[]				#Array to average to calculate calibrated gyro value
gyro_cal=0;				#mean of buffer
gyroScale=1.25;			#Factor to scale gyro by

imuPub=rospy.Publisher('imu_data',Imu)
previousTime=rospy.Time()
yaw=0
angular_vel=0



#Since the gyro sensor is sensitive to various envirnoment changes (e.g. temperature),
#the neutral value of the sensor is constantly updated when both wheel velocites are 0;
def gyroCallback(msg):
	global gyroRaw
	gyroRaw=msg.data
	#rospy.loginfo("Gyro Val %s" % msg.data)
	
#Grab the Left Wheel Veloctiy
def lVelCallback(msg):
	global lVel
	lVel=msg.data
	#rospy.loginfo("Left Vel %s" % lVel)

#Grab the Right Whell Velocity    
def rVelCallback(msg):
	global rVel
	rVel=msg.data
	#rospy.loginfo("Right Vel %s" % rVel)

def publish_imu():
	global buffer,gyro_cal,previousTime,yaw,angular_vel
	currentTime=rospy.Time.now()
	dt=currentTime-previousTime
	dt=dt.to_sec()
	previousTime=currentTime
	if rVel==0 and lVel==0:
		buffer.append(gyroRaw)
		
		if len(buffer) > buffer_length:
			buffer.pop(0)
			
		gyro_cal=numpy.mean(buffer)
		angular_vel=0
	
	else:	
		angular_vel=-(((gyroRaw-gyro_cal)/gyro_cal)*300*gyroScale)*math.pi/180;
		
		if math.fabs(angular_vel) < 0:
			angular_vel=0
		yaw+=(angular_vel*dt)
		
		rospy.loginfo("Yaw %s" % yaw)
		rospy.loginfo("Yaw Vel %s" % angular_vel)
	
	imu=Imu()
	imu.header.stamp = currentTime
	imu.header.frame_id = 'gyro_link'
	imu.orientation.x=0
	imu.orientation.y=0
	imu.orientation.z=math.sin(yaw/2)
	imu.orientation.w=math.cos(yaw/2)
	imu.orientation_covariance=[1e6,0,0,0,1e6,0,0,0,1e-10]
	imu.angular_velocity.x=0
	imu.angular_velocity.y=0
	imu.angular_velocity.z=angular_vel
	imu.angular_velocity_covariance=[1e6, 0, 0, 0, 1e6, 0, 0, 0, 1e-10]
	imu.linear_acceleration_covariance=[-1,0,0,0,0,0,0,0,0]
	imuPub.publish(imu)


def gyro():
    rospy.init_node('gyro2imu')
    rospy.Subscriber("gyro_val", Int16, gyroCallback)
    rospy.Subscriber("lwheel_vel", Float32, lVelCallback);
    rospy.Subscriber("rwheel_vel", Float32, rVelCallback);
    previousTime=rospy.Time.now()
    
    r=rospy.Rate(50)
    while not rospy.is_shutdown():
		publish_imu()
		r.sleep()


if __name__ == '__main__':
    gyro()
