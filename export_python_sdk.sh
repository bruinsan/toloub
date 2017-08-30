#!/bin/sh

# Maintainer: bindrigodossantos
# To have the variable available in your session, you must source this file

# getting python sdk path ../pythonsdk/
PYTHON_SDK_PATH=$(echo $PYTHONPATH | sed 's|/lib.*||g')

# exporting to the session the two needed variables on MAC OS
export DYLD_LIBRARY_PATH=$PYTHON_SDK_PATH/lib
export DYLD_FRAMEWORK_PATH=$PYTHON_SDK_PATH

