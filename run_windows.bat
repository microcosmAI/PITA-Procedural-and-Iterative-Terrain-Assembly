@echo off

set /p MUJOCO_PATH=Enter the path to your MuJoCo folder:

echo.

%MUJOCO_PATH%\bin\simulate export\output.xml