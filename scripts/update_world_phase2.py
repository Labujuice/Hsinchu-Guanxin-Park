#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Guanxin World SDF with Phase 2 Road Network, Expanded Ground Plane, and Smart Parking Poles.
Author: Autonomous Robotics & Simulation Team
"""

import os
import re
from generate_phase2_road_network import generate_road_network_sdf, ROAD_YAW

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

def main():
    with open(WORLD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. New Ground Plane (1400m x 1400m centered at E=-100, N=480 to cover entire 58 ha + buffer)
    ground_plane_xml = '''    <!-- ==================== 地面大底 (Ground Plane 1400m x 1400m 覆蓋全域 58 公頃) ==================== -->
    <model name="ground_plane">
      <static>true</static>
      <pose>-100 480 0 0 0 0</pose>
      <link name="ground_link">
        <collision name="ground_col">
          <geometry><plane><normal>0 0 1</normal><size>1400 1400</size></plane></geometry>
          <surface>
            <friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction>
            <contact><ode><kd>100000</kd><kp>10000000</kp></ode></contact>
          </surface>
        </collision>
        <visual name="ground_vis">
          <geometry><plane><normal>0 0 1</normal><size>1400 1400</size></plane></geometry>
          <material><ambient>0.42 0.44 0.42 1</ambient><diffuse>0.48 0.50 0.48 1</diffuse></material>
        </visual>
      </link>
    </model>'''

    # 2. Road Network and Smart Parking SDF Block
    road_network_xml = generate_road_network_sdf()

    # 3. Locate slice to replace: from <!-- ==================== 地面大底 up to right before <!-- ==================== 寶雅與關新一街之間中介建築群
    start_mark = '<!-- ==================== 地面大底'
    end_mark = '<!-- ==================== 寶雅與關新一街之間中介建築群'

    start_pos = content.find(start_mark)
    end_pos = content.find(end_mark)

    if start_pos == -1 or end_pos == -1:
        print(f"Error: Could not locate markers in {WORLD_PATH}!")
        print(f"start_pos: {start_pos}, end_pos: {end_pos}")
        return False

    new_section = ground_plane_xml + "\n\n" + road_network_xml + "\n\n"
    updated_content = content[:start_pos] + new_section + content[end_pos:]

    # 4. Calibrate Model Y vehicle spawn pose to Northbound lane on Guanxin Road heading towards station
    # Coordinates: E = +6.63, N = +8.74, U = 0.38, yaw = ROAD_YAW (1.34512 rad / 77.07 deg)
    old_pose_re = r'(<include>\s*<name>model_y</name>.*?<pose>)(.*?)(</pose>)'
    new_pose_str = f'6.63 8.74 0.38 0 0 {ROAD_YAW:.5f}'
    updated_content = re.sub(
        old_pose_re,
        rf'\g<1>{new_pose_str}\g<3>',
        updated_content,
        flags=re.DOTALL
    )

    with open(WORLD_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Successfully updated {WORLD_PATH} with Phase 2 assets!")
    return True

if __name__ == '__main__':
    main()
