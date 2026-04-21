cmake_minimum_required(VERSION 3.8)
project(gp7_vision_pipeline)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BoxDetection.msg"
  DEPENDENCIES std_msgs
)

# Do not use ament_python_install_package() here: it conflicts with
# rosidl_generate_interfaces() for the same project name. Install our
# Python modules next to the generated msg package.
ament_get_python_install_dir(python_install_dir)
install(
  DIRECTORY gp7_vision_pipeline/
  DESTINATION "${python_install_dir}/gp7_vision_pipeline"
  FILES_MATCHING PATTERN "*.py"
)

install(
  PROGRAMS
  scripts/vision_pipeline_placeholder
  scripts/realsense_depth_debug
  scripts/yolo_box_detector_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config models model
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
