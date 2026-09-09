#!/bin/bash
set -e

# 載入 ROS 2 Jazzy 環境
source "/opt/ros/$ROS_DISTRO/setup.bash"

# 載入 guanxin_sim 工作區環境
if [ -f "/ros2_ws/install/setup.bash" ]; then
    source "/ros2_ws/install/setup.bash"
fi

# 設定 Gazebo Harmonic 資源路徑
export GZ_SIM_RESOURCE_PATH="/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models:${GZ_SIM_RESOURCE_PATH}"
export SDF_PATH="/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models:${SDF_PATH}"
export GZ_FILE_PATH="/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models:${GZ_FILE_PATH}"

exec "$@"
