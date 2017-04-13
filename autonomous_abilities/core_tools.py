"""
Functional test init
"""

__author__ = "ybrun"
__copyright__ = "Copyright August 2013, Aldebaran Robotics"

import pytest
import time
import ssh_tools
import posixpath
from os import path
from random import choice
from string import ascii_letters, digits, punctuation
from sleekxmpp import ClientXMPP
from distutils.version import LooseVersion
try:
    from qualifcloudsdk import cloud
except ImportError:
    print ("Module qualifcloudsdk not found. This module is required for Cloud tests. "
    "/n /n You can install it via : "
    "/n git clone git@git.aldebaran.lan:qualification-tools/qualification-libraries.git"
    "/n cd QualifCloudSdk/"
    "/n sudo python setup.py install"
    "/n sudo pip install qualifcloudsdk")

def find_wired(services):
    """Returns the service dict of the ethernet connection"""
    for elem in services:
        d = dict(elem)
        if d["Name"] == "Wired":
            return d
    assert False

def find_wifi(services):
    """Returns the service dict of the wifi connection (wifi must be called Now)"""
    for elem in services:
        d = dict(elem)
        if d["Name"] == "Now":
            return d
    assert False

def randstring(length):
    """
    Returns a random string of len length made of uppercase and lowercase letters,
    digits, and usual punctuation
    """
    return ''.join(choice(ascii_letters + digits + punctuation) for _ in range(length))

def install_packages(package_manager, paths):
    """
    Installs packages, returns the list of effectively installed packages
    You MUST pass it absolute paths
    """
    installed = []
    ssh_tools.send_file(paths)
    names = map(path.basename, paths)
    for name in names:
        try:
            if package_manager.install(posixpath.join("/home/nao", name), "tester"):
                installed.append(name)
            else:
                try:
                    package_manager.getPackage(name.split(".")[0])
                    installed.append(name)
                except:
                    pass
        except:
            pass
    return installed


def install_package_relative(package_manager, paths):
    """
    Installs package and returns the list of effectively installed packages

    input: PackageManager proxy, relative path to the file
    """
    ssh_tools.send_file(paths)
    pkg = path.basename(paths)
    package_manager.install("/home/nao/" + pkg)


def remove_package(package_manager, name):
    basename = name.split(".")[0]
    package_manager.remove(basename)
    ssh_tools.delete(name)

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, reply=False):
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if reply:
            rpc = msg['body']
            cmd = rpc.replace(jid, msg['from'])
            msg.reply(cmd).send()
        else:
            operator.notif(msg['body'])

def set_cloud_image(type_version, vnum1=1, vnum2=22, vnum3=3, vnum4=49, domain="cloud-test.aldebaran-robotics.com"):
    """ Set the version of the image to download (on the cloud)
    """
    sdk = cloud.Cloud(domain)
    sdk.set_credentials(oauth=True)
    response = sdk.post_ade_api_profiles(data={"name": "qualif-sw-tests",
                                               "owner": "",
                                               "admins": ""})
    decoded_data = json.loads(response.text)
    pid = decoded_data['id']
    sdk.delete_ade_api_profiles_system(pid)
    sdk.post_ade_api_profiles_system(pid, data={"filter_type": type_version,
                                                "filter_vnum1": vnum1,
                                                "filter_vnum2": vnum2,
                                                "filter_vnum3": vnum3,
                                                "filter_vnum4": vnum4})
    sdk.delete_ade_api_profiles(pid)

class SystemDownloadChecker(object):

    """ Module to catch SystemImageDownloaded event
    """

    def __init__(self):
        """ __init__
        """
        self.downloaded = False

    def getDownloaded(self):
        """ Getter
        """
        return self.downloaded

    def test(self, value):
        """Callback when SystemImageDownloaded is raised.
        """
        self.downloaded = True

def raiseEventAfterDelay(memory, event, value, delay):
    """ Created to be used in threads - which allows to raise an event in the
        background after a defined delay (you can do other stuff in the meantime)
    """
    time.sleep(delay)
    memory.raiseEvent(event, value)

def systemNotifIdsWith0arg():
    """ Return the list of system notification ids which does not need any argument to construct their message
    """
    return [12, 110, 111, 120, 200, 201, 202, 203, 204, 205, 214, 215, 400, 401, 402, 404, 405, 500, 501, 600, 712, 725, 726, 730, 731, 800, 801, 802, 803, 805, 806, 810, 900, 901, 902, 903, 920, 921, 922, 923]

def systemNotifIdsWith1argVersion():
    """ Return the list of system notification ids which needs one argument (a version number) to construct their message
    """
    return [10, 11, 100, 101, 102, 103, 104, 105, 840]

def systemNotifIdsWith1argDevices():
    """ Return the list of system notification ids which needs one argument (a list of devices) to construct their message
    """
    return [720, 721, 722, 723, 724]

def systemNotifIdsWith1argApps():
    """ Return the list of system notification ids which needs one argument (a list of app names) to construct their message
    """
    return [830, 832, 834]

def systemNotifIdsWith2args():
    """ Return the list of system notification ids which needs two arguments (a number and a list of devices) to construct their message
    """
    return [710, 711, 713, 714]

def systemAllNotifIds():
    """ Return the list of all existing system notification ids
    """
    return systemNotifIdsWith0arg() + systemNotifIdsWith1argVersion() + systemNotifIdsWith1argDevices() + systemNotifIdsWith1argApps() + systemNotifIdsWith2args()

def argsForSystemId(systemId):
    """ Return an example of valid arguments corresponding to a system notification id and needed to construct its message
    """
    # if 1 arg expected (version number)
    if systemId in systemNotifIdsWith1argVersion():
        return ["1.2.3"]
    # if 1 arg expected (list of devices)
    if systemId in systemNotifIdsWith1argDevices():
        return ["right leg, left arm"]
    # if 1 arg expected (list of apps)
    if systemId in systemNotifIdsWith1argApps():
        return ["Cocoro, Awesome dance"]
    # if 2 args expected (number of devices, list of devices)
    if systemId in systemNotifIdsWith2args():
        return ["2", "right arm, left leg"]
    # if 0 arg expected
    return []

def check_alvalue_internal_notification(value):
    """
    Description : Checks that value is well formatted.
    "id": int higher or equal to -1
    "severity": "error" or "warning" or "info"
    "removeOnRead": true or false
    "msgParts": array of strings
    "msgArgs": array of strings
    "immediate": true or false
    "sysId": int higher or equal to 0
    For example:
       [["id", 2],
        ["severity", "info"],
        ["removeOnRead", true],
        ["msgParts", ["#I could not update my applications.", "#They are too %s."]],
        ["msgArgs", ["#lame"]],
        ["immediate", false],
        ["sysId", 42]]
    """
    assert(isinstance(value["id"], long))
    assert(value["id"] >= -1)
    assert(isinstance(value["severity"], str))
    assert(value["severity"] in ["info", "warning", "error"])
    assert(isinstance(value["removeOnRead"], bool))
    assert(isinstance(value["msgParts"], list))
    for msgPart in value["msgParts"]:
        assert(isinstance(msgPart, str))
    assert(isinstance(value["msgArgs"], list))
    for msgArg in value["msgArgs"]:
        assert(isinstance(msgArg, str))
    assert(isinstance(value["immediate"], bool))
    assert(isinstance(value["sysId"], long))
    assert(value["sysId"] >= 0)


def clear_notifications(notification_manager):
    """
    Remove all notifications in ALNotificationManager queue
    """
    notif_ids = [dict(n)['id'] for n in notification_manager.notifications()]
    for notif_id in notif_ids:
        notification_manager.remove(notif_id)


def compare_systemVersion(version1, version2):
    """
    inputs:
        version1: string
        version2: string
    Return:
        true if version1 >= version2
        false if version1 < version2
    Exemple:
        for version1 = '2.5.1.15' and version2 = '2.5.0.20'   --> True
        for version1 = '2.5.1.15' and version2 = '2.5.1.120'  --> False
        for version1 = '2.5.1.15' and version2 = '2.5.1.15'   --> True
        for version1 = '2.5.1.15' and version2 = '2.5.1'   --> True
        for version1 = '2.6.1' and version2 = '2.5.0'   --> True
    """
    return LooseVersion(version1) >= LooseVersion(version2)

def get_naoqi_version_from_robot():
    "get NAOqi version from robot"
    output = ssh_tools.runcommand("cat /etc/lsb-release | grep DISTRIB_RELEASE | cut -d'=' -f2")
    try:
        version_number = "{}.{}".format(output.split('.')[0],output.split('.')[1])
    except:
        version_number = ""
    return version_number
