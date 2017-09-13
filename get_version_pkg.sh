#!/bin/bash

for i in $(ls); do
	for j in $(ls $i); do
		if [ "$j" == "manifest.xml" ]; then
			sed -n '2p' $PWD/$i/$j
		fi
	done
	echo "next application"
done
