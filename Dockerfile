FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy

# 安裝 Gazebo Harmonic 與 ros_gz 整合套件、GUI/X11 依賴與 OpenCV
RUN apt-get update && apt-get install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-ros-gz-interfaces \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-cv-bridge \
    ros-jazzy-image-transport \
    python3-pip \
    python3-colcon-common-extensions \
    python3-opencv \
    libgl1-mesa-dri \
    libglx-mesa0 \
    libgl1 \
    libegl1 \
    xterm \
    evtest \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# 設定環境變數
ENV QT_X11_NO_MITSHM=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV GZ_SIM_RESOURCE_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models
ENV SDF_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models
ENV GZ_FILE_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models

WORKDIR /ros2_ws
COPY src /ros2_ws/src

# 構建 ROS 2 工作區
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --symlink-install

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc && \
    echo "export GZ_SIM_RESOURCE_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models" >> /root/.bashrc && \
    echo "export SDF_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models" >> /root/.bashrc && \
    echo "export GZ_FILE_PATH=/ros2_ws/src/guanxin_sim/models:/ros2_ws/install/guanxin_sim/share/guanxin_sim/models" >> /root/.bashrc

CMD ["/bin/bash"]
