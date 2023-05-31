#! /usr/bin/env python

"""
.. module:: service_node_B
	:platform: Unix
	:synopsis: Python module for the service node B.
    
.. moduleauthor:: Anna Possamai

This node implements a *service node* that, when it is called, prints the number of goals reached and cancelled;

Service:
	/goal_n
    
Subscriber:	
	/reaching_goal/result

"""

# import ros stuff
import rospy
import assignment_2_2022.msg
from assignment_2_2022.srv import Goal, GoalResponse
import actionlib
import actionlib.msg



#Initialization of the goal variables
goal_reached=0;
goal_cancelled=0;


def goal_rensponse(req):
	"""
	This function is called when the service is called and returns the number of reached and cancelled goals.

	Args:
		req(GoalRequest): the request of the service

	Returns:
		GoalResponse: the response of the service

	"""
	
	global goal_cancelled, goal_reached
	
	#return the rensponse	
	return GoalResponse(goal_reached, goal_cancelled)
	
	

def goal_number(msg):
	"""
	This callback function subscribes to the '/reaching_goal/result' topic and updates the number of reached and cancelled goals.

	Args:
		msg(): the result of the action

	"""


	global goal_cancelled, goal_reached
	
	# Get the goal status from the msg	
	status = msg.status.status
	
	# Upload the number of reached goal (status = 3)	
	if status == 3:
		goal_reached = goal_reached + 1
	
	# Upload the number of cancelled goal (status = 2)
	elif status == 2:
		goal_cancelled = goal_cancelled + 1



def main():
	"""
	This function initializes the node, subscribes to the '/reaching_goal/result' topic and provides the service '/goal_n'.

	"""
	
	# Initialize the node
	rospy.init_node('service')
	
	# Subscriber to the result topic to get the status
	sub = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, goal_number)
	
	# Create the service
	s = rospy.Service('goal_n', Goal, goal_rensponse)
	
	# keep pytho from exiting until this node is stopped
	rospy.spin()

if __name__=="__main__":
	main()
