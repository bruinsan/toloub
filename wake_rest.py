#!/usr/bin/python

import qi			# robot communication
import sys

"""
We don't need sleep function because wakeUp and rest function are blocking
"""
robot_ip = sys.argv[1]

session = qi.Session()		# create a section with qi

session.connect(robot_ip)	# connecting to the robot ()
mode = session.service("ALMotion")

while True:
	try:
		mode.wakeUp()
		mode.rest()
	except KeyboardInterrupt:
		print ""
		print "Exiting..."
		sys.exit()
