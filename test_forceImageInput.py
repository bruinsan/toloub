import time
import pytest

def test_event_forceSleepMode(activate_dcm_injection, simulator_with_life,
                          session, wait_for_solitary, dcm, memory):

    # we need wait_for_solitary to wait boot of naoqi and then have session again
    time.sleep(15)
    dcm._injectionAdd(["Device/SubDeviceList/Head/Touch/Front/Sensor/Value",
                       "Device/SubDeviceList/Head/Touch/Rear/Sensor/Value",
                       "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"],
                      [1.0, 1.0, 1.0])

    print "Going to sleep"
    time.sleep(4)

    print "Stop Injection"
    dcm._injectionStop()

    while True:
        print "waiting for asleep"
        if memory.getData("AutonomousLife/Asleep") == 1:
            time.sleep(10)
            break

    print "Waking up"
    dcm._injectionAdd(["Device/SubDeviceList/Head/Touch/Front/Sensor/Value",
                       "Device/SubDeviceList/Head/Touch/Rear/Sensor/Value",
                       "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"],
                      [1.0, 1.0, 1.0])

    time.sleep(1)
    dcm._injectionStop()

    while True:
        print "waiting for wakeup"
        if memory.getData("AutonomousLife/Asleep") != 1:
            break

    time.sleep(20)      # waiting to wake up position
    print "FINISHED !!!!!!!!!"
