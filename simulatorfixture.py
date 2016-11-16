#!/usr/bin/python2.7
# encoding: UTF-8

# ==============================================================================
#                     ALDEBARAN-SOFTBANK GROUP - VISION
# ==============================================================================
# PROJECT : Vision Test Contents
# FILE : simulatorfixture.py
# TEST_ID :
# DESCRIPTION :
"""
Fixture for vision tests

"""

# [IMPORTS]---------------------------------------------------------------------
import pytest
from tools import ssh_tools
import time


# [MODULE INFO]-----------------------------------------------------------------
__author__ = ["ybrun", "kota"]
__date__ = "2016-02-19"
__copyright__ = "Copyright 2016, Aldebaran-Robotics (c)"
__version__ = "0.0.1"
__maintainer__ = "kota"
__email__ = "kota@aldebaran.com"


# [GLOBALS]---------------------------------------------------------------------


# ------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def simulator(request):
    """
    Set Video Mode as Simulator
    """
    pid = ssh_tools.get_naoqi_pid()
    naoqi_path = ssh_tools.get_naoqi_path(pid)

    if naoqi_path == "/opt/aldebaran/bin/naoqi-bin":
        file_path_in = '/opt/aldebaran/etc/naoqi/VideoDevice.xml'
        file_path_out = '/home/nao/.config/naoqi/VideoDevice.xml'
    else:
        raise Exception("No naoqi_path")
    ssh_tools.exec_command_one_line("cp {} {}".format(file_path_in,
                                                      file_path_out))
    ssh_tools.runcommand("sed -i 's/Robot/Simulator/g' {}"
                         .format(file_path_out))
    ssh_tools.nao_restart()
    time.sleep(60)

    def ending():
        """
        End of simulator mode
        """
        ssh_tools.runcommand("sed -i 's/Simulator/Robot/g' {}"
                             .format(file_path_out))
        ssh_tools.nao_restart()
        time.sleep(60)
    request.addfinalizer(ending)


@pytest.fixture
def simulate_to_2d(request, people_perception):
    """
    Set Simulation mode to 2D
    """
    mode = people_perception._getDetectionMode()
    people_perception._setDetectionMode("2D")

    def ending():
        """
        Reset Simulation mode to previous state.
        """
        people_perception._setDetectionMode(mode)

    request.addfinalizer(ending)


@pytest.fixture(scope="function")
def simulator_with_life(simulator, diagnosis, motion, autonomous_life):
    """
    Set Video Mode as Simulator and enables life
    """
    # wait for the end of robot boot
    while True:
        if autonomous_life.getState() == "safeguard":
            break

    autonomous_life.setState("disabled")
    motion.setDiagnosisEffectEnabled(0)
    diagnosis._clearActiveDiagnosis()
    autonomous_life.setState("solitary")

@pytest.fixture(scope="function")
def wait_for_solitary(session, autonomous_life):
    print "Waiting for solitary mode!!!!!!!!!!!!!!"
    while True:
        print "ici"
        if autonomous_life.getState() == "solitary":
            break
    print "Exiting solitary mode = {}".format(autonomous_life.getState())
