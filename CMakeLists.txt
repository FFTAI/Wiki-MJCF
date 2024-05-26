cmake_minimum_required(VERSION 3.0.2)
project(urdf2mjcf)

find_package(catkin REQUIRED)

catkin_python_setup()

catkin_package()

catkin_install_python(
  PROGRAMS
  scripts/urdf2mjcf
  scripts/urdf2mjcf_ros
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

if (CATKIN_ENABLE_TESTING)
  catkin_add_nosetests(test)
endif()