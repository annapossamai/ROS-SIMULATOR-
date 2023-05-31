#! /usr/bin/env python

"""
.. module:: action_client_A
	:platform: Unix
	:synopsis: Python module for the action client A.

.. moduleauthor:: Anna Possamai

This node implements an *action client node* that allows the user to *set the target* (x,y) or to cancel it by keyboard input in the console; 
then, it publish the robot position and velocity as a custom message (pos_vel), by relying on the values publish on the topic /odom.

Subscriber: 
	/odom

Publish:
	/pos_vel

Action client:
	/reaching_goal

"""


# import ros stuff
import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
import sys
import select
from std_srvs.srv import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Pos_vel


def callback_pos_vel(msg):


	"""
	Callback function to get the position and velocity and publish them as a custom message (pos_vel).

	Args:
		msg(Pos_vel): the position and velocity of the robot

	"""
	
	global pub
	
	# Get the position from the msg
	position = msg.pose.pose.position
	
	# Get the velocity from the msg
	velocity = msg.twist.twist.linear
	
	# Create custom message
	pos_vel = Pos_vel()
	
	# Assign the parameters of the custom message
	pos_vel.x=position.x
	pos_vel.y=position.y
	pos_vel.vel_x=velocity.x
	pos_vel.vel_y=velocity.y

	# Publish the custom message
	pub.publish(pos_vel)

def robot_client():

	"""
	This function implements the action client node that allows the user to set the target (x,y) or to cancel it.
	
	"""
	
	#Create the SimpleActionClient
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	
	# Wait until the action server is started up
	client.wait_for_server()
	
	while not rospy.is_shutdown():
	
		# Get the keyboard inputs from the user
		print("Insert the new target, or press c to cancel the used one:")
		x=input("Position x: ")
		y=input("Position y: ")
		
		
		if x=="c" or y=="c":
			
			#cancel the goal
			client.cancel_goal()
			print("The goal has been cancelled!")
			
		else:
			
			x=float(x)
			y=float(y)
			
			# Create the new goal position
			goal = assignment_2_2022.msg.PlanningGoal()
			goal.target_pose.pose.position.x = x
			goal.target_pose.pose.position.y = y
	      		
	      		# Send the goal to the server
			client.send_goal(goal)
      		

def main():
	
	"""
	This function initializes the ROS node, the publisher and the subscriber, and calls the client function.
	
	"""


	# Initialize a rospy node so that the SimpleActionClient can
    # publish and subscribe over ROS
	rospy.init_node('action_client')
	
	global pub
	
	#Publisher: send a message containing the position and velocity
	pub = rospy.Publisher("/pos_vel", Pos_vel, queue_size=1)
	
	#Subscriber: get from /odom topic the position and velocity
	sub_odom = rospy.Subscriber("/odom", Odometry, callback_pos_vel)
	
	# Call the client function
	robot_client()
	

if __name__=='__main__':
	main()
