#! /usr/bin/env python

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
	
	global goal_cancelled, goal_reached
	
	#return the rensponse	
	return GoalResponse(goal_reached, goal_cancelled)
	
	

def goal_number(msg):
	
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
		

	




	
	
