#!/bin/bash

for i in $(ls apps/); do
	qicli call PackageManager.install apps/$i
done
