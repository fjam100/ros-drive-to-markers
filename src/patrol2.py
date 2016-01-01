#!/usr/bin/env python
import actionlib
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
import pickle
import sys
from random import shuffle
from std_msgs.msg import String
import thread, time




global action_state
action_state=0
global home

class Patrol():
	def __init__(self):
		self.waypoints = [ 
		[(2.5, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0)],
		[(5.5, 5.5, 0.0), (0.0, 0.0, -0.984047240305, 0.177907360295)],
		[(6.5, 4.5, 0.0), (0.0, 0.0, 0.0, 1.0)],
		[(5.5, 2.0, 0.0), (0.0, 0.0, 0.0, 1.0)]
		]
		pickle.dump(self.waypoints, open( "save.p", "wb" ) )


		with open('save.p') as file:
			self.waypoints=pickle.load(file)

		self.scan_sub=rospy.Subscriber('scan', LaserScan, self.scan_callback)
		self.key_sub=rospy.Subscriber('input_key', String, self.key_callback)
		self.home_sub=rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.amcl_callback)
		self.pressed_state=0

	"""def goal_pose(pose): 
		goal_pose = MoveBaseGoal()
		goal_pose.target_pose.header.frame_id = 'map'
		goal_pose.target_pose.pose.position.x = pose[0][0]
		goal_pose.target_pose.pose.position.y = pose[0][1]
		goal_pose.target_pose.pose.position.z = pose[0][2]
		goal_pose.target_pose.pose.orientation.x = pose[1][0]
		goal_pose.target_pose.pose.orientation.y = pose[1][1]
		goal_pose.target_pose.pose.orientation.z = pose[1][2]
		goal_pose.target_pose.pose.orientation.w = pose[1][3]
		return goal_pose
	"""
	def scan_callback(self, scan):	
		#global action_state	
		global home
		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		client.wait_for_server()
	
		for pose in self.waypoints:
			if self.pressed_state==1:
				print('Aborting and returning home')
				goal_pose = MoveBaseGoal()
				goal_pose.target_pose.header.frame_id = 'map'
				goal_pose.target_pose.pose.position.x = home[0][0]
				goal_pose.target_pose.pose.position.y = home[0][1]
				goal_pose.target_pose.pose.position.z = home[0][2]
				goal_pose.target_pose.pose.orientation.x = home[1][0]
				goal_pose.target_pose.pose.orientation.y = home[1][1]
				goal_pose.target_pose.pose.orientation.z = home[1][2]
				goal_pose.target_pose.pose.orientation.w = home[1][3]
				client.send_goal(goal_pose)
				client.wait_for_result()
				self.pressed_state=0
			elif self.pressed_state==2:
				shuffle(self.waypoints)
				self.pressed_state=0
			else:	 
				goal_pose = MoveBaseGoal()
				goal_pose.target_pose.header.frame_id = 'map'
				goal_pose.target_pose.pose.position.x = pose[0][0]
				goal_pose.target_pose.pose.position.y = pose[0][1]
				goal_pose.target_pose.pose.position.z = pose[0][2]
				goal_pose.target_pose.pose.orientation.x = pose[1][0]
				goal_pose.target_pose.pose.orientation.y = pose[1][1]
				goal_pose.target_pose.pose.orientation.z = pose[1][2]
				goal_pose.target_pose.pose.orientation.w = pose[1][3]
				client.send_goal(goal_pose)
				client.wait_for_result()
				#something interesting
				print('Saving LaserScan data to scanData.p')
				print len(scan.ranges)
				pickle.dump(scan.ranges, open( "scanData.p", "wb" ) )

	def key_callback(self,inputkey):
		global home
		if inputkey.data=='h':
			self.pressed_state=1
			client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
			client.wait_for_server()
			client.cancel_all_goals()

		if inputkey.data=='r':
			print('Randomly reordering waypoints')
			self.pressed_state=2
			client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
			client.wait_for_server()
			client.cancel_all_goals()

	def amcl_callback(self,indata):	
		global home		
		home=[(indata.pose.pose.position.x, indata.pose.pose.position.y, indata.pose.pose.position.z), (indata.pose.pose.orientation.x, indata.pose.pose.orientation.y, indata.pose.pose.orientation.z, indata.pose.pose.orientation.w)]
		self.home_sub.unregister() #subscribes only once

if __name__ == '__main__':
	rospy.init_node('patrol')
	run_patrol = Patrol()
	rate = rospy.Rate(10)
    	while not rospy.is_shutdown():
        	rate.sleep()
