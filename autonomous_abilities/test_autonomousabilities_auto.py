# -*- encoding: UTF-8 -*-
"""
AutonomousAbilities Service API test

__author__ = "bdjellab"
__copyright__ = "Copyright September 2016, Softbank Robotics Europe"
"""

import pytest
import time
from tools.core_tools import install_package_relative, remove_package
from os import path

def event_count():
    global counter
    counter += 1


def test_handle_holdAutonomousAbilities_bft(autonomous_abilities, focus,
                                            context_factory, autonomous_life):
    """
    Description : This tests verifies that holding an autonomous ability only
    holds the right one and that releasing the handles re-enables each
    autonomous ability one by one. It also checks the released signal for
    each handle
    """
    focus_handle = focus.take()
    context = context_factory.makeContext()
    context.focus.setValue(focus_handle)

    aa_status = autonomous_life.getAutonomousAbilitiesStatus()
    aa_names_list = [elem['name'] for elem in aa_status]
    init_aa_status = list(aa_status)
    handle_list = list()

    # Hold all AA one by one and check their status
    for aa_name in aa_names_list:
        old_aa_status = list(aa_status)
        current_method = getattr(autonomous_abilities, "hold" + aa_name)
        handle_list.append(current_method(context))
        aa_status = autonomous_life.getAutonomousAbilitiesStatus()
        for aa_status_elem in aa_status:
            for elem in old_aa_status:
                if elem['name'] == aa_status_elem['name']:
                    old_aa_status_elem = elem
                    break
            if(aa_status_elem['name'] == aa_name):
                if aa_status_elem['enabled'] or aa_status_elem['running']:
                    pytest.fail("{} was not "
                                "hold properly".format(aa_status_elem['name']))
            else:
                test_enabled = (aa_status_elem['enabled'] ==
                                old_aa_status_elem['enabled'])
                test_running = (aa_status_elem['running'] ==
                                old_aa_status_elem['running'])
                if not (test_enabled and test_running):
                    pytest.fail("{} should not be hold at this "
                                "point".format(aa_status_elem['name']))

    # Release all AA handles and check if we get the initial state back
    conn_id_list = list()
    global counter
    counter = 0
    for handle in handle_list:
        conn_id_list.append(handle.released.connect(event_count))
        handle.release()
    if counter != 5:
        pytest.fail("Released signal was raised {} times instead "
                    "of 5".format(counter))
    aa_status = autonomous_life.getAutonomousAbilitiesStatus()
    for aa_status_elem in aa_status:
        init_aa_status_elem = [elem for elem in init_aa_status if
                               elem['name'] == aa_status_elem['name']][0]
        test_enabled = (aa_status_elem['enabled'] ==
                        init_aa_status_elem['enabled'])
        test_running = (aa_status_elem['running'] ==
                        init_aa_status_elem['running'])
        if not (test_enabled and test_running):
            pytest.fail("{} did not go to its initial state "
                        "when its handle was "
                        "released".format(aa_status_elem['name']))
    for handle, conn_id in zip(handle_list, conn_id_list):
        handle.released.disconnect(conn_id)


@pytest.mark.critical
def test_event_autonomousAbilities_launchedApp(autonomous_life, behavior_manager,
                                               package_manager, request):
    """
    Check Autonomous Abilities during the launching of an application

    :Steps:
        Launch application pkg which stops all autonomous abilities for 5s
        Check if all abilities were stopped
        Check if abilities were enabled after end of application

    :Expected:
        The application can stop autonomous abilities during execution
        After application exiting, life can restore autonomous abilities

    :Testrail ID:
        C49448

    :Test type:
        functional

    :Comments:

    """
    pkg_path = "../stopabilities.pkg"
    install_package_relative(package_manager, pkg_path)
    autonomous_life.setState("solitary")

    # check any activity is focused
    if autonomous_life.focusedActivity():
        autonomous_life.stopFocus()

    # get initial state of all autonomous abilities
    aa_initial_list = autonomous_life.getAutonomousAbilitiesStatus()

    # run application that changes autonomous abilities status (it lasts 5s)
    autonomous_life.switchFocus("stopabilities/behavior_1")

    # check activity was launched correctly and life is focused on it
    if not autonomous_life.focusedActivity() == "stopabilities/behavior_1":
        pytest.fail("Autonomous Life is not focused on: {}"
                    .format("stopabilities/behavior_1"))

    time.sleep(1)

    # get autonomous abilities during app execution
    aa_list = autonomous_life.getAutonomousAbilitiesStatus()

    # check if all abilities were correctly disabled
    for ability in aa_list:
        if ability["enabled"]:
            pytest.fail("Ability {} is enabled yet".format(ability["name"]))

    time.sleep(7)  # Time for application to end

    # get abilities status after stopping activity
    aa_list = autonomous_life.getAutonomousAbilitiesStatus()

    if aa_initial_list != aa_list:
        pytest.fail("Life has not restart autonomous abilities correctly")

    def ending():
        behavior_manager.stopAllBehaviors()
        autonomous_life.setState("disabled")
        remove_package(package_manager, path.basename(pkg_path))
    request.addfinalizer(ending)
