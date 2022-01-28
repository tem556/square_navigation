#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the Python library for ROS
import rospy
# Import the library for generating random numbers
import random
# Import the Twist message from the geometry_msgs package
# Twist data structure is used to represent velocity components
from geometry_msgs.msg import Twist

# TF allows to perform transformations between different coordinate frames
import tf

# Import the Odometry message
from nav_msgs.msg import Odometry


class RndVelocityGen():

	def __init__(self):

	# Initiate a node named random velocity
	rospy.init_node("SQUARE")

	# Create a Publisher object, that will publish on /new_vel topic
	# messages of type Twist
	self.vel_pub = rospy.Publisher("/new_vel", Twist, queue_size=1)

	# Creates var of type Twist
	self.vel = Twist()

	# Assign and publish initial velocities
	self.vel.linear.x = 0.3  # m/s
	self.vel.angular.z = 0.0  # rad/s
	self.vel_pub.publish(self.vel)
	rospy.loginfo("Initial velocities: [%5.3f, %5.3f]",
	              self.vel.linear.x, self.vel.angular.z)

	# Subscribe to topic /odom published by the robot base
	self.odom_sub = rospy.Subscriber("/odom", Odometry, self.callback_odometry)


	# Set max value for max time interval between velocity changes,
	# min is set to 1
	self.max_interval = 10

	# Holds the temp vals for x and y
	self.xTemp = 0
	self.yTemp = 0

	self.angle = 0


	def callback_odometry(self, msg):
		self.xTemp = msg.pose.pose.position.x


		self.yTemp = msg.pose.pose.position.y

		self.angle = self.quaternion_to_euler(msg)


	def generate_square_velocities(self):


		for i in range(5):
			# This part is for going to 3, 0
			while (self.xTemp < 3):
				self.vel.linear.x = 0.3
				self.vel_pub.publish(self.vel)
				rospy.sleep(0.1)

			self.vel.linear.x = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)

			while (self.angle < 1.5):
				self.vel.angular.z = 0.3
				self.vel_pub.publish(self.vel)

				rospy.sleep(0.25)

			self.vel.angular.z = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)

			# This part is for going to 3,3
			while (self.yTemp < 3):
				self.vel.linear.x = 0.3
				self.vel_pub.publish(self.vel)
				rospy.sleep(0.1)

			self.vel.linear.x = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)

			while (self.angle < 3):
				self.vel.angular.z = 0.3
				self.vel_pub.publish(self.vel)

				rospy.sleep(0.1)

			self.vel.angular.z = 0
			self.vel_pub.publish(self.vel)

			# This part is for reaching 0, 3
			while (self.xTemp > 0):
				self.vel.linear.x = 0.3
				self.vel_pub.publish(self.vel)
				rospy.sleep(0.1)

			self.vel.linear.x = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)

			while (abs(self.angle) > 1.5):
				self.vel.angular.z = 0.3
				self.vel_pub.publish(self.vel)

				rospy.sleep(0.1)

			self.vel.angular.z = 0
			self.vel_pub.publish(self.vel)

			# This part is for reaching back to origin point
			while (self.yTemp > 0):
				self.vel.linear.x = 0.3
				self.vel_pub.publish(self.vel)
				rospy.sleep(0.1)

			self.vel.linear.x = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)

			while (self.angle < 0):
				self.vel.angular.z = 0.3
				self.vel_pub.publish(self.vel)

				rospy.sleep(0.1)

			self.vel.angular.z = 0
			self.vel_pub.publish(self.vel)

			rospy.sleep(1)


	def quaternion_to_euler(self, msg):
		quaternion = (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
		              msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)


		(roll, pitch, yaw) = tf.transformations.euler_from_quaternion(quaternion)
		return yaw



# Sleeps for the selected seconds
if __name__ == "__main__":
	generator = RndVelocityGen()
	generator.generate_square_velocities()
