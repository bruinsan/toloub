import yaml
import sys
from time import time

from fabric.api import env, run

output_file = "leak_stat.txt"           # output spreadsheet with memory usage
process_name = "process_names.yaml"     # yaml file containing all the names of the analysed process 
remote_memory_stat = "top.txt"          # 1 second updated remote file (ps command on the robot)
                                        # layout = {pid memory command}

env.host_string = sys.argv[1]
env.password = "nao"
env.user = "nao"

class p_stat(object):
    """
    Manage memory usage statistics 
    """

    def __init__(self):
        self.list_proc = dict()         # list of process on analysis from yaml config file
        self.timestamps = float         # timestamp printed to output file
        self.memory_usage = list()      # memory usage of each process (sorted list)

    def _check_contains_process(self, line):
        """
        check if line has one of process from list_proc
        """
        """
        for procces in self.list_proc:
            if proccess in line:
                open file and add to its column the memory usage and timestamp

        maybe it won't work, we need to sort the lines accordly to list_proc and write all
        together to the file
        """
        pass


    def _get_remote_stat(self):
        """
        Retrieves top.txt with fabric and
        fills timestamps and memory_usage
        """
        top = run("cat top.txt")
        if top != '':       # top.txt may be blank
            self.timestamps = time()
            top_list = top.split("\r\n")

            for elem in top_list:
                elem_split = elem.split()   # each line splitted in pid/memory/command
                self._check_contains_process(elem_split)

    def write_stat(self):
        self._get_remote_stat()

        with open(output_file, "a") as fl:
            pass

    def _get_list_process(self):
        with open(process_name, "r") as fl_name:
            self.list_proc = yaml.load(fl_name)

    def write_process_names(self):
        """
        Header of output file
        Fills with the process names separeting by \t
        """
        self._get_list_process()

        with open(output_file, "w") as out:
            out.write("\t")         # first column for timestamp
            for proc in self.list_proc['process']:
                out.write("{}\t".format(proc))


write_process_names()
