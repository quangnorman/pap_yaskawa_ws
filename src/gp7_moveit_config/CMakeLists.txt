cmake_minimum_required(VERSION 3.22)
project(gp7_moveit_config)


find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch config legacy
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS scripts/verify_plan_execute.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()