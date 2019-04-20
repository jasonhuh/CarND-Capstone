waypoint_updater
============================================
term1$ cd /home/student/CarND-Capstone/ros
term1$ catkin_make
term1$ source devel/setup.sh
term1$ roslaunch launch/styx.launch
term2$ cd /home/student/CarND-Capstone/ros
term2$ source devel/setup.sh
term2$ rostopic list
term2$ rostopic echo /final_waypoints
term2$ rosmsg info styx_msgs/Lane

twist_controller (DBW)
=============================================
term1$  cd /home/student/CarND-Capstone/ros/src/twist_controller
