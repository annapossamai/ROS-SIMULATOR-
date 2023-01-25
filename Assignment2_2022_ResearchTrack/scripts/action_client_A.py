#! /usr/bin/env python

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
