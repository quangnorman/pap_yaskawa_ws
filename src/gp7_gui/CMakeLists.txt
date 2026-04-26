cmake_minimum_required(VERSION 3.8)
project(gp7_gui)

if(CMAKE_VERSION VERSION_LESS "3.12")
  set(CMAKE_POLICY_VERSION_MINIMUM 3.10)
endif()

find_package(ament_cmake REQUIRED)

ament_python_install_package(
  ${PROJECT_NAME}
  SETUP_CFG "${CMAKE_CURRENT_SOURCE_DIR}/setup.cfg"
)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}/
)
install(DIRECTORY resource
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
