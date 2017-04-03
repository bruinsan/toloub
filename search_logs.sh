#!/bin/bash

# each 30 seconds, look for the specific string on log files and write to catch_log file if found it 

search=$1
echo "Infinite loop looking for the string: $search"

while :
do
	#echo $search
	tail /var/log/naoqi/*.log* /var/log/naoqi/servicemanager/*.log* | grep -i "$search" -C 5 >> catch_log

	sleep 30

done
