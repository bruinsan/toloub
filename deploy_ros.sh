#!/bin/bash
##
## Usage :
## ./deploy_ros.sh
##
## Login : <mballarini@aldebaran.com>
## Started on  Mon Jun 13 17:21:46 2016 Matthias BALLARINI
##
## Author(s):
##  - Matthias BALLARINI <>
##
## Copyright (C) 2016 Matthias Ballarini

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116

sudo apt-get update

sudo apt-get install python-wstool -y

sudo apt-get install libsdformat1 -y

sudo apt-get install libsdformat-dev -y

sudo apt-get install gazebo2 -y

sudo apt-get install ros-indigo-gazebo-ros -y

sudo apt-get install ros-indigo-gazebo-ros-pkgs -y

sudo apt-get install ros-indigo-desktop-full -y

sudo apt-get install ros-indigo-driver-base ros-indigo-move-base-msgs ros-indigo-octomap ros-indigo-octomap-msgs ros-indigo-humanoid-msgs ros-indigo-humanoid-nav-msgs ros-indigo-camera-info-manager ros-indigo-camera-info-manager-py ros-indigo-rqt-bag ros-indigo-rqt-bag -y

#sudo apt-get install ros-indigo-pepper-meshes -y

printenv | grep ROS

source /opt/ros/indigo/setup.zsh

mkdir -p ~/catkin_ws/src

cd ~/catkin_ws/src

catkin_init_workspace

cd ~/catkin_ws/

catkin_make

source devel/setup.zsh

echo "ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH"

roscd

env | grep ROS

cd ~/catkin_ws/src

echo "- git: {local-name: pepper_robot, uri: \"https://github.com/ros-naoqi/pepper_robot\", version: master}
- git: {local-name: naoqi_injector, uri: \"git@gitlab.aldebaran.lan:ros/naoqi_injector\", version: master}
- setup-file: {local-name: ../devel/setup.zsh }" > .rosinstall

wstool update

cd naoqi_injector
git checkout -b stereo_injection origin/stereo_injection

cd ../..
catkin_make
source devel/setup.zsh

echo "source ~/catkin_ws/devel/setup.zsh" >> ~/.zshrc

cd ~/catkin_ws

catkin_make -j8

echo "source /opt/ros/indigo/setup.zsh" >> ~/.zshrc

source ~/.zshrc

exit 0
