import math
import qi
import sys

__author__ = "bindrigodossantos"
__copyright__ = "Copyright June 2016, Aldebaran Robotics"

"""
Look at the sound source, using the FRAME_WORLD, with a speed fraction 0.1 and using only the head 
"""

session = qi.Session()
session.connect(sys.argv[1])

tracker = session.service("ALTracker")
motion = session.service("ALMotion")
memory = session.service("ALMemory")
soundloc = session.service("ALSoundLocalization")
life = session.service("ALAutonomousLife")

life.setState("disabled")
motion.wakeUp()

soundloc.subscribe("toto")
print "Type CTRL+C to stop soundLocalization"

try:
    while(True):
        soundPos = memory.getData("ALSoundLocalization/SoundLocated")[1]
	
	x = math.cos(soundPos[1])*math.cos(soundPos[0])
	y = math.cos(soundPos[1])*math.sin(soundPos[0])
	z = math.sin(-soundPos[1])		# elevation doesn't work very well
	
	tracker.lookAt([x,y,0],0,0.1,0)

except KeyboardInterrupt:
    print "Test Interrupted!"

