#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Phase 2 Road Network & Smart Parking Infrastructure for Guanxin World SDF.
Author: Autonomous Robotics & Simulation Team
Project: Guanxin Road Digital Twin Simulation
"""

import math
import sys

# Geodetic / Local ENU constants
BEARING_DEG = 12.930438  # Guanxin Road bearing from True North (East of North)
BEARING_RAD = math.radians(BEARING_DEG)
ROAD_YAW = math.radians(90.0 - BEARING_DEG)   # 77.06956 deg = 1.345116 rad
CROSS_YAW = ROAD_YAW - math.radians(90.0)     # -12.93044 deg = -0.225678 rad

# Direction vectors
U_ROAD = (math.sin(BEARING_RAD), math.cos(BEARING_RAD))   # (0.22376, 0.97464) along Guanxin Rd
U_PERP = (math.cos(BEARING_RAD), -math.sin(BEARING_RAD))  # (0.97464, -0.22376) towards Guanxin East Rd (East-SE)

EAST_ROAD_OFFSET = 153.3  # Guanxin East Road offset in perpendicular direction (meters)


def pt_road(s, offset_perp=0.0):
    """Calculates ENU (E, N) coordinate given distance along Guanxin Road (s) and perpendicular offset."""
    e = s * U_ROAD[0] + offset_perp * U_PERP[0]
    n = s * U_ROAD[1] + offset_perp * U_PERP[1]
    return e, n


def generate_road_network_sdf():
    """Generates the comprehensive Phase 2 road network SDF elements."""
    lines = []
    lines.append('    <!-- ==================== Phase 2: 全域路網精確鋪設與路邊智慧停車柱系統 ==================== -->')
    lines.append('    <!-- 涵蓋 58 公頃: 關新路(18m)、關新東路(14m)、光復路(24m)、關新一街(12m)、關新二街(14m)、關新北路(14m)、西側社區巷弄 -->')
    lines.append('    <model name="road_network">')
    lines.append('      <static>true</static>')
    lines.append('      <link name="road_link">')

    # 1. 關新路主幹道柏油路面 (Guanxin Road: s = 0 to 860m, width = 18m, 4 lanes)
    gx_len = 860.0
    gx_mid_e, gx_mid_n = pt_road(gx_len / 2.0, 0.0)
    lines.append(f'        <!-- 1. 關新路主幹道柏油路面 (長 {gx_len}m, 寬 18m, 雙向四線道, 方位角 {BEARING_DEG:.2f}° / yaw={ROAD_YAW:.4f}) -->')
    lines.append(f'        <collision name="gx_road_col"><pose>{gx_mid_e:.3f} {gx_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gx_len} 18.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx_road_vis"><pose>{gx_mid_e:.3f} {gx_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gx_len} 18.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')

    # 2. 關新東路主幹道柏油路面 (Guanxin East Road: s = 20 to 840m, width = 14m, offset = +153.3m)
    gxe_len = 820.0
    gxe_mid_e, gxe_mid_n = pt_road(20.0 + gxe_len / 2.0, EAST_ROAD_OFFSET)
    lines.append(f'        <!-- 2. 關新東路主幹道柏油路面 (長 {gxe_len}m, 寬 14m, 雙向二線道, 平行於關新路東側 153.3m) -->')
    lines.append(f'        <collision name="gxe_road_col"><pose>{gxe_mid_e:.3f} {gxe_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gxe_len} 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gxe_road_vis"><pose>{gxe_mid_e:.3f} {gxe_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gxe_len} 14.0 0.02</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')

    # 3. 光復路一段柏油路面 (Guangfu Road Sec. 1: width = 24m, East-West at Y = -12m)
    lines.append('        <!-- 3. 光復路一段主幹道 (南界門戶橫向幹道, 長 450m, 寬 24m, 雙向六線道) -->')
    lines.append('        <collision name="guangfu_road_col"><pose>10.0 -12.0 0.01 0 0 0</pose><geometry><box><size>450.0 24.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append('        <visual name="guangfu_road_vis"><pose>10.0 -12.0 0.01 0 0 0</pose><geometry><box><size>450.0 24.0 0.02</size></box></geometry><material><ambient>0.20 0.20 0.21 1</ambient><diffuse>0.22 0.22 0.23 1</diffuse></material></visual>')

    # 4. 關新一街 (Guanxin 1st Street: at s = 88m, width = 12m)
    # East section (to Guanxin East Rd, len = 135m, mid offset = +77.5m)
    gx1_e_mid_e, gx1_e_mid_n = pt_road(88.0, 77.5)
    lines.append('        <!-- 4. 關新一街東段 (自關新路連通至關新東路, 長 135m, 寬 12m) -->')
    lines.append(f'        <collision name="gx1_east_col"><pose>{gx1_e_mid_e:.3f} {gx1_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 12.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx1_east_vis"><pose>{gx1_e_mid_e:.3f} {gx1_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 12.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    # West section (to Lane 19, len = 60m, mid offset = -40m)
    gx1_w_mid_e, gx1_w_mid_n = pt_road(88.0, -40.0)
    lines.append('        <!-- 關新一街西段 (自關新路延伸至西側社區, 長 60m, 寬 12m) -->')
    lines.append(f'        <collision name="gx1_west_col"><pose>{gx1_w_mid_e:.3f} {gx1_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>60.0 12.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx1_west_vis"><pose>{gx1_w_mid_e:.3f} {gx1_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>60.0 12.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 5. 關新二街 (Guanxin 2nd Street: at s = 344.5m, width = 14m)
    # East section (to Guanxin East Rd, len = 135m, mid offset = +77.5m)
    gx2_e_mid_e, gx2_e_mid_n = pt_road(344.5, 77.5)
    lines.append('        <!-- 5. 關新二街東段 (自星巴克路口連通至關新東路, 長 135m, 寬 14m) -->')
    lines.append(f'        <collision name="gx2_east_col"><pose>{gx2_e_mid_e:.3f} {gx2_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx2_east_vis"><pose>{gx2_e_mid_e:.3f} {gx2_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    # West section (to Lane 63 & Xinzhuang St, len = 120m, mid offset = -70m)
    gx2_w_mid_e, gx2_w_mid_n = pt_road(344.5, -70.0)
    lines.append('        <!-- 關新二街西段 (自星巴克路口向西通往新莊街, 長 120m, 寬 14m) -->')
    lines.append(f'        <collision name="gx2_west_col"><pose>{gx2_w_mid_e:.3f} {gx2_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>120.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gx2_west_vis"><pose>{gx2_w_mid_e:.3f} {gx2_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>120.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 6. 關新北路 (Guanxin North Road: at s = 488m, width = 14m)
    # East section (north of Sun Park, len = 135m, mid offset = +77.5m)
    gxn_e_mid_e, gxn_e_mid_n = pt_road(488.0, 77.5)
    lines.append('        <!-- 6. 關新北路東段 (日光公園北側橫向幹道, 長 135m, 寬 14m) -->')
    lines.append(f'        <collision name="gxn_east_col"><pose>{gxn_e_mid_e:.3f} {gxn_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gxn_east_vis"><pose>{gxn_e_mid_e:.3f} {gxn_e_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>135.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')
    # West section (towards railway, len = 100m, mid offset = -60m)
    gxn_w_mid_e, gxn_w_mid_n = pt_road(488.0, -60.0)
    lines.append('        <!-- 關新北路西段 (新莊車站前西側聯絡道, 長 100m, 寬 14m) -->')
    lines.append(f'        <collision name="gxn_west_col"><pose>{gxn_w_mid_e:.3f} {gxn_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>100.0 14.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="gxn_west_vis"><pose>{gxn_w_mid_e:.3f} {gxn_w_mid_n:.3f} 0.01 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>100.0 14.0 0.02</size></box></geometry><material><ambient>0.23 0.23 0.24 1</ambient><diffuse>0.25 0.25 0.26 1</diffuse></material></visual>')

    # 7. 西側與東側社區服務巷弄 (Community Service Alleys: width = 7.0m)
    # Commercial mid-block service alley (parallel to Guanxin Rd, offset +52m, s = 88 to 344m)
    alley_len = 236.0
    alley_mid_e, alley_mid_n = pt_road(88.0 + alley_len / 2.0, 52.0)
    lines.append(f'        <!-- 7. 商圈後方南北向服務巷弄 (長 {alley_len}m, 寬 6.5m) -->')
    lines.append(f'        <collision name="service_alley_col"><pose>{alley_mid_e:.3f} {alley_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{alley_len} 6.5 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="service_alley_vis"><pose>{alley_mid_e:.3f} {alley_mid_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{alley_len} 6.5 0.02</size></box></geometry><material><ambient>0.24 0.24 0.25 1</ambient><diffuse>0.26 0.26 0.27 1</diffuse></material></visual>')

    # West Lane 19 curve connector (offset -65m, s = 20 to 88m)
    w_alley1_e, w_alley1_n = pt_road(54.0, -65.0)
    lines.append('        <!-- 關新路19巷西側住宅聯絡弄 (長 68m, 寬 6.5m) -->')
    lines.append(f'        <collision name="w_alley1_col"><pose>{w_alley1_e:.3f} {w_alley1_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>68.0 6.5 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="w_alley1_vis"><pose>{w_alley1_e:.3f} {w_alley1_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>68.0 6.5 0.02</size></box></geometry><material><ambient>0.24 0.24 0.25 1</ambient><diffuse>0.26 0.26 0.27 1</diffuse></material></visual>')

    # West Lane 63 connector (offset -120m, s = 250 to 344m)
    w_alley2_e, w_alley2_n = pt_road(297.0, -120.0)
    lines.append('        <!-- 關新路63巷與新莊街聯絡弄 (長 94m, 寬 7.0m) -->')
    lines.append(f'        <collision name="w_alley2_col"><pose>{w_alley2_e:.3f} {w_alley2_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>94.0 7.0 0.02</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
    lines.append(f'        <visual name="w_alley2_vis"><pose>{w_alley2_e:.3f} {w_alley2_n:.3f} 0.01 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>94.0 7.0 0.02</size></box></geometry><material><ambient>0.24 0.24 0.25 1</ambient><diffuse>0.26 0.26 0.27 1</diffuse></material></visual>')

    # ==================== 中央綠化分隔島 (Central Median Strips with Curb & Keep-Right) ====================
    lines.append('\n        <!-- ===== 8. 關新路中央綠化分隔島 (Central Median Islands with Keep-Right Signs) ===== -->')
    medians = [
        ("median_s1", 16.0, 76.0, "南段1 (光復路口至關新一街口)"),
        ("median_mid", 100.0, 332.0, "中段 (關新一街口至關新二街口)"),
        ("median_n1", 356.0, 476.0, "北段1 (關新二街口至關新北路口)"),
        ("median_n2", 500.0, 800.0, "北段2 (關新北路口至新莊車站大廳前)")
    ]

    for name, s_start, s_end, desc in medians:
        m_len = s_end - s_start
        m_mid = s_start + m_len / 2.0
        me, mn = pt_road(m_mid, 0.0)
        lines.append(f'        <!-- 分隔島: {desc} (長 {m_len:.1f}m, 寬 1.8m, 高 0.20m) -->')
        lines.append(f'        <collision name="{name}_col"><pose>{me:.3f} {mn:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len:.2f} 1.8 0.20</size></box></geometry></collision>')
        lines.append(f'        <visual name="{name}_curb"><pose>{me:.3f} {mn:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len:.2f} 1.8 0.20</size></box></geometry><material><ambient>0.6 0.6 0.6 1</ambient><diffuse>0.65 0.65 0.65 1</diffuse></material></visual>')
        lines.append(f'        <visual name="{name}_lawn"><pose>{me:.3f} {mn:.3f} 0.205 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{m_len - 1.2:.2f} 1.4 0.01</size></box></geometry><material><ambient>0.20 0.52 0.20 1</ambient><diffuse>0.25 0.58 0.25 1</diffuse></material></visual>')
        # Keep-right warning yellow/black tips at both ends
        s_tip1, n_tip1 = pt_road(s_start + 0.3, 0.0)
        lines.append(f'        <visual name="{name}_tip_s"><pose>{s_tip1:.3f} {n_tip1:.3f} 0.11 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>0.6 1.8 0.21</size></box></geometry><material><ambient>0.90 0.82 0.05 1</ambient><diffuse>0.95 0.88 0.08 1</diffuse></material></visual>')
        s_tip2, n_tip2 = pt_road(s_end - 0.3, 0.0)
        lines.append(f'        <visual name="{name}_tip_n"><pose>{s_tip2:.3f} {n_tip2:.3f} 0.11 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>0.6 1.8 0.21</size></box></geometry><material><ambient>0.90 0.82 0.05 1</ambient><diffuse>0.95 0.88 0.08 1</diffuse></material></visual>')

    # Keep-right sign poles on medians (遵行方向標誌桿)
    for idx, s_sign in enumerate([75.0, 331.0, 475.0]):
        spe, spn = pt_road(s_sign, 0.0)
        lines.append(f'        <visual name="median_sign_pole_{idx}"><pose>{spe:.3f} {spn:.3f} 1.2 0 0 0</pose><geometry><cylinder><radius>0.05</radius><length>2.4</length></cylinder></geometry><material><ambient>0.3 0.3 0.3 1</ambient><diffuse>0.35 0.35 0.35 1</diffuse></material></visual>')
        lines.append(f'        <visual name="median_sign_board_{idx}"><pose>{spe:.3f} {spn:.3f} 2.2 0 0 0</pose><geometry><cylinder><radius>0.35</radius><length>0.04</length></cylinder></geometry><material><ambient>0.0 0.3 0.85 1</ambient><diffuse>0.0 0.4 0.95 1</diffuse><emissive>0.0 0.15 0.45 1</emissive></material></visual>')

    # ==================== 道路標線 (Road Markings & Decals) ====================
    lines.append('\n        <!-- ===== 9. 台灣標準道路標線 (Lane Markings, Double Yellow, Dash Lines) ===== -->')
    # Guanxin Road lane dividers (Northbound: offset +4.5m; Southbound: offset -4.5m)
    for s_st, s_ed in [(16.0, 76.0), (100.0, 332.0), (356.0, 476.0), (500.0, 800.0)]:
        d_len = s_ed - s_st
        d_mid = s_st + d_len / 2.0
        # Northbound divider (right lane)
        dne, dnn = pt_road(d_mid, 4.5)
        lines.append(f'        <visual name="dash_r_{int(s_st)}"><pose>{dne:.3f} {dnn:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{d_len:.2f} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
        # Southbound divider (left lane)
        dse, dsn = pt_road(d_mid, -4.5)
        lines.append(f'        <visual name="dash_l_{int(s_st)}"><pose>{dse:.3f} {dsn:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{d_len:.2f} 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')

    # Guanxin East Road double yellow centerline
    lines.append(f'        <visual name="gxe_center_line"><pose>{gxe_mid_e:.3f} {gxe_mid_n:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{gxe_len} 0.25 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')

    # Guangfu Road double yellow centerline and lane dashes
    lines.append('        <visual name="guangfu_center_line"><pose>10.0 -12.0 0.022 0 0 0</pose><geometry><box><size>450.0 0.30 0.002</size></box></geometry><material><ambient>0.9 0.85 0.1 1</ambient><diffuse>0.95 0.9 0.1 1</diffuse></material></visual>')
    lines.append('        <visual name="guangfu_lane_div1"><pose>10.0 -8.2 0.022 0 0 0</pose><geometry><box><size>450.0 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
    lines.append('        <visual name="guangfu_lane_div2"><pose>10.0 -4.4 0.022 0 0 0</pose><geometry><box><size>450.0 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
    lines.append('        <visual name="guangfu_lane_div3"><pose>10.0 -15.8 0.022 0 0 0</pose><geometry><box><size>450.0 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
    lines.append('        <visual name="guangfu_lane_div4"><pose>10.0 -19.6 0.022 0 0 0</pose><geometry><box><size>450.0 0.15 0.002</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')

    # Pedestrian Zebra Crosswalks (行人穿越斑馬線) at intersections
    crosswalks = [
        ("zebra_guangfu_n", 5.0, 0.0, 17.0, 3.2, ROAD_YAW, "光復路口北側斑馬線"),
        ("zebra_gx1_s", 80.0, 0.0, 17.0, 3.0, ROAD_YAW, "關新一街口南側斑馬線"),
        ("zebra_gx1_n", 96.0, 0.0, 17.0, 3.0, ROAD_YAW, "關新一街口北側斑馬線"),
        ("zebra_gx1_e", 88.0, 11.0, 11.0, 2.8, CROSS_YAW, "關新一街東向穿越道"),
        ("zebra_gx2_s", 336.0, 0.0, 17.0, 3.2, ROAD_YAW, "關新二街口南側斑馬線(星巴克)"),
        ("zebra_gx2_n", 353.0, 0.0, 17.0, 3.2, ROAD_YAW, "關新二街口北側斑馬線(日光公園)"),
        ("zebra_gx2_e", 344.5, 11.5, 12.5, 3.0, CROSS_YAW, "關新二街東向穿越道"),
        ("zebra_gxn_s", 479.0, 0.0, 17.0, 3.2, ROAD_YAW, "關新北路口南側斑馬線"),
        ("zebra_gxn_n", 497.0, 0.0, 17.0, 3.2, ROAD_YAW, "關新北路口北側斑馬線"),
        ("zebra_station", 805.0, 0.0, 17.0, 3.5, ROAD_YAW, "新莊車站正門迎賓穿越道")
    ]

    for zid, zs, zo, zw, zl, zy, zdesc in crosswalks:
        ze, zn = pt_road(zs, zo)
        lines.append(f'        <!-- 斑馬線: {zdesc} -->')
        lines.append(f'        <visual name="{zid}"><pose>{ze:.3f} {zn:.3f} 0.024 0 0 {zy:.5f}</pose><geometry><box><size>{zl:.2f} {zw:.2f} 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.98 0.98 0.98 1</diffuse></material></visual>')

    # Motorcycle Waiting Boxes (機車停等區) at Guanxin 2nd St & Guanxin 1st St
    for midx, ms, mo, myaw in [("gx2", 340.0, 4.5, ROAD_YAW), ("gx1", 84.0, 4.5, ROAD_YAW)]:
        mbe, mbn = pt_road(ms, mo)
        lines.append(f'        <!-- 機車停等區: {midx} -->')
        lines.append(f'        <visual name="moto_box_{midx}"><pose>{mbe:.3f} {mbn:.3f} 0.025 0 0 {myaw:.5f}</pose><geometry><box><size>4.5 3.8 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
        lines.append(f'        <visual name="moto_box_inner_{midx}"><pose>{mbe:.3f} {mbn:.3f} 0.026 0 0 {myaw:.5f}</pose><geometry><box><size>4.1 3.4 0.002</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')
        lines.append(f'        <visual name="moto_icon_{midx}"><pose>{mbe:.3f} {mbn:.3f} 0.027 0 0 {myaw:.5f}</pose><geometry><box><size>1.2 1.6 0.002</size></box></geometry><material><ambient>0.95 0.95 0.95 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')

    # ==================== 10. 路邊標準汽車停車格標線 (Parking Stall Decals) ====================
    lines.append('\n        <!-- ===== 10. 路邊標準汽車停車格標線 (2.5m x 5.5m) ===== -->')
    # East side of Guanxin Road (Northbound shoulder: offset +7.75m)
    stall_stations = [
        25.0, 32.0, 39.0, 46.0, 53.0, 60.0,            # 南段 (6格)
        110.0, 117.0, 124.0, 131.0, 138.0, 145.0,       # 中南段 (6格)
        152.0, 159.0, 166.0, 260.0, 267.0, 274.0,       # 寶雅/國泰世華段 (6格)
        365.0, 372.0, 379.0, 386.0, 393.0, 400.0        # 日光公園段 (6格)
    ]

    for pidx, ps in enumerate(stall_stations):
        pe, pn = pt_road(ps, 7.75)
        lines.append(f'        <!-- 停車格 #{pidx+1:02d} (s={ps}m, 東側路肩) -->')
        lines.append(f'        <visual name="stall_frame_{pidx+1:02d}"><pose>{pe:.3f} {pn:.3f} 0.022 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>5.5 2.5 0.0015</size></box></geometry><material><ambient>0.92 0.92 0.92 1</ambient><diffuse>0.95 0.95 0.95 1</diffuse></material></visual>')
        lines.append(f'        <visual name="stall_inner_{pidx+1:02d}"><pose>{pe:.3f} {pn:.3f} 0.023 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>5.2 2.2 0.0015</size></box></geometry><material><ambient>0.22 0.22 0.23 1</ambient><diffuse>0.24 0.24 0.25 1</diffuse></material></visual>')

    # ==================== 11. 防卡死路緣石與人行道系統 (Anti-Stuck Sidewalks & Curb Cuts) ====================
    lines.append('\n        <!-- ===== 11. 防卡死路緣石與人行道系統 (Sidewalks elevated 15cm with Chamfered Curb Cuts) ===== -->')
    # East Sidewalk (width = 5.0m, offset = +11.5m)
    # Segment 1: s = 10 to 78m
    sw1_len = 68.0
    sw1_e, sw1_n = pt_road(10.0 + sw1_len / 2.0, 11.5)
    lines.append(f'        <collision name="sw_e_s1_col"><pose>{sw1_e:.3f} {sw1_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw1_len} 5.0 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_e_s1_vis"><pose>{sw1_e:.3f} {sw1_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw1_len} 5.0 0.15</size></box></geometry><material><ambient>0.74 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.76 1</diffuse></material></visual>')
    # Curb stone strip (offset = +9.08m)
    cw1_e, cw1_n = pt_road(10.0 + sw1_len / 2.0, 9.08)
    lines.append(f'        <visual name="curb_e_s1_vis"><pose>{cw1_e:.3f} {cw1_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw1_len} 0.16 0.15</size></box></geometry><material><ambient>0.55 0.55 0.55 1</ambient><diffuse>0.60 0.60 0.60 1</diffuse></material></visual>')

    # Segment 2: s = 98 to 334m (POYA / McD / Cathay / Starbucks stretch)
    sw2_len = 236.0
    sw2_e, sw2_n = pt_road(98.0 + sw2_len / 2.0, 11.5)
    lines.append(f'        <collision name="sw_e_s2_col"><pose>{sw2_e:.3f} {sw2_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw2_len} 5.0 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_e_s2_vis"><pose>{sw2_e:.3f} {sw2_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw2_len} 5.0 0.15</size></box></geometry><material><ambient>0.74 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.76 1</diffuse></material></visual>')
    cw2_e, cw2_n = pt_road(98.0 + sw2_len / 2.0, 9.08)
    lines.append(f'        <visual name="curb_e_s2_vis"><pose>{cw2_e:.3f} {cw2_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw2_len} 0.16 0.15</size></box></geometry><material><ambient>0.55 0.55 0.55 1</ambient><diffuse>0.60 0.60 0.60 1</diffuse></material></visual>')

    # Segment 3: s = 356 to 476m (Sun Park Sidewalk)
    sw3_len = 120.0
    sw3_e, sw3_n = pt_road(356.0 + sw3_len / 2.0, 11.5)
    lines.append(f'        <collision name="sw_e_s3_col"><pose>{sw3_e:.3f} {sw3_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw3_len} 5.0 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_e_s3_vis"><pose>{sw3_e:.3f} {sw3_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw3_len} 5.0 0.15</size></box></geometry><material><ambient>0.68 0.40 0.30 1</ambient><diffuse>0.72 0.44 0.34 1</diffuse></material></visual>')
    cw3_e, cw3_n = pt_road(356.0 + sw3_len / 2.0, 9.08)
    lines.append(f'        <visual name="curb_e_s3_vis"><pose>{cw3_e:.3f} {cw3_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>{sw3_len} 0.16 0.15</size></box></geometry><material><ambient>0.55 0.55 0.55 1</ambient><diffuse>0.60 0.60 0.60 1</diffuse></material></visual>')

    # West Sidewalk (width = 4.5m, offset = -11.25m)
    # Segment 1: s = 10 to 80m
    wsw1_e, wsw1_n = pt_road(45.0, -11.25)
    lines.append(f'        <collision name="sw_w_s1_col"><pose>{wsw1_e:.3f} {wsw1_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>70.0 4.5 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_w_s1_vis"><pose>{wsw1_e:.3f} {wsw1_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>70.0 4.5 0.15</size></box></geometry><material><ambient>0.74 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.76 1</diffuse></material></visual>')

    # Segment 2: s = 96 to 336m
    wsw2_e, wsw2_n = pt_road(216.0, -11.25)
    lines.append(f'        <collision name="sw_w_s2_col"><pose>{wsw2_e:.3f} {wsw2_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>240.0 4.5 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_w_s2_vis"><pose>{wsw2_e:.3f} {wsw2_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>240.0 4.5 0.15</size></box></geometry><material><ambient>0.74 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.76 1</diffuse></material></visual>')

    # Segment 3: s = 352 to 820m (towards station)
    wsw3_e, wsw3_n = pt_road(586.0, -11.25)
    lines.append(f'        <collision name="sw_w_s3_col"><pose>{wsw3_e:.3f} {wsw3_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>468.0 4.5 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="sw_w_s3_vis"><pose>{wsw3_e:.3f} {wsw3_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>468.0 4.5 0.15</size></box></geometry><material><ambient>0.74 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.76 1</diffuse></material></visual>')

    # Curb Cuts / Ramps (無障礙與出入口倒角緩坡 - 防輪胎卡死)
    ramps = [
        ("ramp_gx1_e", 88.0, 9.0, "關新一街東路緣切口"),
        ("ramp_gx1_w", 88.0, -9.0, "關新一街西路緣切口"),
        ("ramp_gx2_e", 344.5, 9.0, "關新二街東路緣切口"),
        ("ramp_gx2_w", 344.5, -9.0, "關新二街西路緣切口"),
        ("ramp_gxn_e", 488.0, 9.0, "關新北路東路緣切口"),
        ("ramp_gxn_w", 488.0, -9.0, "關新北路西路緣切口")
    ]
    for rid, rs, ro, rdesc in ramps:
        re, rn = pt_road(rs, ro)
        lines.append(f'        <!-- 緩坡切口: {rdesc} -->')
        lines.append(f'        <collision name="{rid}_col"><pose>{re:.3f} {rn:.3f} 0.02 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>12.0 1.2 0.04</size></box></geometry><surface><friction><ode><mu>0.9</mu><mu2>0.9</mu2></ode></friction></surface></collision>')
        lines.append(f'        <visual name="{rid}_vis"><pose>{re:.3f} {rn:.3f} 0.02 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>12.0 1.2 0.04</size></box></geometry><material><ambient>0.35 0.35 0.36 1</ambient><diffuse>0.40 0.40 0.42 1</diffuse></material></visual>')

    lines.append('      </link>')
    lines.append('    </model>')

    # ==================== 12. 路邊智慧停車柱模組佈建 (Smart Parking Meter Poles) ====================
    lines.append('\n    <!-- ==================== 路邊智慧停車柱系統 (Smart Parking Meter Poles) ==================== -->')
    lines.append('    <!-- 沿關新路東側人行道路緣 (offset = +9.35m)，車牌辨識相機朝向車位 -->')
    # Pole rotation: pole needs its camera (local +Y) pointing toward the parking space (towards centerline, which is -U_PERP).
    # Since U_PERP is at yaw = CROSS_YAW (-12.93 deg), pointing towards centerline is yaw = CROSS_YAW + 180 deg = 167.069 deg = 2.9159 rad.
    pole_yaw = CROSS_YAW + math.pi
    for pidx, ps in enumerate(stall_stations):
        pe, pn = pt_road(ps, 9.35)
        pole_name = f'smart_parking_pole_{pidx+1:02d}'
        lines.append(f'    <include>')
        lines.append(f'      <name>{pole_name}</name>')
        lines.append(f'      <uri>model://smart_parking_meter_pole</uri>')
        lines.append(f'      <pose>{pe:.3f} {pn:.3f} 0.15 0 0 {pole_yaw:.5f}</pose>')
        lines.append(f'    </include>')

    return '\n'.join(lines)


if __name__ == '__main__':
    print(f"Guanxin Road Corridor Angle: Bearing={BEARING_DEG:.2f} deg, Yaw={ROAD_YAW:.4f} rad")
    print(f"Perpendicular Angle: Yaw={CROSS_YAW:.4f} rad")
    print(f"Direction Vector Road: {U_ROAD}")
    print(f"Direction Vector Perp: {U_PERP}")
    sdf_block = generate_road_network_sdf()
    print(f"Generated {len(sdf_block.splitlines())} lines of SDF code.")
