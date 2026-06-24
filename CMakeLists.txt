cmake_minimum_required(VERSION 3.0.2)
project(lab4)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  message_generation
)

add_message_files(
  FILES
  RobotStatus.msg
)

add_service_files(
  FILES
  ToggleLogging.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs geometry_msgs message_runtime
)

catkin_install_python(PROGRAMS
  scripts/camera_node.py
  scripts/status_publisher.py
  scripts/logging_control.py
  scripts/logger.py
  scripts/wall_follower.py
  scripts/move_between_objects.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
