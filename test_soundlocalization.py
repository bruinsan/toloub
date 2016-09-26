import math
import qi
import sys
import time

__author__ = "bindrigodossantos"
__copyright__ = "Copyright June 2016, Aldebaran Robotics"

"""
Look at the sound source, using the FRAME_WORLD, with a speed fraction 0.1 and using only the head 
"""
print sys.argv[0], sys.argv[1]
session = qi.Session()
session.connect(sys.argv[1])

tracker = session.service("ALTracker")
motion = session.service("ALMotion")
memory = session.service("ALMemory")
soundloc = session.service("ALSoundLocalization")
life = session.service("ALAutonomousLife")

#life.setState("disabled")
motion.wakeUp()

soundloc.subscribe("SoundLocate")
print "Type CTRL+C to stop soundLocalization"

try:
    while(True):
        soundPos = memory.getData("ALSoundLocalization/SoundLocated")[1]
        print "polar coord = ", soundPos, "\n"
        print "confidence = ", soundPos[2], "\n"
        
        if soundPos[2] > 0.75:
            x = math.cos(soundPos[1])*math.cos(soundPos[0])
            y = math.cos(soundPos[1])*math.sin(soundPos[0])
            z = math.sin(-soundPos[1])		# elevation doesn't work very well
            print "x,y,z = ", [x,y,z], "\n"

            tracker.lookAt([x,y,z],0,0.1,0)
        time.sleep(0.5)

except KeyboardInterrupt:
    # unsubscribe and stop sound localization
    soundloc.unsubscribe("SoundLocate")
    print "Test Interrupted!"

