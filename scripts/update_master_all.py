#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Transformation Script for Guanxin World SDF:
  1. Accurate Guanxin East Road (4 realistic multi-segment geometry with curve towards Xinzhuang Station).
  2. Nordic Three Nations Community (rotated 90 deg, central park, dual roads aligned with Guanxin 1st St, outer duplicates, corner of Guangfu Rd & Guanxin Rd).
  3. Moon Shadow International Building (月影國際會館 18F).
  4. Orange Hour Cafe (橘時咖啡 2F, at corner of Guanxin Rd and Guanxin 2nd St).
  5. Relocate POYA, McDonald's, Starbucks, Cathay Bank, Cosmed to their true East-side poses with photorealistic facades.
  6. Transform commercial amenities (carts, gantry, ramp, pink flowering tree, Starbucks umbrellas/patio, scooters, trees, signal poles).
Author: Autonomous Robotics & Simulation Team
"""

import math
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

# Coordinate Constants
BEARING_DEG = 12.930438
BEARING_RAD = math.radians(BEARING_DEG)
ROAD_YAW = math.radians(90.0 - BEARING_DEG)   # 1.345116 rad = 77.0696 deg
CROSS_YAW = ROAD_YAW - math.radians(90.0)     # -0.225678 rad = -12.9304 deg
WEST_BLDG_YAW = CROSS_YAW - math.radians(90.0) # -1.796474 rad = -102.9304 deg

U_ROAD = (math.sin(BEARING_RAD), math.cos(BEARING_RAD))
U_PERP = (math.cos(BEARING_RAD), -math.sin(BEARING_RAD))

def pt_road(s, perp):
    return s * U_ROAD[0] + perp * U_PERP[0], s * U_ROAD[1] + perp * U_PERP[1]

def transform_old_pose(match):
    x_str, y_str, z_str, r_str, p_str, yaw_str = match.groups()
    x = float(x_str)
    y = float(y_str)
    z = float(z_str)
    r = float(r_str)
    p = float(p_str)
    yaw = float(yaw_str)

    s = x
    perp = -y  # In old coords, negative y was East
    e, n = pt_road(s, perp)
    new_yaw = yaw + ROAD_YAW
    while new_yaw > math.pi:
        new_yaw -= 2.0 * math.pi
    while new_yaw <= -math.pi:
        new_yaw += 2.0 * math.pi

    return f'<pose>{e:.3f} {n:.3f} {z:.3f} {r:.3f} {p:.3f} {new_yaw:.5f}</pose>'

def build_accurate_road_network_sdf():
    lines = []
    lines.append('    <!-- ==================== Phase 2: 全域路網精確鋪設與路邊智慧停車柱系統 ==================== -->')
    lines.append('    <!-- 涵蓋 58 公頃: 關新路(18m)、真實多段彎道關新東路(14m)、光復路(24m)、關新一街(12m)、關新二街(14m)、關新北路(14m)、社區聯絡道 -->')
    lines.append('    <model name="road_network">')
    lines.append('      <static>true</static>')
    lines.append('      <link name="road_link">')

    # 1a. 關新路主幹道直道段 (長 488m, 寬 18m, 雙向四線道)
    gx_len = 488.0
    gx_mid_e, gx_mid_n = pt_road(gx_len / 2.0, 0.0)
    lines.append(f'        <!-- 1a. 關新路主幹道直道段柏油路面 (長 {gx_len}m, 寬 18m, 雙向四線道, 方位角 {BEARING_DEG:.2f}°) -->')
    lines.append(f'        <collision name="gx_road_str_col"><pose>{gx_mid_e:.3f} {gx_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gx_len} 18.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx_road_str_vis"><pose>{gx_mid_e:.3f} {gx_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gx_len} 18.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')

    # 1b. 關新路北側向東轉彎彎道 (5段順滑彎道, 依真實GIS路網曲線鋪設, 連通新莊車站迎賓廣場與關東路)
    lines.append('\n        <!-- 1b. 關新路北側向東轉彎彎道 (依真實GIS與地圖曲線鋪設, 連通新莊車站前與關東路) -->')
    gx_curves = [
        ("gx_curve1", 488.0, 0.0, 540.0, 20.0, "關新路北彎道段1: 日光公園北端起始微彎"),
        ("gx_curve2", 540.0, 20.0, 600.0, 65.0, "關新路北彎道段2: 日光公園東北轉折段"),
        ("gx_curve3", 600.0, 65.0, 650.0, 130.0, "關新路北彎道段3: 朝新莊車站方向偏東"),
        ("gx_curve4", 650.0, 130.0, 685.0, 190.0, "關新路北彎道段4: 新莊車站迎賓廣場前直通段"),
        ("gx_curve5", 685.0, 190.0, 725.0, 245.0, "關新路北彎道段5: 車站前延伸通過鐵路高架下方銜接關東路"),
    ]
    for name, s1, p1, s2, p2, desc in gx_curves:
        e1, n1 = pt_road(s1, p1)
        e2, n2 = pt_road(s2, p2)
        de, dn = e2 - e1, n2 - n1
        l = math.hypot(de, dn)
        yaw = math.atan2(dn, de)
        me, mn = (e1 + e2) / 2.0, (n1 + n2) / 2.0
        lines.append(f'        <!-- 關新路彎道: {desc} (長 {l:.1f}m, 寬 18m) -->')
        lines.append(f'        <collision name="{name}_col"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} 18.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
        lines.append(f'        <visual name="{name}_vis"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} 18.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_line"><pose>{me:.3f} {mn:.3f} 0.022 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # 2. 正確的關新東路 (Guanxin East Road - Multi-segment realistic GIS curve)
    lines.append('\n        <!-- ===== 2. 正確的關新東路多段彎道主幹道 (Guanxin East Road: 依真實GIS與OSM曲線鋪設) ===== -->')
    gxe_segs = [
        ("gxe_seg1_south", 0.0, 175.7, 88.0, 140.0, "南段: 光復路至關新一街, 順正北走向"),
        ("gxe_seg2_school", 88.0, 140.0, 344.5, 118.0, "中南段: 關埔國小西側, 關新一街至關新二街"),
        ("gxe_seg3_park", 344.5, 118.0, 488.0, 118.0, "中北段: 日光公園東側直道, 關新二街至關新北路, 寬14m"),
        ("gxe_seg4a_north", 488.0, 118.0, 580.0, 145.0, "北段彎道1: 日光公園東北轉角微彎"),
        ("gxe_seg4b_north", 580.0, 145.0, 680.0, 190.0, "北段彎道2: 新莊車站東側聯絡段"),
        ("gxe_seg4c_north", 680.0, 190.0, 780.0, 250.0, "北段彎道3: 往東北接埔頂路口")
    ]
    for name, s1, p1, s2, p2, desc in gxe_segs:
        e1, n1 = pt_road(s1, p1)
        e2, n2 = pt_road(s2, p2)
        de, dn = e2 - e1, n2 - n1
        length = math.hypot(de, dn)
        yaw = math.atan2(dn, de)
        mid_e, mid_n = (e1 + e2) / 2.0, (n1 + n2) / 2.0
        lines.append(f'        <!-- 關新東路: {desc} (長 {length:.1f}m, 寬 14m) -->')
        lines.append(f'        <collision name="{name}_col"><pose>{mid_e:.3f} {mid_n:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{length:.2f} 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
        lines.append(f'        <visual name="{name}_vis"><pose>{mid_e:.3f} {mid_n:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{length:.2f} 14.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_line"><pose>{mid_e:.3f} {mid_n:.3f} 0.022 0 0 {yaw:.5f}</pose><geometry><box><size>{length:.2f} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # 3. 光復路一段 (450m, width 24m, 雙向六線道) - 角度精準對齊北歐三小國南棟 (CROSS_YAW = -12.9304°)
    gf_len = 450.0
    gf_mid_e, gf_mid_n = pt_road(0.0, 25.0)
    lines.append('\n        <!-- 3. 光復路一段主幹道 (南界門戶橫向幹道, 長 450m, 寬 24m, 雙向六線道, 角度精準對齊北歐三小國南棟與關新一街) -->')
    lines.append(f'        <collision name="guangfu_road_col"><pose>{gf_mid_e:.3f} {gf_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>{gf_len} 24.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="guangfu_road_vis"><pose>{gf_mid_e:.3f} {gf_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>{gf_len} 24.0 0.02</size></box></geometry><material><ambient>0.20 0.20 0.21 1</ambient><diffuse>0.22 0.22 0.23 1</diffuse></material></visual>')

    # 4. 關新一街 (Guanxin 1st Street: at s = 88m, width = 12m)
    gx1_e_mid_e, gx1_e_mid_n = pt_road(88.0, 74.5)
    lines.append('\n        <!-- 4. 關新一街東段 (自關新路連通至關新東路, 長 131m, 寬 12m) -->')
    lines.append(f'        <collision name="gx1_east_col"><pose>{gx1_e_mid_e:.3f} {gx1_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>131.0 12.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx1_east_vis"><pose>{gx1_e_mid_e:.3f} {gx1_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>131.0 12.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    gx1_w_mid_e, gx1_w_mid_n = pt_road(88.0, -40.0)
    lines.append('        <!-- 關新一街西段 (自關新路延伸至北歐三小國社區南側開放道路, 長 60m, 寬 12m) -->')
    lines.append(f'        <collision name="gx1_west_col"><pose>{gx1_w_mid_e:.3f} {gx1_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>60.0 12.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx1_west_vis"><pose>{gx1_w_mid_e:.3f} {gx1_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>60.0 12.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 5. 關新二街 (Guanxin 2nd Street: at s = 344.5m, width = 14m)
    gx2_e_mid_e, gx2_e_mid_n = pt_road(344.5, 63.5)
    lines.append('\n        <!-- 5. 關新二街東段 (自星巴克路口連通至關新東路/日光公園東南角, 長 109m, 寬 14m) -->')
    lines.append(f'        <collision name="gx2_east_col"><pose>{gx2_e_mid_e:.3f} {gx2_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>109.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx2_east_vis"><pose>{gx2_e_mid_e:.3f} {gx2_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>109.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    gx2_w_mid_e, gx2_w_mid_n = pt_road(344.5, -70.0)
    lines.append('        <!-- 關新二街西段 (自橘時咖啡/星巴克路口向西通往新莊街, 長 120m, 寬 14m) -->')
    lines.append(f'        <collision name="gx2_west_col"><pose>{gx2_w_mid_e:.3f} {gx2_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>120.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx2_west_vis"><pose>{gx2_w_mid_e:.3f} {gx2_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>120.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 6. 關新北路 (Guanxin North Road: at s = 488m, width = 14m)
    gxn_e_mid_e, gxn_e_mid_n = pt_road(488.0, 63.5)
    lines.append('\n        <!-- 6. 關新北路東段 (日光公園東北橫向幹道, 連通至關新東路, 長 109m, 寬 14m) -->')
    lines.append(f'        <collision name="gxn_east_col"><pose>{gxn_e_mid_e:.3f} {gxn_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>109.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gxn_east_vis"><pose>{gxn_e_mid_e:.3f} {gxn_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>109.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    gxn_w_mid_e, gxn_w_mid_n = pt_road(488.0, -60.0)
    lines.append('        <!-- 關新北路西段 (新莊車站前西側聯絡道, 長 100m, 寬 14m) -->')
    lines.append(f'        <collision name="gxn_west_col"><pose>{gxn_w_mid_e:.3f} {gxn_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>100.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gxn_west_vis"><pose>{gxn_w_mid_e:.3f} {gxn_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>100.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 7. 後方服務巷弄
    alley_len = 236.0
    alley_mid_e, alley_mid_n = pt_road(88.0 + alley_len / 2.0, 42.0)
    lines.append(f'\n        <!-- 7. 東側商圈後方服務巷弄 (長 {alley_len}m, 寬 6.5m) -->')
    lines.append(f'        <collision name="service_alley_col"><pose>{alley_mid_e:.3f} {alley_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{alley_len} 6.5 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="service_alley_vis"><pose>{alley_mid_e:.3f} {alley_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{alley_len} 6.5 0.02</size></box></geometry><material><ambient>0.24 0.24 0.25 1</ambient><diffuse>0.26 0.26 0.27 1</diffuse></material></visual>')

    # 8. 關東路主幹道 (Guandong Road: 5段真實路網, 連通光復路至新莊車站東側並穿過鐵路接埔頂路)
    lines.append('\n        <!-- ===== 8. 關東路主幹道 (Guandong Road: 依真實GIS連通光復路、新莊車站東側與埔頂路) ===== -->')
    gd_segs = [
        ("gd_seg1_south", 0.0, 290.0, 350.0, 240.0, "關東路南段: 自光復路向北", 12.0),
        ("gd_seg2_mid", 350.0, 240.0, 550.0, 215.0, "關東路中段: 通往新莊車站商圈", 12.0),
        ("gd_seg3_station", 550.0, 215.0, 685.0, 200.0, "關東路車站段: 新莊車站東側聯絡", 14.0),
        ("gd_seg4_underpass", 685.0, 200.0, 760.0, 110.0, "關東路跨線/涵洞段: 穿越鐵路往西北", 14.0),
        ("gd_seg5_north", 760.0, 110.0, 840.0, -10.0, "關東路北段: 連接埔頂路口", 14.0),
    ]
    for name, s1, p1, s2, p2, desc, width in gd_segs:
        e1, n1 = pt_road(s1, p1)
        e2, n2 = pt_road(s2, p2)
        de, dn = e2 - e1, n2 - n1
        l = math.hypot(de, dn)
        yaw = math.atan2(dn, de)
        me, mn = (e1 + e2) / 2.0, (n1 + n2) / 2.0
        lines.append(f'        <!-- 關東路: {desc} (長 {l:.1f}m, 寬 {width:.1f}m) -->')
        lines.append(f'        <collision name="{name}_col"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} {width:.1f} 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
        lines.append(f'        <visual name="{name}_vis"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} {width:.1f} 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_line"><pose>{me:.3f} {mn:.3f} 0.022 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # 9. 埔頂路與新莊車站北側聯絡便道
    lines.append('\n        <!-- ===== 9. 車站北側新馬路：埔頂路拓寬段與內灣線橋下便道 ===== -->')
    puding_segs = [
        ("puding_seg1_west", 840.0, -150.0, 840.0, -10.0, "埔頂路西段: 往光埔重劃區方向", 16.0),
        ("puding_seg2_mid", 840.0, -10.0, 830.0, 120.0, "埔頂路中段: 關東路路口至便道路口", 16.0),
        ("puding_seg3_east", 830.0, 120.0, 810.0, 260.0, "埔頂路東段: 跨越鐵路往公道五路方向", 16.0),
    ]
    for name, s1, p1, s2, p2, desc, width in puding_segs:
        e1, n1 = pt_road(s1, p1)
        e2, n2 = pt_road(s2, p2)
        de, dn = e2 - e1, n2 - n1
        l = math.hypot(de, dn)
        yaw = math.atan2(dn, de)
        me, mn = (e1 + e2) / 2.0, (n1 + n2) / 2.0
        lines.append(f'        <!-- 埔頂路: {desc} (長 {l:.1f}m, 寬 {width:.1f}m) -->')
        lines.append(f'        <collision name="{name}_col"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} {width:.1f} 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
        lines.append(f'        <visual name="{name}_vis"><pose>{me:.3f} {mn:.3f} 0.01 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} {width:.1f} 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_line"><pose>{me:.3f} {mn:.3f} 0.022 0 0 {yaw:.5f}</pose><geometry><box><size>{l:.2f} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # 內灣線橋下便道 (自新莊車站前沿高架鐵路下方通往埔頂路)
    v_e1, v_n1 = pt_road(685.0, 200.0)
    v_e2, v_n2 = pt_road(830.0, 120.0)
    v_de, v_dn = v_e2 - v_e1, v_n2 - v_n1
    v_l = math.hypot(v_de, v_dn)
    v_yaw = math.atan2(v_dn, v_de)
    v_me, v_mn = (v_e1 + v_e2) / 2.0, (v_n1 + v_n2) / 2.0
    lines.append(f'        <!-- 內灣線橋下便道 (長 {v_l:.1f}m, 寬 10m) -->')
    lines.append(f'        <collision name="viaduct_rd_col"><pose>{v_me:.3f} {v_mn:.3f} 0.01 0 0 {v_yaw:.5f}</pose><geometry><box><size>{v_l:.2f} 10.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="viaduct_rd_vis"><pose>{v_me:.3f} {v_mn:.3f} 0.01 0 0 {v_yaw:.5f}</pose><geometry><box><size>{v_l:.2f} 10.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
    lines.append(f'        <visual name="viaduct_rd_line"><pose>{v_me:.3f} {v_mn:.3f} 0.022 0 0 {v_yaw:.5f}</pose><geometry><box><size>{v_l:.2f} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # 10. 關新路中央綠化分隔島
    lines.append('\n        <!-- ===== 10. 關新路中央綠化分隔島 (Central Median Islands) ===== -->')
    medians = [
        ("median_s1", 16.0, 76.0, "南段1 (光復路口至關新一街口)"),
        ("median_mid", 100.0, 332.0, "中段 (關新一街口至關新二街口)"),
        ("median_n1", 356.0, 476.0, "北段1 (關新二街口至關新北路口)")
    ]
    for name, s_start, s_end, desc in medians:
        m_len = s_end - s_start
        m_mid = s_start + m_len / 2.0
        me, mn = pt_road(m_mid, 0.0)
        lines.append(f'        <!-- 分隔島: {desc} -->')
        lines.append(f'        <collision name="{name}_col"><pose>{me:.3f} {mn:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len:.2f} 1.8 0.20</size></box></geometry></collision>')
        lines.append(f'        <visual name="{name}_curb"><pose>{me:.3f} {mn:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len:.2f} 1.8 0.20</size></box></geometry><material><ambient>0.6 0.6 0.6 1</ambient><diffuse>0.65 0.65 0.65 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_lawn"><pose>{me:.3f} {mn:.3f} 0.205 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len - 1.2:.2f} 1.4 0.01</size></box></geometry><material><ambient>0.20 0.52 0.20 1</ambient><diffuse>0.25 0.58 0.25 1</diffuse></material></visual>')

    # 11. 道路標線
    lines.append('\n        <!-- ===== 11. 台灣標準道路標線 (Lane Markings, Double Yellow, Dash Lines) ===== -->')
    for s_st, s_ed in [(16.0, 76.0), (100.0, 332.0), (356.0, 476.0)]:
        d_len = s_ed - s_st
        d_mid = s_st + d_len / 2.0
        dne, dnn = pt_road(d_mid, 4.5)
        lines.append(f'        <visual name="dash_r_{int(s_st)}"><pose>{dne:.3f} {dnn:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{d_len:.2f} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
        dse, dsn = pt_road(d_mid, -4.5)
        lines.append(f'        <visual name="dash_l_{int(s_st)}"><pose>{dse:.3f} {dsn:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{d_len:.2f} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')

    # 光復路中央雙黃線與分道虛線 (Guangfu Double Yellow & Lane Dividers)
    lines.append(f'        <visual name="guangfu_center_line"><pose>{gf_mid_e:.3f} {gf_mid_n:.3f} 0.022 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>{gf_len} 0.30 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')
    gfe_e, gfe_n = pt_road(4.0, 25.0)
    lines.append(f'        <visual name="guangfu_dash_eb"><pose>{gfe_e:.3f} {gfe_n:.3f} 0.022 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>{gf_len} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
    gfw_e, gfw_n = pt_road(-4.0, 25.0)
    lines.append(f'        <visual name="guangfu_dash_wb"><pose>{gfw_e:.3f} {gfw_n:.3f} 0.022 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>{gf_len} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')

    # 光復路與關新路口斑馬線 (Crosswalks)
    cw_gx_e, cw_gx_n = pt_road(13.5, 0.0)
    lines.append(f'        <visual name="crosswalk_guanxin_vis"><pose>{cw_gx_e:.3f} {cw_gx_n:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>3.0 18.0 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.98 0.98 0.98 1</diffuse></material></visual>')
    cw_gfw_e, cw_gfw_n = pt_road(0.0, -10.5)
    lines.append(f'        <visual name="crosswalk_guangfu_w_vis"><pose>{cw_gfw_e:.3f} {cw_gfw_n:.3f} 0.022 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>3.0 24.0 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.98 0.98 0.98 1</diffuse></material></visual>')
    cw_gfe_e, cw_gfe_n = pt_road(0.0, 10.5)
    lines.append(f'        <visual name="crosswalk_guangfu_e_vis"><pose>{cw_gfe_e:.3f} {cw_gfe_n:.3f} 0.022 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>3.0 24.0 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.98 0.98 0.98 1</diffuse></material></visual>')

    # 12. 人行道鋪面 (Sidewalk Surfaces)
    lines.append('\n        <!-- ===== 12. 人行道透水磚鋪面 (Permeable Brick Sidewalks: 寬度 4.5m ~ 8.0m) ===== -->')
    w_sw_len = 472.0
    w_sw_mid_e, w_sw_mid_n = pt_road(16.0 + w_sw_len / 2.0, -11.5)
    lines.append(f'        <collision name="sw_west_col"><pose>{w_sw_mid_e:.3f} {w_sw_mid_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{w_sw_len} 5.0 0.20</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_west_vis"><pose>{w_sw_mid_e:.3f} {w_sw_mid_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{w_sw_len} 5.0 0.20</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse></material></visual>')

    e_sw_len = 472.0
    e_sw_mid_e, e_sw_mid_n = pt_road(16.0 + e_sw_len / 2.0, 11.5)
    lines.append(f'        <collision name="sw_east_col"><pose>{e_sw_mid_e:.3f} {e_sw_mid_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{e_sw_len} 5.0 0.20</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_east_vis"><pose>{e_sw_mid_e:.3f} {e_sw_mid_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{e_sw_len} 5.0 0.20</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse></material></visual>')

    # 光復路北側人行道 (銜接北歐三小國南棟騎樓至光復路北緣, 寬8m, 長115m)
    sw_gfn_e, sw_gfn_n = pt_road(16.0, -68.5)
    lines.append(f'        <!-- 光復路北側人行道 (西段: 銜接北歐三小國南棟騎樓, 寬8m, 長115m) -->')
    lines.append(f'        <collision name="sw_guangfu_north_col"><pose>{sw_gfn_e:.3f} {sw_gfn_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>115.0 8.0 0.20</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_guangfu_north_vis"><pose>{sw_gfn_e:.3f} {sw_gfn_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>115.0 8.0 0.20</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse></material></visual>')

    # 光復路北側東段人行道 (關新路東側至關新東路, 寬5m, 長165m)
    sw_gfne_e, sw_gfne_n = pt_road(14.5, 93.35)
    lines.append(f'        <!-- 光復路北側人行道 (東段: 關新路口至關新東路口, 寬5m, 長165m) -->')
    lines.append(f'        <collision name="sw_guangfu_ne_col"><pose>{sw_gfne_e:.3f} {sw_gfne_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>165.0 5.0 0.20</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_guangfu_ne_vis"><pose>{sw_gfne_e:.3f} {sw_gfne_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>165.0 5.0 0.20</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse></material></visual>')

    # 光復路南側連續人行道 (寬5m, 長450m)
    sw_gfs_e, sw_gfs_n = pt_road(-14.5, 25.0)
    lines.append(f'        <!-- 光復路南側全線人行道 (寬5m, 長450m) -->')
    lines.append(f'        <collision name="sw_guangfu_south_col"><pose>{sw_gfs_e:.3f} {sw_gfs_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>450.0 5.0 0.20</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_guangfu_south_vis"><pose>{sw_gfs_e:.3f} {sw_gfs_n:.3f} 0.10 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>450.0 5.0 0.20</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse></material></visual>')

    lines.append('      </link>')
    lines.append('    </model>')
    return '\n'.join(lines)

def build_smart_parking_poles():
    lines = []
    lines.append('    <!-- ==================== 路邊智慧停車柱系統 (Smart Parking Meter Poles) ==================== -->')
    stalls = [
        ("pole_e_01", 108.0, 9.5, 0.0), ("pole_e_02", 114.0, 9.5, 0.0), ("pole_e_03", 120.0, 9.5, 0.0),
        ("pole_e_04", 126.0, 9.5, 0.0), ("pole_e_05", 132.0, 9.5, 0.0), ("pole_e_06", 138.0, 9.5, 0.0),
        ("pole_e_07", 144.0, 9.5, 0.0), ("pole_e_08", 150.0, 9.5, 0.0), ("pole_e_09", 156.0, 9.5, 0.0),
        ("pole_e_10", 162.0, 9.5, 0.0), ("pole_e_11", 168.0, 9.5, 0.0), ("pole_e_12", 174.0, 9.5, 0.0),
        ("pole_w_01", 110.0, -9.5, math.pi), ("pole_w_02", 116.0, -9.5, math.pi), ("pole_w_03", 122.0, -9.5, math.pi),
        ("pole_w_04", 128.0, -9.5, math.pi), ("pole_w_05", 134.0, -9.5, math.pi), ("pole_w_06", 140.0, -9.5, math.pi),
        ("pole_w_07", 146.0, -9.5, math.pi), ("pole_w_08", 152.0, -9.5, math.pi), ("pole_w_09", 158.0, -9.5, math.pi),
        ("pole_w_10", 164.0, -9.5, math.pi), ("pole_w_11", 170.0, -9.5, math.pi), ("pole_w_12", 176.0, -9.5, math.pi),
    ]
    for name, s, perp, yaw_rel in stalls:
        pe, pn = pt_road(s, perp)
        pyaw = ROAD_YAW + yaw_rel
        lines.append(f'    <include><name>{name}</name><uri>model://smart_parking_meter_pole</uri><pose>{pe:.3f} {pn:.3f} 0.20 0 0 {pyaw:.5f}</pose></include>')
    return '\n'.join(lines)

def build_east_commercial_strip():
    lines = []
    lines.append('    <!-- ==================== 寶雅與關新一街之間中介建築群 (Intermediary Block: 十詠八方 12F) ==================== -->')
    e12, n12 = pt_road(122.0, 29.75)
    lines.append('    <!-- 關新路 6~18 號：十詠八方 12層大樓 (星島海南雞飯、精品門市) -->')
    lines.append('    <model name="block_gx1_to_poya">')
    lines.append('      <static>true</static>')
    lines.append(f'      <pose>{e12:.3f} {n12:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    lines.append('      <link name="bldg_link">')
    lines.append('        <collision name="tower_col"><pose>0 0 21.0 0 0 0</pose><geometry><box><size>52 30.5 42.0</size></box></geometry></collision>')
    lines.append('        <visual name="tower_main_vis"><pose>0 0 21.0 0 0 0</pose><geometry><box><size>52 30.5 42.0</size></box></geometry><material><ambient>0.76 0.74 0.70 1</ambient><diffuse>0.82 0.80 0.76 1</diffuse></material></visual>')
    lines.append('        <visual name="tower_crown"><pose>0 0 43.5 0 0 0</pose><geometry><box><size>48 26 3.0</size></box></geometry><material><ambient>0.3 0.3 0.32 1</ambient><diffuse>0.35 0.35 0.38 1</diffuse></material></visual>')
    lines.append('        <visual name="balconies_front"><pose>0 15.55 23.0 0 0 0</pose><geometry><box><size>48 0.8 34.0</size></box></geometry><material><ambient>0.2 0.25 0.3 0.9</ambient><diffuse>0.25 0.3 0.35 0.9</diffuse></material></visual>')
    lines.append('        <visual name="retail_canopy"><pose>0 15.75 4.2 0 0 0</pose><geometry><box><size>52 1.8 0.3</size></box></geometry><material><ambient>0.22 0.22 0.24 1</ambient><diffuse>0.25 0.25 0.28 1</diffuse></material></visual>')
    lines.append('        <visual name="singdao_fascia"><pose>-18.0 15.35 3.2 0 0 0</pose><geometry><box><size>15.5 0.15 1.4</size></box></geometry><material><ambient>0.92 0.75 0.1 1</ambient><diffuse>0.98 0.82 0.12 1</diffuse><emissive>0.7 0.55 0.1 1</emissive></material></visual>')
    lines.append('        <visual name="singdao_glass"><pose>-18.0 15.3 1.5 0 0 0</pose><geometry><box><size>15.0 0.1 2.4</size></box></geometry><material><ambient>0.1 0.15 0.2 0.85</ambient><diffuse>0.15 0.2 0.25 0.85</diffuse></material></visual>')
    lines.append('        <visual name="retail_fascia_mid"><pose>8.0 15.35 3.2 0 0 0</pose><geometry><box><size>35.5 0.15 1.4</size></box></geometry><material><ambient>0.28 0.28 0.3 1</ambient><diffuse>0.32 0.32 0.35 1</diffuse></material></visual>')
    lines.append('        <visual name="retail_glass_mid"><pose>8.0 15.3 1.5 0 0 0</pose><geometry><box><size>35.0 0.1 2.4</size></box></geometry><material><ambient>0.1 0.15 0.2 0.85</ambient><diffuse>0.15 0.2 0.25 0.85</diffuse></material></visual>')
    lines.append('      </link>')
    lines.append('    </model>')

    lines.append('\n    <!-- ==================== 東側商圈六大名店 (POYA, 起家雞, 麥當勞, 國泰世華, 康是美, 星巴克) ==================== -->')
    stores = [
        ("poya_store", "model://poya_store", 171.0, 22.0, "POYA 寶雅新竹關新店 (20 號)"),
        ("cheogajip_store", "model://cheogajip_store", 196.0, 21.0, "起家雞韓式炸雞新竹關新店 (22 號)"),
        ("mcdonalds_building", "model://mcdonalds_building", 226.0, 23.5, "麥當勞新竹關新店得來速 (26 號)"),
        ("cathay_bank_building", "model://cathay_bank_building", 266.0, 24.0, "國泰世華銀行 & 日光大樓 (32 號)"),
        ("cosmed_store", "model://cosmed_store", 297.0, 21.5, "COSMED 康是美新竹日光門市 (36 號)"),
        ("starbucks_building", "model://starbucks_building", 328.0, 21.75, "星巴克新竹日光門市 (38 號, 關新二街口)"),
    ]
    for name, uri, s, perp, desc in stores:
        e, n = pt_road(s, perp)
        lines.append(f'    <!-- {desc} -->')
        lines.append(f'    <include><name>{name}</name><uri>{uri}</uri><pose>{e:.3f} {n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose></include>')

    return '\n'.join(lines)

def build_phase4_blocks():
    lines = []
    lines.append('    <!-- ==================== Phase 4: 教育園區與代表性大型住商豪宅街區 ==================== -->')
    lines.append('    <!-- 關新路西側: 北歐三小國(丹麥/芬蘭/挪威)、月影國際會館(18F)、橘時咖啡(2F)、東京中城(24F)、富宇君鼎(24F) | 東側: 關埔國小 -->')

    # 1. 北歐三小國
    lines.append('\n    <!-- 1. 昌益丹麥 / 芬蘭 / 挪威現代住宅社區 (15層樓, 48m, 東西橫向雙排 + 中央110m公園 + 雙道路對齊關新一街 + 外側複製棟) -->')
    e_nordic, n_nordic = pt_road(88.0, -14.0)
    lines.append('    <include>')
    lines.append('      <name>changyi_residential_block</name>')
    lines.append('      <uri>model://changyi_residential_block</uri>')
    lines.append(f'      <pose>{e_nordic:.3f} {n_nordic:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 2. 月影國際會館
    e_ms, n_ms = pt_road(245.0, -32.0)
    lines.append('\n    <!-- 2. 月影國際會館 (Moon Shadow 18層樓, 58m, 北歐三小國北側連接關新路商住名邸, 挑高連續騎樓) -->')
    lines.append('    <include>')
    lines.append('      <name>moon_shadow_building</name>')
    lines.append('      <uri>model://moon_shadow_building</uri>')
    lines.append(f'      <pose>{e_ms:.3f} {n_ms:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 3. 橘時咖啡
    e_oh, n_oh = pt_road(326.0, -22.0)
    lines.append('\n    <!-- 3. 橘時咖啡 (Orange Hour Cafe 2層樓, 8m, 臨關新路與關新二街西南轉角夾角, 全景轉角落地窗與露天雅座) -->')
    lines.append('    <include>')
    lines.append('      <name>orange_hour_cafe</name>')
    lines.append('      <uri>model://orange_hour_cafe</uri>')
    lines.append(f'      <pose>{e_oh:.3f} {n_oh:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 4. 東京中城雙塔豪宅
    e_tr, n_tr = pt_road(416.0, -33.0)
    lines.append('\n    <!-- 4. 東京中城雙塔現代豪宅地標 (24層樓, 72m, 日光公園西側對街, 挑高大理石精品商鋪基座, 垂直金屬格柵) -->')
    lines.append('    <include>')
    lines.append('      <name>tokyo_roppongi_towers</name>')
    lines.append('      <uri>model://tokyo_roppongi_towers</uri>')
    lines.append(f'      <pose>{e_tr:.3f} {n_tr:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 5. 富宇君鼎高層豪宅
    e_fj, n_fj = pt_road(560.0, -32.0)
    lines.append('\n    <!-- 5. 富宇君鼎 24 層天際線豪宅地標 (高 78m, 發光造型冠頂 82m, 新莊車站迎賓廣場西北側) -->')
    lines.append('    <include>')
    lines.append('      <name>fuyu_junding_tower</name>')
    lines.append('      <uri>model://fuyu_junding_tower</uri>')
    lines.append(f'      <pose>{e_fj:.3f} {n_fj:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 6. 新竹市立關埔國小校園
    e_gp, n_gp = pt_road(280.0, 220.0)
    lines.append('\n    <!-- 6. 新竹市立關埔國小校園 (有機低矮聚落校舍、木紋清水模立面、200m 紅土 PU 跑道操場、穿透式金屬格柵圍牆) -->')
    lines.append('    <include>')
    lines.append('      <name>guanpu_elementary_school</name>')
    lines.append('      <uri>model://guanpu_elementary_school</uri>')
    lines.append(f'      <pose>{e_gp:.3f} {n_gp:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    lines.append('    </include>')

    return '\n'.join(lines)

def transform_commercial_details_section(content):
    details_match = re.search(r'(<model name="commercial_strip_details">.*?</model>)', content, flags=re.DOTALL)
    if details_match:
        details_str = details_match.group(1)
        pose_pat = re.compile(r'<pose>\s*([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s*</pose>')
        transformed_details = pose_pat.sub(transform_old_pose, details_str)
        content = content.replace(details_str, transformed_details)

    scooter_pat = re.compile(r'(<include>\s*<name>scooter_.*?<pose>\s*)([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)(\s*</pose>.*?</include>)', flags=re.DOTALL)
    def trans_scooter(m):
        prefix = m.group(1)
        x = float(m.group(2))
        y = float(m.group(3))
        z = float(m.group(4))
        r = float(m.group(5))
        p = float(m.group(6))
        yaw = float(m.group(7))
        suffix = m.group(8)
        e, n = pt_road(x, -y)
        nyaw = yaw + ROAD_YAW
        return f"{prefix}{e:.3f} {n:.3f} {z:.3f} {r:.3f} {p:.3f} {nyaw:.5f}{suffix}"
    content = scooter_pat.sub(trans_scooter, content)

    tree_pat = re.compile(r'(<include>\s*<name>tree_([ew])_\d+</name>\s*<uri>model://street_tree</uri>\s*<pose>\s*)([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)(\s*</pose>\s*</include>)')
    def trans_tree(m):
        prefix = m.group(1)
        side = m.group(2)
        s = float(m.group(3))
        perp = 9.8 if side == "e" else -9.8
        suffix = m.group(9)
        e, n = pt_road(s, perp)
        return f"{prefix}{e:.3f} {n:.3f} 0.20 0 0 {ROAD_YAW:.5f}{suffix}"
    content = tree_pat.sub(trans_tree, content)

    signal_pat = re.compile(r'(<include>\s*<name>signal_pole_gx2_([a-z]+)</name>\s*<uri>model://traffic_signal_pole</uri>\s*<pose>\s*)([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)(\s*</pose>\s*</include>)')
    def trans_signal(m):
        prefix = m.group(1)
        side = m.group(2)
        suffix = m.group(9)
        if side == "se":
            s, perp = 338.0, 9.5
            yaw = ROAD_YAW + math.pi / 2.0
        else:
            s, perp = 350.0, -9.5
            yaw = ROAD_YAW - math.pi / 2.0
        e, n = pt_road(s, perp)
        return f"{prefix}{e:.3f} {n:.3f} 0.20 0 0 {yaw:.5f}{suffix}"
    content = signal_pat.sub(trans_signal, content)

    return content

def update_phase3_landmarks(content):
    # 1. Update railway_viaduct pose
    v_pat = r'(<include>\s*<name>railway_viaduct</name>\s*<uri>model://railway_viaduct</uri>\s*<pose>)[^<]+(</pose>\s*</include>)'
    content = re.sub(v_pat, r'\g<1>338.460 625.110 0.0 0 0 -0.22568\g<2>', content)

    # 2. Update xinzhuang_station pose
    s_pat = r'(<include>\s*<name>xinzhuang_station</name>\s*<uri>model://xinzhuang_station</uri>\s*<pose>)[^<]+(</pose>\s*</include>)'
    content = re.sub(s_pat, r'\g<1>372.576 617.282 0.0 0 0 -0.22568\g<2>', content)

    # 3. Update xinzhuang_station_plaza
    plaza_sdf = '''    <!-- 新莊車站前迎賓廣場與計程車排班避車道 (Station Plaza & Taxi Drop-off Bay) -->
    <model name="xinzhuang_station_plaza">
      <static>true</static>
      <link name="plaza_link">
        <collision name="plaza_deck_col"><pose>343.336 623.995 0.075 0 0 -0.22568</pose><geometry><box><size>42.0 26.0 0.15</size></box></geometry></collision>
        <visual name="plaza_deck_vis"><pose>343.336 623.995 0.075 0 0 -0.22568</pose><geometry><box><size>42.0 26.0 0.15</size></box></geometry><material><ambient>0.72 0.74 0.76 1</ambient><diffuse>0.78 0.80 0.82 1</diffuse></material></visual>
        <visual name="plaza_planter1"><pose>334.932 632.081 0.35 0 0 -0.22568</pose><geometry><box><size>8.0 2.2 0.50</size></box></geometry><material><ambient>0.45 0.48 0.5 1</ambient><diffuse>0.52 0.55 0.58 1</diffuse></material></visual>
        <visual name="plaza_shrub1"><pose>334.932 632.081 0.80 0 0 -0.22568</pose><geometry><box><size>7.6 1.8 0.45</size></box></geometry><material><ambient>0.15 0.48 0.18 1</ambient><diffuse>0.20 0.55 0.22 1</diffuse></material></visual>
        <visual name="plaza_planter2"><pose>354.425 627.605 0.35 0 0 -0.22568</pose><geometry><box><size>8.0 2.2 0.50</size></box></geometry><material><ambient>0.45 0.48 0.5 1</ambient><diffuse>0.52 0.55 0.58 1</diffuse></material></visual>
        <visual name="plaza_shrub2"><pose>354.425 627.605 0.80 0 0 -0.22568</pose><geometry><box><size>7.6 1.8 0.45</size></box></geometry><material><ambient>0.15 0.48 0.18 1</ambient><diffuse>0.20 0.55 0.22 1</diffuse></material></visual>
        <visual name="flagpole1"><pose>348.162 631.608 4.0 0 0 0</pose><geometry><cylinder><radius>0.05</radius><length>8.0</length></cylinder></geometry><material><ambient>0.8 0.8 0.85 1</ambient><diffuse>0.9 0.9 0.95 1</diffuse></material></visual>
      </link>
    </model>'''
    p_pat = r'<!-- 新莊車站前迎賓廣場與計程車排班避車道.*?<model name="xinzhuang_station_plaza">.*?</model>'
    content = re.sub(p_pat, plaza_sdf, content, flags=re.DOTALL)
    return content

def main():
    print(f"Loading world from {WORLD_PATH}...")
    with open(WORLD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("Generating accurate Guanxin East Road network...")
    road_network_sdf = build_accurate_road_network_sdf()
    parking_poles_sdf = build_smart_parking_poles()

    road_pat = r'<!-- ==================== Phase 2: 全域路網精確鋪設與路邊智慧停車柱系統 ====================.*?<!-- ==================== 寶雅與關新一街之間中介建築群'
    new_road_block = road_network_sdf + "\n\n" + parking_poles_sdf + "\n\n"
    if not re.search(road_pat, content, flags=re.DOTALL):
        print("Error: Could not locate Phase 2 road network section!")
        return False
    content = re.sub(road_pat, new_road_block + "<!-- ==================== 寶雅與關新一街之間中介建築群", content, flags=re.DOTALL)

    print("Repositioning commercial stores...")
    east_stores_sdf = build_east_commercial_strip()
    commercial_pat = r'<!-- ==================== 寶雅與關新一街之間中介建築群.*?<!-- ==================== 寶雅至星巴克一整條路超精細真實街道設施'
    if not re.search(commercial_pat, content, flags=re.DOTALL):
        print("Error: Could not locate commercial stores section!")
        return False
    content = re.sub(commercial_pat, east_stores_sdf + "\n\n    <!-- ==================== 寶雅至星巴克一整條路超精細真實街道設施", content, flags=re.DOTALL)

    print("Transforming sidewalk amenities, scooters, and street trees...")
    content = transform_commercial_details_section(content)

    midblock_pat = r'<!-- ==================== 中街現代住宅社區群.*?<!-- ==================== Phase 4:'
    if re.search(midblock_pat, content, flags=re.DOTALL):
        content = re.sub(midblock_pat, "<!-- ==================== Phase 4:", content, flags=re.DOTALL)

    print("Updating Phase 4 West side buildings and Guanpu school...")
    phase4_sdf = build_phase4_blocks()
    phase4_pat = r'<!-- ==================== Phase 4:.*?<!-- ==================== Phase 3: 重點交通與公共休閒地標建模'
    if not re.search(phase4_pat, content, flags=re.DOTALL):
        print("Error: Could not locate Phase 4 section!")
        return False
    content = re.sub(phase4_pat, phase4_sdf + "\n\n    <!-- ==================== Phase 3: 重點交通與公共休閒地標建模", content, flags=re.DOTALL)

    print("Relocating Xinzhuang Station, station plaza, and railway viaduct...")
    content = update_phase3_landmarks(content)

    with open(WORLD_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("Master transformation complete! World SDF successfully updated.")
    return True

if __name__ == "__main__":
    main()
