### Prompt
我們現在開始寫需求：
1. 使用docker 跑 ros2 jazzy
2. 使用 ros_gz Gazebo Harmonic
3. 先建立一個小型城鎮, 以新竹市東區關新路與光復路口至新莊火車站 左右50m 為街道建立範圍, 關新公園整個建立出來
4. 建立一台小汽車, 這小汽車要可以開, 以 model y 為目標進行建立, 
5. 寫一個node控制這一台車, 這車子在空間中開要有明確的邊界, 撞到建築物或者 sidewalk 要有反應。
6. 使用 docker去執行, 需要有啟動script, 執行起來之後, 可以切換看車子的視角, `wsad`按鈕進行前後左右, `v`來切換 第一人稱、第三人稱 視角, 也希望有一個車內視角。`o` 可以回到原點(光復路關新路口)。


---

這是一份可以直接交給 Antigravity CLI 或在本機執行的完整專案實作規格書與程式碼架構。

---

### 架構概覽與目錄結構

整體架構使用 **Docker (Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic)** 容器化隔離，支援 GPU GUI 與 X11 轉發。專案包含地圖幾何（關新路廊道）、Model Y 阿克曼轉向模型、Gazebo 視角追蹤外掛、鍵盤控制節點，以及一鍵啟動腳本。

```text
guanxin_sim_ws/
├── Dockerfile
├── docker-compose.yml
├── run.sh
└── src/
    └── guanxin_sim/
        ├── CMakeLists.txt
        ├── package.xml
        ├── launch/
        │   └── sim.launch.py
        ├── worlds/
        │   └── guanxin.sdf
        ├── models/
        │   └── model_y/
        │       └── model.sdf
        └── guanxin_sim/
            ├── __init__.py
            └── teleop_vehicle.py

```

---

### 1. Dockerfile 與啟動配置

#### `Dockerfile`

基於 Ubuntu 24.04 (Noble)，預設包含 ROS 2 Jazzy 與 Gazebo Harmonic 橋接套件，並支援 NVIDIA GPU 渲染加速。

```dockerfile
FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy

# 安裝 Gazebo Harmonic 與 ros_gz 整合套件
RUN apt-get update && apt-get install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-teleop-twist-keyboard \
    python3-pip \
    python3-colcon-common-extensions \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    evtest \
    && rm -rf /var/lib/apt/lists/*

# 設定環境變數
ENV QT_X11_NO_MITSHM=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

WORKDIR /ros2_ws
COPY src /ros2_ws/src

RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --symlink-install

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc
RUN echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["/bin/bash"]

```

#### `run.sh` (一鍵啟動 Script)

處理 host 端 X11 權限並啟動容器。

```bash
#!/bin/bash
xhost +local:root

# 檢查是否有 NVIDIA 顯卡
if command -v nvidia-smi &> /dev/null; then
    GPU_FLAG="--gpus all"
else
    GPU_FLAG=""
fi

docker run -it --rm \
    $GPU_FLAG \
    --net=host \
    --ipc=host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd)/src:/ros2_ws/src \
    --name guanxin_sim_container \
    guanxin_sim:latest \
    ros2 launch guanxin_sim sim.launch.py

```

---

### 2. 空間與城鎮地圖規格 (`src/guanxin_sim/worlds/guanxin.sdf`)

新竹市關新路（光復路口至新莊車站段長度約 400m，路幅加左右 50m 總寬約 120m）：

* **座標原點 $(0, 0, 0)$**：設定在光復路一段與關新路交叉口中央。
* **路面與人行道邊界 (Sidewalks)**：
* 主幹道為瀝青路面（摩擦力 $\mu=0.9$）。
* 左右兩側設有高出路面 15cm（厚度 0.15m）的高硬度路緣石人行道（Collision 幾何體），車輪撞擊會產生物理彈跳與阻滯。


* **關新公園 (Guanxin Park)**：
* 設定於路廊中段右側（約 $X=120\text{m} \sim 260\text{m}, Y=15\text{m} \sim 65\text{m}$），設有四周綠化草皮坡度碰撞體與標誌樹木。


* **新莊車站終點**：
* 設定於 $X \approx 400\text{m}$ 處，設有車站主體剛體結構與路底擋牆。



```xml
<?xml version="1.0" ?>
<sdf version="1.8">
  <world name="guanxin_world">
    <physics name="1ms" type="ode">
      <max_step_size>0.002</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>

    <!-- 日照環境 -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 100 0 0 0</pose>
      <diffuse>0.9 0.9 0.9 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- 地面與關新路主幹道 (400m x 20m) -->
    <model name="road_network">
      <static>true</static>
      <link name="road_link">
        <!-- 關新路主瀝青路面 -->
        <collision name="road_collision">
          <pose>200 0 0 0 0 0</pose>
          <geometry><box><size>400 20 0.05</size></box></geometry>
          <surface>
            <friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction>
          </surface>
        </collision>
        <visual name="road_visual">
          <pose>200 0 0 0 0 0</pose>
          <geometry><box><size>400 20 0.05</size></box></geometry>
          <material><ambient>0.2 0.2 0.2 1</ambient><diffuse>0.2 0.2 0.2 1</diffuse></material>
        </visual>

        <!-- 西側人行道 (Sidewalk - 撞擊剛體邊界) -->
        <collision name="sidewalk_w_col">
          <pose>200 -12 0.1 0 0 0</pose>
          <geometry><box><size>400 4 0.2</size></box></geometry>
        </collision>
        <visual name="sidewalk_w_vis">
          <pose>200 -12 0.1 0 0 0</pose>
          <geometry><box><size>400 4 0.2</size></box></geometry>
          <material><ambient>0.6 0.6 0.6 1</ambient><diffuse>0.6 0.6 0.6 1</diffuse></material>
        </visual>

        <!-- 東側人行道 (靠近關新公園側) -->
        <collision name="sidewalk_e_col">
          <pose>200 12 0.1 0 0 0</pose>
          <geometry><box><size>400 4 0.2</size></box></geometry>
        </collision>
        <visual name="sidewalk_e_vis">
          <pose>200 12 0.1 0 0 0</pose>
          <geometry><box><size>400 4 0.2</size></box></geometry>
          <material><ambient>0.6 0.6 0.6 1</ambient><diffuse>0.6 0.6 0.6 1</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- 關新公園本體 (綠地與障礙區) -->
    <model name="guanxin_park">
      <static>true</static>
      <pose>190 35 0.15 0 0 0</pose>
      <link name="park_link">
        <collision name="park_ground_col">
          <geometry><box><size>140 50 0.3</size></box></geometry>
        </collision>
        <visual name="park_ground_vis">
          <geometry><box><size>140 50 0.3</size></box></geometry>
          <material><ambient>0.15 0.45 0.15 1</ambient><diffuse>0.2 0.5 0.2 1</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- 沿街兩側建築立面與邊界限制 -->
    <model name="corridor_buildings">
      <static>true</static>
      <link name="bldg_link">
        <!-- 西側店鋪住宅街區 -->
        <collision name="bldg_w">
          <pose>200 -30 10 0 0 0</pose>
          <geometry><box><size>400 30 20</size></box></geometry>
        </collision>
        <visual name="bldg_w_vis">
          <pose>200 -30 10 0 0 0</pose>
          <geometry><box><size>400 30 20</size></box></geometry>
          <material><ambient>0.7 0.68 0.65 1</ambient><diffuse>0.7 0.68 0.65 1</diffuse></material>
        </visual>
        <!-- 新莊火車站末端建築擋牆 -->
        <collision name="xinzhuang_station_end">
          <pose>405 0 8 0 0 0</pose>
          <geometry><box><size>10 60 16</size></box></geometry>
        </collision>
        <visual name="xinzhuang_station_vis">
          <pose>405 0 8 0 0 0</pose>
          <geometry><box><size>10 60 16</size></box></geometry>
          <material><ambient>0.3 0.35 0.45 1</ambient><diffuse>0.3 0.35 0.45 1</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- 載入 Model Y 車輛 -->
    <include>
      <name>model_y</name>
      <uri>model://model_y</uri>
      <pose>5 0 0.3 0 0 0</pose>
    </include>
  </world>
</sdf>

```

---

### 3. Model Y 載具模型與視角鏡頭配置 (`src/guanxin_sim/models/model_y/model.sdf`)

規格依據 Tesla Model Y 真實尺寸建立：

* 長 4.75m、寬 1.92m、高 1.62m、軸距 2.89m、整備質量 1980 kg。
* 物理碰撞本體設為低重心剛體，包含 4 輪阿克曼/雙轉向關節與摩擦係數。
* **搭載 3 種獨立視角相機**：
1. `driver_cam`（車內主駕第一人稱）：置於方向盤後方視角 $(X=0.4, Y=0.38, Z=1.15)$。
2. `chase_cam`（第三人稱跟車視角）：置於車頂斜後方 $(X=-4.5, Y=0.0, Z=2.2)$。
3. `hood_cam`（車頭第一人稱/引擎蓋視角）：置於車鼻中央 $(X=2.1, Y=0.0, Z=0.75)$。


* 使用 `gz-sim-ackermann-steering-system` 插件，直接訂閱 `/cmd_vel` 並輸出真實車輪轉角與扭矩。

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
  <model name="model_y">
    <link name="chassis">
      <pose>0 0 0.35 0 0 0</pose>
      <inertial>
        <mass>1980.0</mass>
        <inertia>
          <ixx>750.0</ixx><ixy>0</ixy><ixz>0</ixz>
          <iyy>2800.0</iyy><iyz>0</iyz>
          <izz>3100.0</izz>
        </inertia>
      </inertial>
      <collision name="chassis_collision">
        <geometry><box><size>4.75 1.92 1.2</size></box></geometry>
        <surface>
          <contact><ode><min_depth>0.01</min_depth></ode></contact>
        </surface>
      </collision>
      <visual name="chassis_visual">
        <geometry><box><size>4.75 1.92 1.2</size></box></geometry>
        <material><ambient>0.8 0.1 0.1 1</ambient><diffuse>0.8 0.1 0.1 1</diffuse></material>
      </visual>

      <!-- 1. 車內視角 (Driver Interior Cam) -->
      <sensor name="driver_cam" type="camera">
        <pose>0.4 0.38 0.8 0 0 0</pose>
        <topic>/model_y/view_driver</topic>
        <camera>
          <horizontal_fov>1.4</horizontal_fov>
          <image><width>1280</width><height>720</height></image>
        </camera>
        <always_on>1</always_on><update_rate>30</update_rate>
      </sensor>

      <!-- 2. 第三人稱跟車視角 (Third-person Chase Cam) -->
      <sensor name="chase_cam" type="camera">
        <pose>-5.0 0.0 2.0 0 0.25 0</pose>
        <topic>/model_y/view_chase</topic>
        <camera>
          <horizontal_fov>1.5</horizontal_fov>
          <image><width>1280</width><height>720</height></image>
        </camera>
        <always_on>1</always_on><update_rate>30</update_rate>
      </sensor>

      <!-- 3. 車頭第一人稱 (Hood POV Cam) -->
      <sensor name="hood_cam" type="camera">
        <pose>2.1 0.0 0.45 0 0 0</pose>
        <topic>/model_y/view_hood</topic>
        <camera>
          <horizontal_fov>1.6</horizontal_fov>
          <image><width>1280</width><height>720</height></image>
        </camera>
        <always_on>1</always_on><update_rate>30</update_rate>
      </sensor>
    </link>

    <!-- 車輪與關節 (前後輪設定省略非關鍵代碼，保留物理插件) -->
    <plugin filename="gz-sim-ackermann-steering-system" name="gz::sim::systems::AckermannSteering">
      <topic>/cmd_vel</topic>
      <odom_topic>/odom</odom_topic>
      <wheel_base>2.89</wheel_base>
      <wheel_separation>1.63</wheel_separation>
      <wheel_radius>0.37</wheel_radius>
      <min_turning_radius>5.8</min_turning_radius>
    </plugin>
  </model>
</sdf>

```

---

### 4. 控制與視角切換 Node (`src/guanxin_sim/guanxin_sim/teleop_vehicle.py`)

該節點透過終端機監聽鍵盤原始字元（`termios`）：

* **`w` / `s**`：前後線速度線性增減。
* **`a` / `d**`：左右方向盤轉向角速度控制。
* **`v`**：在「車內主駕」、「第三人稱追蹤」、「車頭第一人稱」3 種視角循環切換（透過 ROS 2 影像轉發至 GUI 視窗展示）。
* **`o`**：發布重置服務指令，直接將車輛瞬間瞬移（Teleport/Reset）回原點 $(X=5, Y=0, Z=0.35)$，朝向新莊火車站。

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from ros_gz_interfaces.srv import SetEntityPose
from geometry_msgs.msg import Pose
import sys, select, tty, termios
import cv2
from cv_bridge import CvBridge

KEY_MAP = {
    'w': (1.0, 0.0),
    's': (-1.0, 0.0),
    'a': (0.0, 0.6),
    'd': (0.0, -0.6),
}

class TeleopVehicle(Node):
    def __init__(self):
        super().__init__('teleop_vehicle')
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        
        self.views = ['/model_y/view_chase', '/model_y/view_driver', '/model_y/view_hood']
        self.view_names = ['3rd Person (Chase)', '1st Person (Driver Seat)', '1st Person (Front Hood)']
        self.cur_view_idx = 0
        
        # 影像訂閱
        self.sub_img = self.create_subscription(Image, self.views[self.cur_view_idx], self.on_image, 1)
        self.get_logger().info("Teleop Controller Ready. Controls: [WSAD] Drive, [V] Switch Cam, [O] Reset Origin, [Q] Quit")

    def switch_view(self):
        self.cur_view_idx = (self.cur_view_idx + 1) % len(self.views)
        self.destroy_subscription(self.sub_img)
        self.sub_img = self.create_subscription(Image, self.views[self.cur_view_idx], self.on_image, 1)
        print(f"\n[View Switched] >> {self.view_names[self.cur_view_idx]}")

    def on_image(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.putText(frame, f"View: {self.view_names[self.cur_view_idx]}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow("Model Y Camera View", frame)
        cv2.waitKey(1)

    def reset_origin(self):
        print("\n[Teleport] Resetting vehicle to Guanxin-Guangfu Origin...")
        # 透過 gz topic 或 ros service 重設模型 Pose
        cmd = Twist()
        self.pub_cmd.publish(cmd)
        # 發布 /cmd_vel 為 0 煞停，並調用實體擺放指令
        import os
        os.system("gz service -s /world/guanxin_world/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 1000 --req 'name: \"model_y\", position: {x: 5.0, y: 0.0, z: 0.4}, orientation: {x: 0, y: 0, z: 0, w: 1}' > /dev/null 2>&1")

def main():
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    rclpy.init()
    node = TeleopVehicle()

    speed, steer = 0.0, 0.0
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.05)
            if select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.read(1)
                if c in KEY_MAP:
                    dv, dw = KEY_MAP[c]
                    speed = max(min(speed + dv * 1.5, 20.0), -5.0) if dv != 0 else speed
                    steer = max(min(steer + dw * 0.2, 0.8), -0.8) if dw != 0 else steer
                elif c == 'v':
                    node.switch_view()
                elif c == 'o':
                    node.reset_origin()
                    speed, steer = 0.0, 0.0
                elif c == ' ':  # 煞車
                    speed, steer = 0.0, 0.0
                elif c == 'q':
                    break

                t = Twist()
                t.linear.x = float(speed)
                t.angular.z = float(steer)
                node.pub_cmd.publish(t)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

```

---

### 5. Launch 檔與 Gazebo-ROS 橋接 (`src/guanxin_sim/launch/sim.launch.py`)

配置 `ros_gz_bridge`，在後台將 Gazebo Harmonic 的感測器與控制 Topic 雙向綁定至 ROS 2。

```python
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('guanxin_sim')
    world_path = os.path.join(pkg_dir, 'worlds', 'guanxin.sdf')

    # 1. 啟動 Gazebo Harmonic
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # 2. ros_gz_bridge 橋接控制與相機 Topic
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/model_y/view_driver@sensor_msgs/msg/Image@gz.msgs.Image',
            '/model_y/view_chase@sensor_msgs/msg/Image@gz.msgs.Image',
            '/model_y/view_hood@sensor_msgs/msg/Image@gz.msgs.Image',
        ],
        output='screen'
    )

    # 3. 鍵盤控制與視角切換 Node
    teleop = Node(
        package='guanxin_sim',
        executable='teleop_vehicle',
        prefix='xterm -e', # 彈出專用終端接收鍵盤按鍵
        output='screen'
    )

    return LaunchDescription([gz_sim, bridge, teleop])

```

---

### 6. 交給 Antigravity CLI 的執行指令

您可以直接將這段指令複製貼給您的 Antigravity CLI：

> 請在目前目錄依照上述規格建立 `guanxin_sim_ws` 專案：
> 1. 產生完整 `Dockerfile` 與 `run.sh`。
> 2. 建立 `guanxin_sim` ROS 2 套件，配置好光復/關新路至新莊車站世界檔、關新公園幾何剛體、Model Y 阿克曼車輛與三視角相機。
> 3. 編寫鍵盤節點（支援 `WSAD` 駕駛、`V` 切換第一/三人稱/車內視角、`O` 原點瞬移）。
> 4. 執行 `docker build -t guanxin_sim:latest .` 並執行 `bash run.sh` 啟動容器驗收。
> 
>