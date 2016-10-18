#!/bin/bash

for i in `seq 1 10`;
do
    qicli call ALPhotoStorage.takePhoto 1 1 1
done
