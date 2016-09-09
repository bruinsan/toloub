#!/bin/bash

for i in $(ls apps/); do
	echo "Installing application: ${i}"
	qicli call PackageManager.install /home/nao/apps/$i
done
