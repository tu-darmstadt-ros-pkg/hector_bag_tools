cmake_minimum_required(VERSION 2.8.3)
project(hector_bag_tools)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rosbag
  rospy
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES hector_bag_tools
#  CATKIN_DEPENDS rosbag rospy
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(
  PROGRAMS scripts/split_bag
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
