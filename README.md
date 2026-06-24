# Lab 04b - Robot Architecture - ROS

ROS-Noetic-Applikation für Turtlebot3 waffle_pi mit Kameraverarbeitung, eigener Message, Logging-Service, Wall Follower und Bewegung zwischen zwei Objekten.

## Build

cd ~/catkin_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle_pi

## Start

Wall Follower:
roslaunch lab4 wall_follower.launch

Move Between Objects:
roslaunch lab4 move_between_objects.launch

## Logging Service

Logging ausschalten:
rosservice call /toggle_logging "enable: false"

Logging einschalten:
rosservice call /toggle_logging "enable: true"

## Inhalte

- camera_node.py: Kamera mit cv_bridge und OpenCV
- RobotStatus.msg: Geschwindigkeit und LiDAR-Abstände
- status_publisher.py: veröffentlicht RobotStatus
- logger.py: speichert RobotStatus als CSV
- logging_control.py: Logging-Service
- wall_follower.py: Wandfolger
- move_between_objects.py: fährt zwischen zwei Objekten hin und her
- two_objects.world: eigene Gazebo-Welt
