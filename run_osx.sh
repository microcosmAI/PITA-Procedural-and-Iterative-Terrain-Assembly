#!/bin/sh
set -m 

read -p "Enter the path to your MuJoCo folder:" MUJOCO_PATH

echo

$MUJOCO_PATH/MuJoCo.app/Contents/MacOS/simulate "$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"/export/test.xml