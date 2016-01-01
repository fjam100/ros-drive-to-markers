#!/usr/bin/env python
import rospy
import pickle
import sys
import thread, time
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker

with open('save.p') as file:
	position_list=pickle.load(file)

topic = 'visualization_marker'
publisher = rospy.Publisher(topic, Marker, queue_size=1)

rospy.init_node('register')

markerArray = MarkerArray()

while not rospy.is_shutdown():
   marker = Marker()
   marker.header.frame_id = 'map'
   marker.header.stamp = rospy.Time.now()
   marker.type = marker.SPHERE
   marker.action = marker.ADD
   marker.ns = 'basic_shapes'
   marker.id = 0
   marker.scale.x = 0.2
   marker.scale.y = 0.2
   marker.scale.z = 0.2
   marker.color.r = 0.0
   marker.color.g = 1.0
   marker.color.b = 0.0
   marker.color.a = 1.0
   counter=0
   for poses in position_list:
	   marker.id=counter
	   marker.pose.orientation.w = 1.0
	   marker.pose.position.x = poses[0][0]
	   marker.pose.position.y = poses[0][1]
	   marker.pose.position.z = poses[0][2]
	   markerArray.markers.append(marker)
	   counter=counter+1
           publisher.publish(marker)
