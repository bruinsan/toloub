import math
import qi
from sys import stdout
import time
import argparse

__author__ = "bindrigodossantos"
__copyright__ = "Copyright June 2016, Aldebaran Robotics"

"""
Detect a sound source and print its localization on the TORSO_FRAME of the robot
"""
def main(session):
    motion = session.service("ALMotion")
    memory = session.service("ALMemory")
    sound_localization = session.service("ALSoundLocalization")
    autonomous_life = session.service("ALAutonomousLife")
    
    # robot on the inital state for the test
    # autonomous_life.setState("disabled")
    motion.wakeUp()
    assert not sound_localization.isPaused(), "ALSoundLocalization is Paused"
    
    sound_localization.subscribe("SoundLocation")
    print "Type CTRL+C to stop soundLocalization\n"
    
    try:
        while(True):
            soundPos = memory.getData("ALSoundLocalization/SoundLocated")[1][0]
            stdout.write("\r{0} degrees".format(math.degrees(soundPos)))
            stdout.flush()
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        # unsubscribe and stop sound localization
        sound_localization.unsubscribe("SoundLocation")
        print "\nTest Interrupted!"
    
if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or local Naoqi")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
    


