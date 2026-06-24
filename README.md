# Lab 04b - Robot Architecture - ROS

ROS-Noetic-Applikation für Turtlebot3 waffle_pi mit Kameraverarbeitung, eigener Message, Logging-Service, Wall Follower und Bewegung zwischen zwei Objekten.

## Voraussetzungen

- Ubuntu 20.04
- ROS Noetic
- Turtlebot3 Packages im Catkin Workspace
- OpenCV / cv_bridge

## Build

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
