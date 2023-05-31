#! /usr/bin/env python

"""
.. module:: dist_vel_C
	:platform: Unix
	:synopsis: Python module for the subscriber node C.

.. moduleauthor:: Anna Possamai

This node implements a *subscriber node* that subscribes *to the robots position and velocity* (using the custom message) 
and prints on the console the distance of the robot from the target (set in node action_client_A), 
and its average speed with the frequency set as a parameter in the launch file.

Subscriber:
	/pos_vel

Service client:
	/set_frequency

"""


# import ros stuff
import rospy
from assignment_2_2022.msg import Pos_vel
import math
import time

# Frequency with wich the node publish the information
f = 1.0

# Last time the info was printed
tp=0


def callback(msg):

	"""
	This callback function subscribes to the '/pos_vel' topic and prints the distance of the robot from the target and its average speed.

	Args:
		msg(Pos_vel): the position and velocity of the robot

	"""

	global f, tp

	# convert the current time in milliseconds
	c_time= time.time()*1000

	# compute the period in milliseconds
	p = (1/f)*1000


# calculate distance and the average speed according to the calculated period
	if c_time - tp > p:
 
		# Get the desired position
		x_desired = rospy.get_param("des_pos_x")
		y_desired = rospy.get_param("des_pos_y")

		#Get the actual position and speed
		x = msg.x
		y = msg.y
		v_x=msg.vel_x
		v_y=msg.vel_y

		# Compute the distance of the robot from the target
		d = math.dist([x_desired,y_desired], [x,y])

		# Compute the robot average speed
		average_vel= math.sqrt(v_x**2 + v_y**2)

		#Print the distance and the average speed
		print("Distance from the target: ", d)
		print("Average speed: ", average_vel)

		# Update the last time the info was printed with the current time
		tp = c_time


def main():

	"""
	This function initializes the node and subscribes to the '/pos_vel' topic.
  
	"""

	#Global variable
	global f

	#Initialize the node
	rospy.init_node('dist_vel')

	# Get the publish frequency parameter
	f = rospy.get_param("/publish_frequency")

	# Subscriber to the topic to get the position and velocity
	sub = rospy.Subscriber('/pos_vel', Pos_vel, callback)

	#keep python from exiting until this node is stopped
	rospy.spin()

if __name__ == "__main__":
   
	main()

