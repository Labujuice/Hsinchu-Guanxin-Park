import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('guanxin_sim')
    world_path = os.path.join(pkg_dir, 'worlds', 'guanxin.sdf')
    models_path = os.path.join(pkg_dir, 'models')

    # 設定 Gazebo 資源路徑以正確解析 model://model_y
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

    # 宣告啟動參數：是否使用 xterm 獨立彈出鍵盤終端
    use_xterm_arg = DeclareLaunchArgument(
        'use_xterm',
        default_value='true',
        description='Whether to open teleop node in a dedicated xterm window'
    )
    use_xterm = LaunchConfiguration('use_xterm')

    # 1. 啟動 Gazebo Harmonic (gz sim)
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

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

    # 3. 鍵盤控制與視角切換節點 (使用 xterm 彈出專用終端)
    teleop_xterm = Node(
        package='guanxin_sim',
        executable='teleop_vehicle',
        prefix='xterm -geometry 95x25 -title "Tesla Model Y Teleop Controller [WSAD/V/O]" -e',
        output='screen',
        condition=IfCondition(use_xterm)
    )

    # 4. 鍵盤控制與視角切換節點 (無 xterm 備用模式)
    teleop_direct = Node(
        package='guanxin_sim',
        executable='teleop_vehicle',
        output='screen',
        condition=UnlessCondition(use_xterm)
    )

    return LaunchDescription([
        set_gz_resource_path,
        set_sdf_path,
        set_gz_file_path,
        use_xterm_arg,
        gz_sim,
        bridge,
        teleop_xterm,
        teleop_direct
    ])
