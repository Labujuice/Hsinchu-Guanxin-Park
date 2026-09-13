#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Phase 3 Landmarks (TRA Xin-Zhuang Station, Railway Viaduct, Sun Park Landscape) for Guanxin World SDF.
Author: Autonomous Robotics & Simulation Team
Project: Guanxin Road Digital Twin Simulation
"""

import math

BEARING_DEG = 12.930438
BEARING_RAD = math.radians(BEARING_DEG)
ROAD_YAW = math.radians(90.0 - BEARING_DEG)   # 1.345116 rad
CROSS_YAW = ROAD_YAW - math.radians(90.0)     # -0.225678 rad

U_ROAD = (math.sin(BEARING_RAD), math.cos(BEARING_RAD))   # (0.22376, 0.97464)
U_PERP = (math.cos(BEARING_RAD), -math.sin(BEARING_RAD))  # (0.97464, -0.22376)


def pt_road(s, offset_perp=0.0):
    """Calculates ENU (E, N) coordinate given distance along Guanxin Road (s) and perpendicular offset."""
    e = s * U_ROAD[0] + offset_perp * U_PERP[0]
    n = s * U_ROAD[1] + offset_perp * U_PERP[1]
    return e, n


def generate_phase3_sdf():
    lines = []
    lines.append('    <!-- ==================== Phase 3: 重點交通與公共休閒地標建模 ==================== -->')
    lines.append('    <!-- 涵蓋: 台鐵新莊車站大樓、高架鐵路橋梁橋墩(淨空>5.2m)、日光公園全區景觀與遊憩設施 -->')

    # ==================== 1. 台鐵高架鐵路橋樑與橋墩 (Railway Viaduct across Guanxin Rd) ====================
    # At s = 803.7m (across Guanxin Rd), crossing angle = CROSS_YAW
    ve, vn = pt_road(803.7, 0.0)
    lines.append('\n    <!-- 1. 台鐵六家/內灣線高架鐵路跨街橋樑與混凝土橋墩 (橋下淨空 5.4m >= 4.8m) -->')
    lines.append('    <include>')
    lines.append('      <name>railway_viaduct</name>')
    lines.append('      <uri>model://railway_viaduct</uri>')
    lines.append(f'      <pose>{ve:.3f} {vn:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # ==================== 2. 台鐵新莊車站大樓 (TRA Xin-Zhuang Station) ====================
    # At GCP 5: [E: 184.55, N: 803.70], oriented along railway corridor (CROSS_YAW)
    # The station sits slightly on the east side of the viaduct crossing
    se, sn = pt_road(803.7, 26.0)
    lines.append('\n    <!-- 2. 台鐵新莊車站大樓 (GCP 5: 二層挑高高架車站、鋼構雨棚月台、採光玻璃帷幕與正門發光招牌) -->')
    lines.append('    <include>')
    lines.append('      <name>xinzhuang_station</name>')
    lines.append('      <uri>model://xinzhuang_station</uri>')
    lines.append(f'      <pose>{se:.3f} {sn:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # Station Front Plaza & Taxi Loop (新莊車站前廣場、計程車排班彎道與行人避車道)
    plz_e, plz_n = pt_road(785.0, 20.0)
    lines.append('\n    <!-- 新莊車站前迎賓廣場與計程車排班避車道 (Station Plaza & Taxi Drop-off Bay) -->')
    lines.append('    <model name="xinzhuang_station_plaza">')
    lines.append('      <static>true</static>')
    lines.append('      <link name="plaza_link">')
    # Plaza granite paver deck (width 26m, length 42m, height 0.15m)
    lines.append(f'        <collision name="plaza_deck_col"><pose>{plz_e:.3f} {plz_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>42.0 26.0 0.15</size></box></geometry></collision>')
    lines.append(f'        <visual name="plaza_deck_vis"><pose>{plz_e:.3f} {plz_n:.3f} 0.075 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>42.0 26.0 0.15</size></box></geometry><material><ambient>0.72 0.74 0.76 1</ambient><diffuse>0.78 0.80 0.82 1</diffuse></material></visual>')
    # Plaza ornamental planter beds & benches
    plz_b1_e, plz_b1_n = pt_road(775.0, 14.0)
    lines.append(f'        <visual name="plaza_planter1"><pose>{plz_b1_e:.3f} {plz_b1_n:.3f} 0.35 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>8.0 2.2 0.50</size></box></geometry><material><ambient>0.45 0.48 0.5 1</ambient><diffuse>0.52 0.55 0.58 1</diffuse></material></visual>')
    lines.append(f'        <visual name="plaza_shrub1"><pose>{plz_b1_e:.3f} {plz_b1_n:.3f} 0.80 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>7.6 1.8 0.45</size></box></geometry><material><ambient>0.15 0.48 0.18 1</ambient><diffuse>0.20 0.55 0.22 1</diffuse></material></visual>')
    plz_b2_e, plz_b2_n = pt_road(795.0, 14.0)
    lines.append(f'        <visual name="plaza_planter2"><pose>{plz_b2_e:.3f} {plz_b2_n:.3f} 0.35 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>8.0 2.2 0.50</size></box></geometry><material><ambient>0.45 0.48 0.5 1</ambient><diffuse>0.52 0.55 0.58 1</diffuse></material></visual>')
    lines.append(f'        <visual name="plaza_shrub2"><pose>{plz_b2_e:.3f} {plz_b2_n:.3f} 0.80 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>7.6 1.8 0.45</size></box></geometry><material><ambient>0.15 0.48 0.18 1</ambient><diffuse>0.20 0.55 0.22 1</diffuse></material></visual>')
    # Station entrance flagpole triplet (車站門前三連旗桿)
    flg_e, flg_n = pt_road(788.0, 11.5)
    lines.append(f'        <visual name="flagpole1"><pose>{flg_e:.3f} {flg_n:.3f} 4.0 0 0 0</pose><geometry><cylinder><radius>0.05</radius><length>8.0</length></cylinder></geometry><material><ambient>0.8 0.8 0.85 1</ambient><diffuse>0.9 0.9 0.95 1</diffuse></material></visual>')
    lines.append('      </link>')
    lines.append('    </model>')

    # ==================== 3. 關新公園（日光公園）全區景觀深化 ====================
    # Park dimensions: 120m (along Guanxin Rd, s=356 to 476) x 91m (perpendicular offset=14 to 105)
    # Park center: s = 416m, offset = 59.5m
    pk_c_e, pk_c_n = pt_road(416.0, 59.5)
    lines.append('\n    <!-- 3. 關新公園 / 日光公園全區景觀系統 (120m x 91m, GCP 4, 洗石子圍牆, 大草坪, 景觀涼亭, 景觀公廁, 兒童遊憩與體健區) -->')
    lines.append('    <model name="sun_park_landscape">')
    lines.append('      <static>true</static>')
    lines.append('      <link name="park_link">')

    # (A) 公園大底與外圍低矮洗石子花台圍牆 (Perimeter Washed-Stone Planter Wall)
    # Park base turf (120m x 91m, raised 10cm above asphalt)
    lines.append(f'        <!-- 公園基座微地形草皮大底 -->')
    lines.append(f'        <collision name="park_base_col"><pose>{pk_c_e:.3f} {pk_c_n:.3f} 0.05 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>120.0 91.0 0.10</size></box></geometry></collision>')
    lines.append(f'        <visual name="park_base_vis"><pose>{pk_c_e:.3f} {pk_c_n:.3f} 0.05 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>120.0 91.0 0.10</size></box></geometry><material><ambient>0.18 0.50 0.18 1</ambient><diffuse>0.22 0.58 0.22 1</diffuse></material></visual>')

    # 4邊低矮洗石子花台圍牆 (高 0.45m, 寬 0.6m)
    # West wall (facing Guanxin Rd, offset = +14.2m)
    w_wall_e, w_wall_n = pt_road(416.0, 14.3)
    lines.append(f'        <collision name="wall_w_col"><pose>{w_wall_e:.3f} {w_wall_n:.3f} 0.25 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>116.0 0.6 0.50</size></box></geometry></collision>')
    lines.append(f'        <visual name="wall_w_vis"><pose>{w_wall_e:.3f} {w_wall_n:.3f} 0.25 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>116.0 0.6 0.50</size></box></geometry><material><ambient>0.65 0.62 0.58 1</ambient><diffuse>0.72 0.68 0.64 1</diffuse></material></visual>')
    # East wall (facing Guanxin East Rd, offset = +104.7m)
    e_wall_e, e_wall_n = pt_road(416.0, 104.7)
    lines.append(f'        <collision name="wall_e_col"><pose>{e_wall_e:.3f} {e_wall_n:.3f} 0.25 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>116.0 0.6 0.50</size></box></geometry></collision>')
    lines.append(f'        <visual name="wall_e_vis"><pose>{e_wall_e:.3f} {e_wall_n:.3f} 0.25 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>116.0 0.6 0.50</size></box></geometry><material><ambient>0.65 0.62 0.58 1</ambient><diffuse>0.72 0.68 0.64 1</diffuse></material></visual>')
    # South wall (facing Guanxin 2nd St, s = 356.3m)
    s_wall_e, s_wall_n = pt_road(356.3, 59.5)
    lines.append(f'        <collision name="wall_s_col"><pose>{s_wall_e:.3f} {s_wall_n:.3f} 0.25 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>88.0 0.6 0.50</size></box></geometry></collision>')
    lines.append(f'        <visual name="wall_s_vis"><pose>{s_wall_e:.3f} {s_wall_n:.3f} 0.25 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>88.0 0.6 0.50</size></box></geometry><material><ambient>0.65 0.62 0.58 1</ambient><diffuse>0.72 0.68 0.64 1</diffuse></material></visual>')
    # North wall (facing Guanxin North Rd, s = 475.7m)
    n_wall_e, n_wall_n = pt_road(475.7, 59.5)
    lines.append(f'        <collision name="wall_n_col"><pose>{n_wall_e:.3f} {n_wall_n:.3f} 0.25 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>88.0 0.6 0.50</size></box></geometry></collision>')
    lines.append(f'        <visual name="wall_n_vis"><pose>{n_wall_e:.3f} {n_wall_n:.3f} 0.25 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>88.0 0.6 0.50</size></box></geometry><material><ambient>0.65 0.62 0.58 1</ambient><diffuse>0.72 0.68 0.64 1</diffuse></material></visual>')

    # (B) 公園西南角地標名牌碑 (Southwest Entrance Park Monument - 星巴克斜對角)
    mon_e, mon_n = pt_road(358.0, 16.5)
    lines.append(f'        <!-- 西南角入口「關新公園」石牌標誌 (Park Stone Monument) -->')
    lines.append(f'        <visual name="monument_base"><pose>{mon_e:.3f} {mon_n:.3f} 0.45 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>3.6 0.8 0.90</size></box></geometry><material><ambient>0.35 0.35 0.38 1</ambient><diffuse>0.42 0.42 0.45 1</diffuse></material></visual>')
    lines.append(f'        <visual name="monument_plaque"><pose>{mon_e:.3f} {mon_n:.3f} 0.50 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>3.2 0.85 0.55</size></box></geometry><material><ambient>0.85 0.75 0.1 1</ambient><diffuse>0.92 0.82 0.12 1</diffuse><emissive>0.3 0.25 0.05 1</emissive></material></visual>')

    # (C) 內部休閒步道系統 (Interconnecting Walkways: 環園步道與中央主穿越步道)
    # Loop walkway segments (width 2.8m, red paver brick)
    lines.append('        <!-- 公園外環紅磚休閒散步道 (Outer Loop Walkway) -->')
    w_walk_e, w_walk_n = pt_road(416.0, 18.0)
    lines.append(f'        <visual name="walk_w"><pose>{w_walk_e:.3f} {w_walk_n:.3f} 0.105 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>110.0 2.8 0.01</size></box></geometry><material><ambient>0.62 0.35 0.26 1</ambient><diffuse>0.68 0.40 0.30 1</diffuse></material></visual>')
    e_walk_e, e_walk_n = pt_road(416.0, 101.0)
    lines.append(f'        <visual name="walk_e"><pose>{e_walk_e:.3f} {e_walk_n:.3f} 0.105 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>110.0 2.8 0.01</size></box></geometry><material><ambient>0.62 0.35 0.26 1</ambient><diffuse>0.68 0.40 0.30 1</diffuse></material></visual>')
    s_walk_e, s_walk_n = pt_road(360.0, 59.5)
    lines.append(f'        <visual name="walk_s"><pose>{s_walk_e:.3f} {s_walk_n:.3f} 0.105 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>82.0 2.8 0.01</size></box></geometry><material><ambient>0.62 0.35 0.26 1</ambient><diffuse>0.68 0.40 0.30 1</diffuse></material></visual>')
    n_walk_e, n_walk_n = pt_road(472.0, 59.5)
    lines.append(f'        <visual name="walk_n"><pose>{n_walk_e:.3f} {n_walk_n:.3f} 0.105 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>82.0 2.8 0.01</size></box></geometry><material><ambient>0.62 0.35 0.26 1</ambient><diffuse>0.68 0.40 0.30 1</diffuse></material></visual>')

    # Central diagonal walkway (from southwest to northeast, 3.2m wide)
    lines.append('        <!-- 公園中央貫通林蔭步道 (Central Arterial Walkway) -->')
    c_walk_e, c_walk_n = pt_road(416.0, 59.5)
    lines.append(f'        <visual name="walk_cross"><pose>{c_walk_e:.3f} {c_walk_n:.3f} 0.106 0 0 {CROSS_YAW:.5f}</pose><geometry><box><size>80.0 3.2 0.01</size></box></geometry><material><ambient>0.72 0.70 0.65 1</ambient><diffuse>0.78 0.75 0.70 1</diffuse></material></visual>')

    # (D) 中央陽光大草坪與地形起伏微丘 (Central Sun Lawn & Gentle Topo Mounds)
    lawn_e, lawn_n = pt_road(416.0, 62.0)
    lines.append('        <!-- 公園中央開闊陽光大草坪 (Central Sun Lawn) -->')
    lines.append(f'        <visual name="main_sun_lawn"><pose>{lawn_e:.3f} {lawn_n:.3f} 0.108 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>75.0 52.0 0.01</size></box></geometry><material><ambient>0.15 0.55 0.18 1</ambient><diffuse>0.20 0.62 0.22 1</diffuse></material></visual>')

    # 微丘起伏 1 (Mound 1 - 東南草坡)
    m1_e, m1_n = pt_road(385.0, 75.0)
    lines.append(f'        <visual name="topo_mound1"><pose>{m1_e:.3f} {m1_n:.3f} 0.45 0 0 {ROAD_YAW:.5f}</pose><geometry><cylinder><radius>12.0</radius><length>0.7</length></cylinder></geometry><material><ambient>0.18 0.58 0.20 1</ambient><diffuse>0.22 0.65 0.25 1</diffuse></material></visual>')
    # 微丘起伏 2 (Mound 2 - 西北休憩微丘)
    m2_e, m2_n = pt_road(450.0, 42.0)
    lines.append(f'        <visual name="topo_mound2"><pose>{m2_e:.3f} {m2_n:.3f} 0.40 0 0 {ROAD_YAW:.5f}</pose><geometry><cylinder><radius>9.5</radius><length>0.6</length></cylinder></geometry><material><ambient>0.18 0.58 0.20 1</ambient><diffuse>0.22 0.65 0.25 1</diffuse></material></visual>')

    # (E) 現代景觀休憩涼亭 (Rest Pavilion at GCP 4: s = 440m, offset = 68m)
    # Wooden slat trellis ceiling, steel columns, stone benches
    pav_e, pav_n = pt_road(440.0, 68.0)
    lines.append(f'\n        <!-- 現代休閒景觀涼亭 (GCP 4 休憩核心: 挑高鋼構木紋百葉亭) -->')
    lines.append(f'        <collision name="pav_base_col"><pose>{pav_e:.3f} {pav_n:.3f} 0.15 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>10.0 8.0 0.3</size></box></geometry></collision>')
    lines.append(f'        <visual name="pav_base_vis"><pose>{pav_e:.3f} {pav_n:.3f} 0.15 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>10.0 8.0 0.3</size></box></geometry><material><ambient>0.5 0.48 0.45 1</ambient><diffuse>0.58 0.55 0.52 1</diffuse></material></visual>')
    # Pavilion roof canopy
    lines.append(f'        <collision name="pav_roof_col"><pose>{pav_e:.3f} {pav_n:.3f} 3.4 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>11.0 9.0 0.3</size></box></geometry></collision>')
    lines.append(f'        <visual name="pav_roof_vis"><pose>{pav_e:.3f} {pav_n:.3f} 3.4 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>11.0 9.0 0.3</size></box></geometry><material><ambient>0.35 0.25 0.15 1</ambient><diffuse>0.45 0.32 0.20 1</diffuse></material></visual>')
    # 4 Steel pillars
    for cdx, cdy in [(-4.2, -3.2), (4.2, -3.2), (-4.2, 3.2), (4.2, 3.2)]:
        lines.append(f'        <visual name="pav_col_{cdx}_{cdy}"><pose>{pav_e + cdx:.3f} {pav_n + cdy:.3f} 1.7 0 0 0</pose><geometry><cylinder><radius>0.15</radius><length>3.1</length></cylinder></geometry><material><ambient>0.22 0.24 0.26 1</ambient><diffuse>0.28 0.30 0.32 1</diffuse></material></visual>')
    # Central teak benches inside pavilion
    lines.append(f'        <visual name="pav_bench1"><pose>{pav_e:.3f} {pav_n - 1.8:.3f} 0.45 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>6.0 0.6 0.45</size></box></geometry><material><ambient>0.48 0.30 0.15 1</ambient><diffuse>0.55 0.36 0.20 1</diffuse></material></visual>')
    lines.append(f'        <visual name="pav_bench2"><pose>{pav_e:.3f} {pav_n + 1.8:.3f} 0.45 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>6.0 0.6 0.45</size></box></geometry><material><ambient>0.48 0.30 0.15 1</ambient><diffuse>0.55 0.36 0.20 1</diffuse></material></visual>')

    # (F) 現代公園景觀公廁 (Public Restroom Facility at Northeast: s = 460m, offset = 92m)
    rr_e, rr_n = pt_road(460.0, 92.0)
    lines.append(f'\n        <!-- 現代公園景觀公廁 (Public Restroom - 清水模與木紋隔柵建築) -->')
    lines.append(f'        <collision name="restroom_col"><pose>{rr_e:.3f} {rr_n:.3f} 2.0 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>12.0 7.5 4.0</size></box></geometry></collision>')
    lines.append(f'        <visual name="restroom_vis"><pose>{rr_e:.3f} {rr_n:.3f} 2.0 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>12.0 7.5 4.0</size></box></geometry><material><ambient>0.72 0.74 0.72 1</ambient><diffuse>0.78 0.80 0.78 1</diffuse></material></visual>')
    # Restroom cantilevered flat roof
    lines.append(f'        <visual name="restroom_roof"><pose>{rr_e:.3f} {rr_n:.3f} 4.15 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>13.2 8.5 0.3</size></box></geometry><material><ambient>0.28 0.30 0.32 1</ambient><diffuse>0.34 0.36 0.38 1</diffuse></material></visual>')
    # Restroom entry privacy screen (木紋格柵防視屏風)
    lines.append(f'        <visual name="restroom_screen"><pose>{rr_e - 1.5:.3f} {rr_n - 4.2:.3f} 1.5 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>5.0 0.15 3.0</size></box></geometry><material><ambient>0.45 0.28 0.15 1</ambient><diffuse>0.52 0.34 0.18 1</diffuse></material></visual>')

    # (G) 兒童遊樂場安全地墊區 (Playground Rubber Safety Mat Zone around Slide: s = 410m, offset = 32m)
    mat_e, mat_n = pt_road(410.0, 32.0)
    lines.append(f'\n        <!-- 兒童遊樂場吸震彈性安全地墊區 (Rubber Safety Mat) -->')
    lines.append(f'        <visual name="play_mat_blue"><pose>{mat_e:.3f} {mat_n:.3f} 0.108 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>24.0 18.0 0.015</size></box></geometry><material><ambient>0.12 0.40 0.70 1</ambient><diffuse>0.16 0.50 0.85 1</diffuse></material></visual>')
    lines.append(f'        <visual name="play_mat_yellow_ring"><pose>{mat_e:.3f} {mat_n:.3f} 0.110 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>20.0 14.0 0.015</size></box></geometry><material><ambient>0.85 0.70 0.10 1</ambient><diffuse>0.92 0.78 0.12 1</diffuse></material></visual>')

    # 兒童盪鞦韆組 (Double Swing Set: s = 418m, offset = 38m)
    swg_e, swg_n = pt_road(418.0, 38.0)
    lines.append(f'        <!-- 雙人盪鞦韆組 (Double Swing Frame) -->')
    lines.append(f'        <collision name="swing_frame_col"><pose>{swg_e:.3f} {swg_n:.3f} 1.6 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>4.5 1.8 3.2</size></box></geometry></collision>')
    lines.append(f'        <visual name="swing_beam"><pose>{swg_e:.3f} {swg_n:.3f} 3.1 0 0 {ROAD_YAW:.5f}</pose><geometry><cylinder><radius>0.08</radius><length>4.5</length></cylinder></geometry><material><ambient>0.9 0.2 0.2 1</ambient><diffuse>0.95 0.25 0.25 1</diffuse></material></visual>')
    lines.append(f'        <visual name="swing_seat1"><pose>{swg_e - 1.1:.3f} {swg_n:.3f} 0.5 0 0 0</pose><geometry><box><size>0.6 0.25 0.06</size></box></geometry><material><ambient>0.1 0.1 0.1 1</ambient><diffuse>0.2 0.2 0.2 1</diffuse></material></visual>')
    lines.append(f'        <visual name="swing_seat2"><pose>{swg_e + 1.1:.3f} {swg_n:.3f} 0.5 0 0 0</pose><geometry><box><size>0.6 0.25 0.06</size></box></geometry><material><ambient>0.1 0.1 0.1 1</ambient><diffuse>0.2 0.2 0.2 1</diffuse></material></visual>')

    # (H) 體健運動設施區 (Adult Fitness Station: s = 380m, offset = 32m)
    fit_e, fit_n = pt_road(380.0, 32.0)
    lines.append(f'\n        <!-- 社區體健設施區 (Fitness Equipment Zone: 雙人漫步機與轉腰器) -->')
    lines.append(f'        <visual name="fit_mat"><pose>{fit_e:.3f} {fit_n:.3f} 0.108 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>14.0 10.0 0.015</size></box></geometry><material><ambient>0.20 0.45 0.25 1</ambient><diffuse>0.25 0.55 0.30 1</diffuse></material></visual>')
    lines.append(f'        <visual name="walker_vis"><pose>{fit_e:.3f} {fit_n:.3f} 0.75 0 0 {ROAD_YAW:.5f}</pose><geometry><box><size>1.6 1.2 1.4</size></box></geometry><material><ambient>0.85 0.65 0.05 1</ambient><diffuse>0.92 0.72 0.08 1</diffuse></material></visual>')
    lines.append(f'        <visual name="twister_vis"><pose>{fit_e + 2.5:.3f} {fit_n:.3f} 0.65 0 0 0</pose><geometry><cylinder><radius>0.5</radius><length>1.2</length></cylinder></geometry><material><ambient>0.2 0.5 0.7 1</ambient><diffuse>0.25 0.6 0.8 1</diffuse></material></visual>')

    lines.append('      </link>')
    lines.append('    </model>')

    # ==================== 4. 標誌性磨石子大溜滑梯 (Terrazzo Giant Slide) ====================
    # Placed in the rubber safety mat zone at s = 406m, offset = 30m
    # Slide orientation: sliding direction faces toward park central lawn
    slide_e, slide_n = pt_road(406.0, 30.0)
    slide_yaw = ROAD_YAW + math.pi / 2.0  # faces into the park (+U_PERP)
    lines.append('\n    <!-- 4. 標誌性地景：磨石子大溜滑梯 (Terrazzo Giant Slide - 依實測座標錨定於日光公園遊戲區) -->')
    lines.append('    <include>')
    lines.append('      <name>terrazzo_slide</name>')
    lines.append('      <uri>model://terrazzo_slide</uri>')
    lines.append(f'      <pose>{slide_e:.3f} {slide_n:.3f} 0.10 0 0 {slide_yaw:.5f}</pose>')
    lines.append('    </include>')

    return '\n'.join(lines)


if __name__ == '__main__':
    sdf_block = generate_phase3_sdf()
    print(f"Generated {len(sdf_block.splitlines())} lines of Phase 3 SDF.")
