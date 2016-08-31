#!/bin/bash

files=$(ls /home/nao/.local/share/photostorage)

file_name=`echo "$files" | cut -d'.' -f1`

for photo in $file_name 
do
    qicli call ALPhotoStorage.setMetadata $photo FAVORITE 1
done
