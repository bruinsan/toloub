import math
import qi
import sys
import time
import argparse

__author__ = "bindrigodossantos"
__copyright__ = "Copyright June 2016, Aldebaran Robotics"

"""
Look at the sound source, using the FRAME_WORLD, with a speed fraction 0.1 and using only the head 
"""
def main(session,distance, confidence):
    motion = session.service("ALMotion")
    tracker = session.service("ALTracker")

    motion.wakeUp()

    # Add Target to track
    targetName = "Sound"
    distanceSource = distance
    filterConfidence = confidence
    tracker.registerTarget(targetName,[distanceSource, filterConfidence])

    # set mode
    mode = "Head"
    tracker.setMode(mode)

    # start tracker
    tracker.track(targetName)

    try:
        while True:
            time.sleep(1)
    except:
        print "Stopping"

    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()


if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or local Naoqi")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--dist", type=float, help="distance to the object")
    parser.add_argument("--confid",type=float, help="filter confidence")    

    args = parser.parse_args()
    print args
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.dist, args.confid)
    
