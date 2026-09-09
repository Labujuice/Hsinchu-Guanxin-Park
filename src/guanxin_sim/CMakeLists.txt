cmake_minimum_required(VERSION 3.8)
project(guanxin_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python teleop script as an executable in lib/guanxin_sim/
install(PROGRAMS
  guanxin_sim/teleop_vehicle.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME teleop_vehicle
)

# Install launch, worlds, models directories into share/guanxin_sim/
install(DIRECTORY
  launch
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
