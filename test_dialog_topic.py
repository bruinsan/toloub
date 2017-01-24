import math
import qi
import sys
import time
import argparse

__author__ = "bindrigodossantos"
__copyright__ = "Copyright June 2016, Aldebaran Robotics"

def main(session,topic):
    dialog = session.service("ALDialog")

    topic_name = dialog.loadTopic("/home/nao/"+topic)
    dialog.activateTopic(topic_name)

    dialog.runDialog()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping"
        dialog.deactivateTopic(topic_name)
        dialog.unloadTopic(topic_name)
        dialog.stopDialog()


if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or local Naoqi")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--topic", type=str, help="topic to be tested")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.topic)
    
