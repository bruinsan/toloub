#!/bin/bash

for i in $(ls $1/); do
	echo "Installing application: ${i}"
	qicli call PackageManager.install /home/nao/$1/$i
done
