import os
import re
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def launch_setup(context, *args, **kwargs):
    pkg_dir = get_package_share_directory('guanxin_sim')
    world_path = os.path.join(pkg_dir, 'worlds', 'guanxin.sdf')

    enable_vehicle_str = LaunchConfiguration('enable_vehicle').perform(context).strip().lower()
    enable_vehicle = enable_vehicle_str in ['true', '1', 'yes', 'on']

    use_xterm_str = LaunchConfiguration('use_xterm').perform(context).strip().lower()
    use_xterm = use_xterm_str in ['true', '1', 'yes', 'on']

    actions = []

    if enable_vehicle:
        world_file_to_load = world_path

        # 1. 啟動 Gazebo Harmonic (gz sim)
        gz_sim = ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_file_to_load],
            output='screen'
        )
        actions.append(gz_sim)

        # 2. ros_gz_bridge 橋接控制、里程計與三組相機 Topics
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
        actions.append(bridge)

        # 3. 鍵盤控制與視角切換節點 (使用 xterm 彈出專用終端或直接輸出)
        if use_xterm:
            teleop_node = Node(
                package='guanxin_sim',
                executable='teleop_vehicle',
                prefix='xterm -geometry 95x25 -title "Tesla Model Y Teleop Controller [WSAD/V/O]" -e',
                output='screen'
            )
        else:
            teleop_node = Node(
                package='guanxin_sim',
                executable='teleop_vehicle',
                output='screen'
            )
        actions.append(teleop_node)
    else:
        # 地圖純檢視/編輯模式：動態去除 Model Y 載具模型，純載入地圖世界
        with open(world_path, 'r', encoding='utf-8') as f:
            sdf_content = f.read()

        # 移除包含 model_y 的 <include> 標籤區塊
        pattern = r'(\s*<!--[^\n]*-->)?\s*<include>\s*<name>model_y</name>.*?</include>'
        map_only_sdf = re.sub(pattern, '', sdf_content, flags=re.DOTALL)

        temp_world_path = '/tmp/guanxin_map_only.sdf'
        with open(temp_world_path, 'w', encoding='utf-8') as f:
            f.write(map_only_sdf)

        print("=" * 60)
        print("[sim.launch.py] 啟動【地圖純檢視/編輯模式】")
        print("[sim.launch.py] 已停用汽車模組：未生成 Model Y、未啟動相機橋接與操控視窗")
        print("=" * 60)

        gz_sim = ExecuteProcess(
            cmd=['gz', 'sim', '-r', temp_world_path],
            output='screen'
        )
        actions.append(gz_sim)

    return actions

def generate_launch_description():
    pkg_dir = get_package_share_directory('guanxin_sim')
    models_path = os.path.join(pkg_dir, 'models')

    # 設定 Gazebo 資源路徑以正確解析 model://
    existing_resource_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    combined_resource_path = f"{models_path}:{existing_resource_path}" if existing_resource_path else models_path

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=combined_resource_path
    )
    set_sdf_path = SetEnvironmentVariable(
        name='SDF_PATH',
        value=combined_resource_path
    )
    set_gz_file_path = SetEnvironmentVariable(
        name='GZ_FILE_PATH',
        value=combined_resource_path
    )

    # 宣告啟動參數：是否啟用汽車模組 (預設開啟)
    enable_vehicle_arg = DeclareLaunchArgument(
        'enable_vehicle',
        default_value='true',
        description='Whether to enable the vehicle module (Model Y, camera bridges, teleop controller)'
    )

    # 宣告啟動參數：是否使用 xterm 獨立彈出鍵盤終端
    use_xterm_arg = DeclareLaunchArgument(
        'use_xterm',
        default_value='true',
        description='Whether to open teleop node in a dedicated xterm window'
    )

    return LaunchDescription([
        set_gz_resource_path,
        set_sdf_path,
        set_gz_file_path,
        enable_vehicle_arg,
        use_xterm_arg,
        OpaqueFunction(function=launch_setup)
    ])
