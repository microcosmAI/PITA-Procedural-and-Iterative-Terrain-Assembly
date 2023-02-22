#!/bin/bash
read -p "Enter the path to your MuJoCo folder: " MUJOCO_PATH

echo ""

"$MUJOCO_PATH/bin/simulate" "$(dirname "$0")/export/test.xml"