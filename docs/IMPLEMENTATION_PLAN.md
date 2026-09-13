# 新竹關新路仿真實作計畫 (Hsinchu Guanxin Road Simulation Implementation Plan)

> **專案目標**：使用 Docker 容器化環境（Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic），建構新竹市東區關新路（光復路口至新莊車站，含關新公園）之 3D 物理街區，並建立具備真實阿克曼轉向之 Tesla Model Y 車輛模型、三重視角切換（車內、第三人稱、車頭）與鍵盤控制節點（WSAD / V / O）。

---

## 1. 需求分析與規格對照表

| 需求項目 | 規格內容與技術選型 | 關鍵實作細節 |
| :--- | :--- | :--- |
| **容器化環境** | Ubuntu 24.04 (Noble) + ROS 2 Jazzy | Dockerfile 支援 NVIDIA GPU 與 Mesa 軟體渲染；X11 GUI 轉發 |
| **物理模擬器** | Gazebo Harmonic (Gz Sim 8) + `ros_gz` | ODE 物理引擎（步長 0.002s / 500Hz），高真實度碰撞接觸表面 |
| **世界與地圖** | 關新路廊道（光復路口至新莊車站，長 400m，寬 120m） | 瀝青路面（$\mu=0.9$）、15cm 凸起人行道路緣石（剛體碰撞體）、關新公園本體（綠地地形與邊界）、兩側店面建築與新莊車站擋牆 |
| **載具模型** | Tesla Model Y 尺寸與重量真實模擬 | 長 4.75m、寬 1.92m、高 1.62m、整備質量 1980kg；具備完整的 4 輪與轉向關節結構，搭載 `gz-sim-ackermann-steering-system` |
| **感測與視角** | 3 種相機視角 + OpenCV 即時 HUD | 1. 車內主駕視角 (`driver_cam`)<br>2. 第三人稱跟車視角 (`chase_cam`)<br>3. 車頭第一人稱視角 (`hood_cam`) |
| **控制節點** | ROS 2 Python 節點 (`teleop_vehicle`) | - `W/S`：前進/後退速度線性控制<br>- `A/D`：方向盤轉向角速度控制<br>- `V`：循環切換相機影像視角<br>- `O`：瞬移重置車輛至原點並清除速度<br>- `Space`：緊急煞車<br>- `Q`：退出節點 |
| **啟動流程** | 一鍵腳本與 ROS 2 Launch | `run.sh`（自動偵測 GPU 與 X11 設定）-> `sim.launch.py`（啟動 Gazebo、ros_gz_bridge、teleop 終端） |

---

## 2. 專案目錄架構規劃

整個工作區目錄配置如下：

```text
gz_my_world/
├── Dockerfile                  # Docker 映像檔定義 (Jazzy + Harmonic + GUI 相依項)
├── docker-compose.yml          # Docker Compose 便捷設定 (選配)
├── run.sh                      # 一鍵檢查 GPU、X11 權限並啟動容器的腳本
├── requirement.md              # 原始需求規格書
├── IMPLEMENTATION_PLAN.md      # 本實作計畫書
└── src/
    └── guanxin_sim/            # ROS 2 核心套件 (ament_cmake)
        ├── CMakeLists.txt      # 建置腳本 (安裝 launch, worlds, models, python 節點)
        ├── package.xml         # 套件資訊與 ROS 2 相依宣告
        ├── launch/
        │   └── sim.launch.py   # 主啟動檔 (Gazebo + ros_gz_bridge + Teleop)
        ├── worlds/
        │   └── guanxin.sdf     # 關新路世界檔 (路網、公園、建築、邊界剛體、光照)
        ├── models/
        │   └── model_y/
        │       ├── model.config # Gazebo 模型描述檔
        │       └── model.sdf    # Model Y 完整物理模型 (底盤、轉向軸、4輪、3相機、阿克曼插件)
        └── guanxin_sim/
            ├── __init__.py
            └── teleop_vehicle.py # 鍵盤控制、相機切換與原點重置節點
```

---

## 3. 實作階段規劃 (Phase Breakdown)

### Phase 0: 容器化與環境基底構建
* **目標**：確保容器內外圖形轉發無誤、ROS 2 與 Gazebo 依賴完整無缺失。
* **預防性修復與細節補強**：
  1. 檢視 `requirement.md` 的 Dockerfile，補齊漏列的相依套件：
     - `xterm`（launch 檔中 `prefix='xterm -e'` 所需）
     - `python3-opencv` / `ros-jazzy-cv-bridge`（影像顯示與轉換所需）
     - `ros-jazzy-image-transport` 與 `libegl1-mesa`
  2. 設定環境變數 `GZ_SIM_RESOURCE_PATH=/ros2_ws/install/guanxin_sim/share/guanxin_sim/models`，防止 Gazebo 找不到 `model://model_y`。
  3. `run.sh` 增加對 Wayland / X11 DISPLAY 自動辨識與 `xhost +local:root` 安全處理。

### Phase 1: ROS 2 套件骨架與建置配置 (`guanxin_sim`)
* **目標**：建立標準 ROS 2 套件結構，配置 CMakeLists.txt 與 package.xml。
* **主要工作**：
  1. 建立 `package.xml`：宣告 `ros_gz_bridge`, `ros_gz_sim`, `geometry_msgs`, `sensor_msgs`, `nav_msgs`, `cv_bridge` 等依賴。
  2. 撰寫 `CMakeLists.txt`：
     - 使用 `ament_cmake` 與 `ament_cmake_python`。
     - 正確安裝 `launch`, `worlds`, `models` 至 `share/guanxin_sim/`。
     - 安裝 `teleop_vehicle.py` 可執行檔至 `lib/guanxin_sim/`。

### Phase 2: 關新路高擬真空間世界檔 (`guanxin.sdf`)
* **目標**：建立座標系精確、具備嚴格物理碰撞反應的街區與公園環境。
* **主要工作**：
  1. **座標系確立**：
     - 原點 $(0, 0, 0)$：光復路一段與關新路交叉口中心。
     - 軸向：$+X$ 沿關新路朝向新莊車站（總長約 400m），$+Y$ 朝向關新公園方向（路寬左右各 50m，總寬約 120m），$+Z$ 垂直地面。
  2. **路面與人行道邊界 (Sidewalk Curb Collision)**：
     - 主幹道路面厚度 0.05m，瀝青摩擦係數設定 $\mu=0.9$。
     - 左右兩側人行道高出路面 15cm（厚度 0.2m，頂面 $Z=0.2$），設定堅硬碰撞剛體，若車輛轉向不慎衝撞路緣石，輪胎與懸吊將產生物理彈跳與阻滯。
  3. **關新公園 (Guanxin Park)**：
     - 位置配置於 $X \in [120, 260]\text{m}, Y \in [15, 65]\text{m}$。
     - 包含微地形草坡剛體、外環走道、代表性樹木幾何障礙物與公園邊界花台。
  4. **沿街商業建築與新莊車站終點**：
     - 西側商業住宅立面（$Y \approx -20\text{m} \sim -50\text{m}$）長條剛體群，防止車輛開出邊界。
     - 東側建築群（緊鄰關新公園前後）。
     - 新莊火車站末端建築擋牆（$X \approx 405\text{m}$），作為關新路底死胡同剛性邊界。
  5. **物理引擎與光影**：
     - 啟用 `gz-sim-physics-system`, `gz-sim-sensors-system`, `gz-sim-user-commands-system`, `gz-sim-scene-broadcaster-system`。
     - 太陽平行光投射陰影，環境光充足。

### Phase 3: Tesla Model Y 完整物理載具與相機組態 (`model.sdf`)
* **目標**：補全 `requirement.md` 中省略的四輪轉向結構，建立真正可開動、具物理剛性的 Model Y。
* **重大技術細節補全 (Crucial Implementation Detail)**：
  - `requirement.md` 提供的範例中僅有 chassis 與插件骨架，車輪與關節標註為省略。
  - **實做必須完整補齊**：
    1. **轉向關節與轉向節 (Steering Knuckles)**：
       - `fl_steering_link` & `fr_steering_link` 透過 `revolute` 關節（Z軸旋轉）連結至底盤，設定合理極限角（約 $\pm 0.6$ rad，約 35 度）。
    2. **四顆車輪與滾動軸 (Wheel Axles)**：
       - 前左右輪分別透過 `revolute` 關節（Y軸滾動）連結至轉向節。
       - 後左右輪直接透過 `revolute` 關節（Y軸滾動）連結至底盤。
       - 設定車輪半徑 0.37m、寬度 0.25m、適當質量與慣量。
       - 設定輪胎表面摩擦係數 $\mu=1.0$、接觸剛性（ode min_depth/kp/kd）。
    3. **阿克曼轉向外掛 (`gz-sim-ackermann-steering-system`) 完整參數綁定**：
       - `topic`: `/cmd_vel`
       - `odom_topic`: `/odom`
       - `left_joint`: 前左輪滾動關節
       - `right_joint`: 前右輪滾動關節
       - `left_steering_joint`: 前左轉向關節
       - `right_steering_joint`: 前右轉向關節
       - `wheel_base`: 2.89m
       - `wheel_separation`: 1.63m
       - `wheel_radius`: 0.37m
  4. **三機位感測器配置**：
     - `driver_cam`（車內駕駛座視角）：置於駕駛座頭枕前方 ($0.4, 0.38, 0.8$)，視角向正前方，可見車內擋風玻璃與前方街景。
     - `chase_cam`（第三人稱跟車視角）：置於車頂後上方 ($-5.0, 0.0, 2.2$)，俯角約 15 度指向車身與前方路面。
     - `hood_cam`（車頭保桿/第一人稱前視）：置於前鼻中央 ($2.1, 0.0, 0.45$)，廣角無遮擋前視。

### Phase 4: 車輛控制、相機切換與原點重置節點 (`teleop_vehicle.py`)
* **目標**：提供直覺的終端機鍵盤控制與即時相機 OpenCV 視窗。
* **主要工作**：
  1. **按鍵監聽**：
     - 使用 `termios` 與非阻塞 `select.select` 接收原始按鍵。
     - `W/S`：線性加速度遞增/遞減（速度範圍 $-5.0 \sim 20.0 \text{ m/s}$）。
     - `A/D`：方向盤轉角速度增減（角速度範圍 $-0.8 \sim 0.8 \text{ rad/s}$）。
     - `Space`：煞車，重置速度與轉向為 0。
  2. **視角切換 (`V`)**：
     - 循環切換訂閱 `/model_y/view_chase`、`/model_y/view_driver`、`/model_y/view_hood`。
     - 使用 OpenCV 視窗彈出影像，並在畫面左上角標註當前視角名稱與控制狀態 HUD。
     - `cv2.waitKey(1)` 確保畫面流暢更新（30fps）。
  3. **回到原點 (`O`)**：
     - 發布 `/cmd_vel` 歸零煞停。
     - 呼叫 Gazebo Harmonic 服務 `/world/guanxin_world/set_pose`，將 `model_y` 瞬移回起始點 $(X=5.0, Y=0.0, Z=0.35, \text{yaw}=0)$。
     - 清除車身動量與角動量，避免瞬移後繼續漂移。

### Phase 5: 啟動流程整合與 ROS-Gazebo 橋接 (`sim.launch.py` & `run.sh`)
* **目標**：達成一鍵啟動、雙向通訊、自動轉發。
* **主要工作**：
  1. **`sim.launch.py`**：
     - 動態解析套件路徑，設定 `GZ_SIM_RESOURCE_PATH`。
     - 啟動 `gz sim -r guanxin.sdf`。
     - 啟動 `ros_gz_bridge parameter_bridge`：
       - `/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist`
       - `/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry`
       - 三組相機影像：`/model_y/view_*@sensor_msgs/msg/Image@gz.msgs.Image`
     - 啟動 `teleop_vehicle` 節點（可在專用終端或同一終端中運行）。
  2. **`run.sh`**：
     - 自動偵測 `nvidia-smi` 並加上 `--gpus all`。
     - 掛載 X11 socket 與 display 環境變數。
     - 將工作目錄 `src` 掛載進容器，方便即時修改測試。

---

## 4. 驗收標準與測試流程 (Verification & Acceptance)

完成各階段程式碼後，將依序執行下列測試以確保完全符合 `requirement.md`：

| 測試編號 | 測試項目 | 預期成果 |
| :---: | :--- | :--- |
| **T1** | Docker 映像檔建置 | `docker build -t guanxin_sim:latest .` 成功，無缺漏套件，colcon build 零錯誤。 |
| **T2** | Gazebo 世界載入 | 執行 `bash run.sh` 後 Gazebo Harmonic GUI 順利啟動，成功渲染關新路 400m 路廊、人行道、綠色關新公園與新莊車站擋牆。 |
| **T3** | Model Y 實體就位 | Model Y 穩定停放於光復路關新路口起點 ($X=5, Y=0$)，四輪著地無塌陷或物理抖動。 |
| **T4** | 鍵盤驅動與物理碰撞 | 操作 `W/S/A/D` 車身能平滑加速、轉向與倒車；轉向衝上 15cm 人行道路緣或撞擊建築物時，產生明顯物理阻擋與車身彈跳反應。 |
| **T5** | 視角切換功能 | 按下 `V` 鍵，OpenCV 畫面即時切換「第三人稱跟車」、「駕駛座車內」、「車頭第一人稱」3 種視角，HUD 文字相應變更。 |
| **T6** | 原點瞬移重置 | 車輛行駛至任意位置後，按下 `O` 鍵，車輛立即瞬移回起點，車速即刻歸零，無殘留速度。 |

---

## 5. 潛在風險與因應策略

1. **GPU GUI 轉發權限**：
   - *風險*：非 root 權限或 NVIDIA Docker runtime 未配置可能導致 Gazebo 畫面無法顯示。
   - *因應*：在 `run.sh` 中加入 X11 權限檢查，並配置 Mesa 軟體渲染 fallback 選項（`LIBGL_ALWAYS_SOFTWARE=1`）。
2. **阿克曼轉向物理調校**：
   - *風險*：車輪質量過輕或轉向關節阻尼不足可能導致車輛高速轉向時翻覆或甩尾。
   - *因應*：依據真實 Model Y 規格設定低重心（電池底盤集中於 $Z=0.25$）、高慣量以及摩擦錐 parameters，確保操駕手感扎實穩定。
3. **相機畫面更新延遲**：
   - *風險*：高解析度 (1280x720) 3 鏡頭同時發布可能消耗過多 CPU/GPU 資源。
   - *因應*：相機 update_rate 設定為 30Hz，並於 teleop 節點中僅對當前切換的視角進行動態訂閱（動態 create/destroy subscription），節省傳輸頻寬與 CPU 負載。

---

## 6. 開工前確認事項

請檢閱本實做計畫。確認無誤後，我們將立即依照此步驟依序產出完整檔案：
1. `Dockerfile` & `run.sh`
2. `src/guanxin_sim/package.xml` & `CMakeLists.txt`
3. `src/guanxin_sim/worlds/guanxin.sdf`
4. `src/guanxin_sim/models/model_y/model.sdf` (含完整車輪與轉向機構)
5. `src/guanxin_sim/guanxin_sim/teleop_vehicle.py`
6. `src/guanxin_sim/launch/sim.launch.py`
7. 進行建置驗證與測試引導。
