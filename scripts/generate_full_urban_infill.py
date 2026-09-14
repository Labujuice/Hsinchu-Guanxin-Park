#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full Urban Infill & Landscape Generation Script for Guanxin Digital Twin
Author: Autonomous Robotics & Simulation Team
"""

import os
import sys
import math
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(REPO_DIR, "src", "guanxin_sim", "models")
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")
INSTALL_WORLD_PATH = os.path.join(REPO_DIR, "install", "guanxin_sim", "share", "guanxin_sim", "worlds", "guanxin.sdf")

# Coordinate Constants
BEARING_DEG = 12.930438
BEARING_RAD = math.radians(BEARING_DEG)
ROAD_YAW = math.radians(90.0 - BEARING_DEG)     # 1.345116 rad = 77.0696 deg
CROSS_YAW = ROAD_YAW - math.radians(90.0)       # -0.225678 rad = -12.9304 deg
WEST_BLDG_YAW = CROSS_YAW - math.radians(90.0)   # -1.796474 rad = -102.9304 deg

U_ROAD = (math.sin(BEARING_RAD), math.cos(BEARING_RAD))
U_PERP = (math.cos(BEARING_RAD), -math.sin(BEARING_RAD))

def pt_road(s, perp):
    return s * U_ROAD[0] + perp * U_PERP[0], s * U_ROAD[1] + perp * U_PERP[1]

def save_model(model_name, description, sdf_content):
    m_dir = os.path.join(MODELS_DIR, model_name)
    os.makedirs(m_dir, exist_ok=True)
    
    config_path = os.path.join(m_dir, "model.config")
    config_content = f"""<?xml version="1.0"?>
<model>
  <name>{model_name}</name>
  <version>1.0</version>
  <sdf version="1.8">model.sdf</sdf>
  <author>
    <name>Robotics &amp; Simulation Specialist</name>
    <email>robotics@guanxin.sim</email>
  </author>
  <description>
    {description}
  </description>
</model>
"""
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_content)
        
    sdf_path = os.path.join(m_dir, "model.sdf")
    with open(sdf_path, "w", encoding="utf-8") as f:
        f.write(sdf_content)
    print(f"Created model: {model_name}")

# ==============================================================================
# Model 1: 超級大銅製裝置藝術 -「風之冠．無限科技之環」 (Monumental Bronze Public Art)
# ==============================================================================
def create_giant_bronze_sculpture_monument():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="giant_bronze_sculpture_monument">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="bronze_monument_link">')
    
    # 物理碰撞剛體 (三層花崗岩台座與中央青銅基座，供機器人與車輛實體防護)
    lines.append('      <!-- 物理碰撞剛體 (三層花崗岩台座與中央基柱) -->')
    lines.append('      <collision name="base_step1_col"><pose>0 0 0.2 0 0 0</pose><geometry><box><size>26.0 26.0 0.4</size></box></geometry></collision>')
    lines.append('      <collision name="base_step2_col"><pose>0 0 0.6 0 0 0</pose><geometry><box><size>20.0 20.0 0.4</size></box></geometry></collision>')
    lines.append('      <collision name="base_step3_col"><pose>0 0 1.0 0 0 0</pose><geometry><box><size>15.0 15.0 0.4</size></box></geometry></collision>')
    lines.append('      <collision name="core_pedestal_col"><pose>0 0 2.5 0 0 0</pose><geometry><box><size>6.4 6.4 2.6</size></box></geometry></collision>')
    lines.append('      <collision name="spire_trunk_col"><pose>0 0 6.5 0 0 0</pose><geometry><cylinder><radius>2.2</radius><length>6.0</length></cylinder></geometry></collision>')
    
    # 1. 三層花崗岩雕塑基座 (Multi-tiered Granite Plaza Steps)
    lines.append('      <!-- 1. 三層八角同心花崗岩親水廣場基座 -->')
    lines.append('      <visual name="base_step1_vis"><pose>0 0 0.2 0 0 0</pose><geometry><box><size>26.0 26.0 0.4</size></box></geometry><material><ambient>0.72 0.70 0.68 1</ambient><diffuse>0.78 0.76 0.74 1</diffuse><specular>0.3 0.3 0.3 1</specular></material></visual>')
    lines.append('      <visual name="base_step2_vis"><pose>0 0 0.6 0 0 0</pose><geometry><box><size>20.0 20.0 0.4</size></box></geometry><material><ambient>0.45 0.45 0.48 1</ambient><diffuse>0.52 0.52 0.55 1</diffuse><specular>0.4 0.4 0.4 1</specular></material></visual>')
    lines.append('      <visual name="base_step3_vis"><pose>0 0 1.0 0 0 0</pose><geometry><box><size>15.0 15.0 0.4</size></box></geometry><material><ambient>0.25 0.25 0.28 1</ambient><diffuse>0.30 0.30 0.34 1</diffuse><specular>0.6 0.6 0.6 1</specular></material></visual>')
    lines.append('      <!-- 親水倒影鏡面水池池水 -->')
    lines.append('      <visual name="reflecting_pool"><pose>0 0 1.21 0 0 0</pose><geometry><box><size>13.8 13.8 0.01</size></box></geometry><material><ambient>0.10 0.28 0.38 0.92</ambient><diffuse>0.15 0.38 0.52 0.92</diffuse><specular>0.95 0.98 1.0 1</specular></material></visual>')
    
    # 2. 中央重型鑄造青銅基柱 (Octagonal Heavy Cast Bronze Pedestal)
    lines.append('      <!-- 2. 中央重型鑄造青銅基柱與銘刻銘板 -->')
    lines.append('      <visual name="bronze_core_pedestal"><pose>0 0 2.5 0 0 0</pose><geometry><box><size>6.4 6.4 2.6</size></box></geometry><material><ambient>0.32 0.20 0.10 1</ambient><diffuse>0.48 0.32 0.16 1</diffuse><specular>0.75 0.55 0.25 1</specular></material></visual>')
    lines.append('      <visual name="pedestal_cornice"><pose>0 0 3.85 0 0 0</pose><geometry><box><size>7.2 7.2 0.3</size></box></geometry><material><ambient>0.40 0.26 0.12 1</ambient><diffuse>0.58 0.40 0.20 1</diffuse><specular>0.85 0.65 0.30 1</specular></material></visual>')
    
    # 四方青銅浮雕歷史銘板 (4 Cardinal Bronze Dedication Plaques)
    lines.append('      <visual name="plaque_s"><pose>0 -3.25 2.5 0 0 0</pose><geometry><box><size>4.8 0.12 1.5</size></box></geometry><material><ambient>0.55 0.38 0.15 1</ambient><diffuse>0.75 0.55 0.22 1</diffuse><specular>0.9 0.7 0.3 1</specular></material></visual>')
    lines.append('      <visual name="plaque_n"><pose>0 3.25 2.5 0 0 0</pose><geometry><box><size>4.8 0.12 1.5</size></box></geometry><material><ambient>0.55 0.38 0.15 1</ambient><diffuse>0.75 0.55 0.22 1</diffuse><specular>0.9 0.7 0.3 1</specular></material></visual>')
    lines.append('      <visual name="plaque_e"><pose>3.25 0 2.5 0 0 0</pose><geometry><box><size>0.12 4.8 1.5</size></box></geometry><material><ambient>0.55 0.38 0.15 1</ambient><diffuse>0.75 0.55 0.22 1</diffuse><specular>0.9 0.7 0.3 1</specular></material></visual>')
    lines.append('      <visual name="plaque_w"><pose>-3.25 0 2.5 0 0 0</pose><geometry><box><size>0.12 4.8 1.5</size></box></geometry><material><ambient>0.55 0.38 0.15 1</ambient><diffuse>0.75 0.55 0.22 1</diffuse><specular>0.9 0.7 0.3 1</specular></material></visual>')
    
    # 3. 雙向飛旋青銅神翼與螺旋上升主體 (Monumental Soaring Bronze Twin Spires, 19.5m tall!)
    lines.append('      <!-- 3. 超級雙曲青銅神翼 (19.5m 壯麗青銅主羽翼) -->')
    # 翅膀 A (東南向巨型羽翼)
    lines.append('      <visual name="wing_a_lower"><pose>1.2 -0.8 6.5 0.25 0.35 0.5</pose><geometry><box><size>1.6 0.8 6.5</size></box></geometry><material><ambient>0.36 0.22 0.12 1</ambient><diffuse>0.56 0.38 0.20 1</diffuse><specular>0.85 0.65 0.30 1</specular></material></visual>')
    lines.append('      <visual name="wing_a_mid"><pose>2.8 -1.8 11.2 0.40 0.50 0.6</pose><geometry><box><size>1.3 0.6 6.0</size></box></geometry><material><ambient>0.42 0.28 0.14 1</ambient><diffuse>0.62 0.44 0.22 1</diffuse><specular>0.90 0.70 0.35 1</specular></material></visual>')
    lines.append('      <visual name="wing_a_tip"><pose>4.2 -2.6 15.8 0.55 0.65 0.7</pose><geometry><box><size>0.9 0.35 5.5</size></box></geometry><material><ambient>0.48 0.32 0.16 1</ambient><diffuse>0.70 0.50 0.25 1</diffuse><specular>0.95 0.75 0.40 1</specular></material></visual>')
    lines.append('      <visual name="wing_a_crest"><pose>5.2 -3.2 19.2 0.70 0.80 0.8</pose><geometry><box><size>0.5 0.2 3.0</size></box></geometry><material><ambient>0.58 0.42 0.18 1</ambient><diffuse>0.82 0.62 0.28 1</diffuse><specular>1.0 0.85 0.50 1</specular></material></visual>')
    
    # 翅膀 B (西北向巨型羽翼)
    lines.append('      <!-- 翅膀 B (西北向巨型羽翼) -->')
    lines.append('      <visual name="wing_b_lower"><pose>-1.2 0.8 6.5 -0.25 -0.35 0.5</pose><geometry><box><size>1.6 0.8 6.5</size></box></geometry><material><ambient>0.36 0.22 0.12 1</ambient><diffuse>0.56 0.38 0.20 1</diffuse><specular>0.85 0.65 0.30 1</specular></material></visual>')
    lines.append('      <visual name="wing_b_mid"><pose>-2.8 1.8 11.2 -0.40 -0.50 0.6</pose><geometry><box><size>1.3 0.6 6.0</size></box></geometry><material><ambient>0.42 0.28 0.14 1</ambient><diffuse>0.62 0.44 0.22 1</diffuse><specular>0.90 0.70 0.35 1</specular></material></visual>')
    lines.append('      <visual name="wing_b_tip"><pose>-4.2 2.6 15.8 -0.55 -0.65 0.7</pose><geometry><box><size>0.9 0.35 5.5</size></box></geometry><material><ambient>0.48 0.32 0.16 1</ambient><diffuse>0.70 0.50 0.25 1</diffuse><specular>0.95 0.75 0.40 1</specular></material></visual>')
    lines.append('      <visual name="wing_b_crest"><pose>-5.2 3.2 19.5 -0.70 -0.80 0.8</pose><geometry><box><size>0.5 0.2 3.0</size></box></geometry><material><ambient>0.58 0.42 0.18 1</ambient><diffuse>0.82 0.62 0.28 1</diffuse><specular>1.0 0.85 0.50 1</specular></material></visual>')
    
    # 4. 巨型空中青銅莫比烏斯環 (Suspended 10m Giant Bronze Celestial Ring)
    lines.append('      <!-- 4. 巨型空中青銅莫比烏斯環 (直徑 10m 貫通天穹之環) -->')
    n_ring_segs = 12
    ring_radius = 4.8
    ring_z = 12.0
    for i in range(n_ring_segs):
        ang = i * (2.0 * math.pi / n_ring_segs)
        rx = ring_radius * math.cos(ang)
        ry = ring_radius * math.sin(ang)
        # 傾斜角度打造莫比烏斯環視覺
        tilt = 0.35 * math.sin(ang)
        lines.append(f'      <visual name="ring_seg_{i}"><pose>{rx:.3f} {ry:.3f} {ring_z + tilt*3.0:.3f} {tilt:.3f} 0.4 {ang + math.pi/2:.3f}</pose><geometry><box><size>2.6 0.65 0.65</size></box></geometry><material><ambient>0.42 0.28 0.14 1</ambient><diffuse>0.65 0.45 0.22 1</diffuse><specular>0.88 0.70 0.35 1</specular></material></visual>')
    
    # 5. 中央高反射拋光青銅核心球體 ("新竹科技之眼" 拋光青銅核心)
    lines.append('      <!-- 5. 核心拋光青銅晶球 ("新竹科技核心", 直徑 3.2m 耀眼青銅反射球) -->')
    lines.append('      <visual name="bronze_core_sphere"><pose>0 0 12.0 0 0 0</pose><geometry><cylinder><radius>1.6</radius><length>2.4</length></cylinder></geometry><material><ambient>0.62 0.46 0.18 1</ambient><diffuse>0.88 0.72 0.32 1</diffuse><specular>1.0 0.95 0.70 1</specular></material></visual>')
    lines.append('      <visual name="sphere_equator_band"><pose>0 0 12.0 0 0 0</pose><geometry><cylinder><radius>1.9</radius><length>0.3</length></cylinder></geometry><material><ambient>0.75 0.60 0.25 1</ambient><diffuse>0.95 0.82 0.38 1</diffuse><emissive>0.25 0.18 0.05 1</emissive></material></visual>')
    
    # 6. 周邊 8 柱青銅雕塑光柱與投射座 (8 Perimeter Bronze Light Steles)
    lines.append('      <!-- 6. 八方青銅立柱與光雕基座 -->')
    for i in range(8):
        b_ang = i * (2.0 * math.pi / 8.0)
        bx = 11.2 * math.cos(b_ang)
        by = 11.2 * math.sin(b_ang)
        lines.append(f'      <collision name="stele_col_{i}"><pose>{bx:.3f} {by:.3f} 1.6 0 0 {b_ang:.3f}</pose><geometry><box><size>0.6 0.6 2.4</size></box></geometry></collision>')
        lines.append(f'      <visual name="stele_vis_{i}"><pose>{bx:.3f} {by:.3f} 1.6 0 0 {b_ang:.3f}</pose><geometry><box><size>0.6 0.6 2.4</size></box></geometry><material><ambient>0.38 0.24 0.12 1</ambient><diffuse>0.55 0.38 0.18 1</diffuse><specular>0.8 0.6 0.3 1</specular></material></visual>')
        lines.append(f'      <visual name="stele_cap_{i}"><pose>{bx:.3f} {by:.3f} 2.9 0 0 {b_ang:.3f}</pose><geometry><box><size>0.8 0.8 0.2</size></box></geometry><material><ambient>0.65 0.50 0.20 1</ambient><diffuse>0.85 0.70 0.30 1</diffuse><specular>0.9 0.8 0.4 1</specular></material></visual>')
        lines.append(f'      <visual name="stele_light_{i}"><pose>{bx:.3f} {by:.3f} 3.05 0 0 0</pose><geometry><cylinder><radius>0.2</radius><length>0.1</length></cylinder></geometry><material><ambient>0.9 0.85 0.6 1</ambient><diffuse>1.0 0.95 0.7 1</diffuse><emissive>0.8 0.7 0.3 1</emissive></material></visual>')
        
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("giant_bronze_sculpture_monument", "Monumental 19.5m Super Giant Bronze Public Art Sculpture 'Crown of Wind and Tech Mobius' at Nikko Park Center", '\n'.join(lines))

# ==============================================================================
# Model 2: 關新帝國商業名邸大樓 (Guanxin Imperial Commercial Plaza & High-Rise, 17F)
# ==============================================================================
def create_guanxin_imperial_plaza():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="guanxin_imperial_plaza">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="bldg_link">')
    
    # 碰撞剛體
    lines.append('      <collision name="podium_col"><pose>0 0 7.0 0 0 0</pose><geometry><box><size>60.0 28.0 14.0</size></box></geometry></collision>')
    lines.append('      <collision name="tower_col"><pose>0 0 34.0 0 0 0</pose><geometry><box><size>56.0 24.0 40.0</size></box></geometry></collision>')
    
    # 1F~3F 崗石基座與騎樓
    lines.append('      <!-- 1F~3F 宏偉崗石基座 (高 14m) -->')
    lines.append('      <visual name="podium_vis"><pose>0 0 7.0 0 0 0</pose><geometry><box><size>60.0 28.0 14.0</size></box></geometry><material><ambient>0.74 0.72 0.68 1</ambient><diffuse>0.80 0.78 0.74 1</diffuse></material></visual>')
    # 騎樓走廊 (Y = +12.5m facing Guanxin Rd)
    lines.append('      <visual name="arcade_floor"><pose>0 12.5 0.08 0 0 0</pose><geometry><box><size>58.0 3.5 0.02</size></box></geometry><material><ambient>0.62 0.60 0.58 1</ambient><diffuse>0.70 0.68 0.66 1</diffuse></material></visual>')
    lines.append('      <visual name="arcade_ceiling"><pose>0 12.5 4.5 0 0 0</pose><geometry><box><size>58.0 3.5 0.25</size></box></geometry><material><ambient>0.28 0.28 0.30 1</ambient><diffuse>0.32 0.32 0.35 1</diffuse></material></visual>')
    for x_c in [-24.0, -12.0, 0.0, 12.0, 24.0]:
        lines.append(f'      <visual name="arcade_col_{int(x_c)}"><pose>{x_c} 13.8 2.25 0 0 0</pose><geometry><cylinder><radius>0.45</radius><length>4.5</length></cylinder></geometry><material><ambient>0.40 0.38 0.36 1</ambient><diffuse>0.48 0.46 0.44 1</diffuse></material></visual>')
    
    # 玉山銀行旗艦分行看板 (E.SUN Bank Green Signboard)
    lines.append('      <!-- 玉山銀行旗艦分行 (E.SUN Bank) 綠色經典招牌與挑高大門 -->')
    lines.append('      <visual name="esun_fascia"><pose>-14.0 14.1 4.8 0 0 0</pose><geometry><box><size>22.0 0.2 1.6</size></box></geometry><material><ambient>0.05 0.45 0.28 1</ambient><diffuse>0.08 0.62 0.38 1</diffuse><emissive>0.04 0.30 0.18 1</emissive></material></visual>')
    lines.append('      <visual name="esun_glass"><pose>-14.0 14.05 2.2 0 0 0</pose><geometry><box><size>20.0 0.1 3.8</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    
    # 關新名品精品名店 (Luxury Retail Storefronts)
    lines.append('      <visual name="retail_fascia"><pose>14.0 14.1 4.8 0 0 0</pose><geometry><box><size>22.0 0.2 1.6</size></box></geometry><material><ambient>0.22 0.22 0.25 1</ambient><diffuse>0.28 0.28 0.32 1</diffuse></material></visual>')
    lines.append('      <visual name="retail_glass"><pose>14.0 14.05 2.2 0 0 0</pose><geometry><box><size>20.0 0.1 3.8</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    
    # 4F~17F 雙塔現代豪宅主體 (Main Tower Body, 54m)
    lines.append('      <!-- 4F~17F 現代豪宅塔樓 -->')
    lines.append('      <visual name="tower_main_vis"><pose>0 0 34.0 0 0 0</pose><geometry><box><size>56.0 24.0 40.0</size></box></geometry><material><ambient>0.78 0.76 0.74 1</ambient><diffuse>0.84 0.82 0.80 1</diffuse></material></visual>')
    lines.append('      <visual name="balconies_west"><pose>0 12.2 34.0 0 0 0</pose><geometry><box><size>52.0 0.8 34.0</size></box></geometry><material><ambient>0.20 0.25 0.30 0.9</ambient><diffuse>0.25 0.32 0.38 0.9</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <!-- 頂部造型冠頂 (Crown) -->')
    lines.append('      <visual name="tower_crown"><pose>0 0 55.5 0 0 0</pose><geometry><box><size>50.0 20.0 3.0</size></box></geometry><material><ambient>0.25 0.25 0.28 1</ambient><diffuse>0.32 0.32 0.36 1</diffuse></material></visual>')
    lines.append('      <visual name="crown_spire"><pose>0 0 58.0 0 0 0</pose><geometry><cylinder><radius>0.4</radius><length>4.0</length></cylinder></geometry><material><ambient>0.7 0.6 0.2 1</ambient><diffuse>0.85 0.75 0.3 1</diffuse></material></visual>')
    
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("guanxin_imperial_plaza", "Guanxin Imperial Plaza 17F Mixed-Use Tower with E.SUN Bank Branch & Arcade", '\n'.join(lines))

# ==============================================================================
# Model 3: 光復路南側連續住商大樓群 (Guangfu South Commercial & Residential Strip)
# ==============================================================================
def create_guangfu_south_commercial_strip():
    for seg, length, height, floors in [("west", 130.0, 48.0, 15), ("east", 180.0, 52.0, 16)]:
        model_name = f"guangfu_south_strip_{seg}"
        lines = []
        lines.append('<?xml version="1.0" ?>')
        lines.append('<sdf version="1.8">')
        lines.append(f'  <model name="{model_name}">')
        lines.append('    <static>true</static>')
        lines.append('    <link name="strip_link">')
        
        lines.append(f'      <collision name="podium_col"><pose>0 0 4.0 0 0 0</pose><geometry><box><size>{length:.1f} 28.0 8.0</size></box></geometry></collision>')
        lines.append(f'      <collision name="tower_col"><pose>0 0 {height/2.0:.1f} 0 0 0</pose><geometry><box><size>{length-4.0:.1f} 24.0 {height:.1f}</size></box></geometry></collision>')
        
        lines.append(f'      <visual name="podium_vis"><pose>0 0 4.0 0 0 0</pose><geometry><box><size>{length:.1f} 28.0 8.0</size></box></geometry><material><ambient>0.70 0.68 0.65 1</ambient><diffuse>0.76 0.74 0.70 1</diffuse></material></visual>')
        lines.append(f'      <!-- 1F 連續騎樓走廊 (Y = +12.5m facing Guangfu Rd) -->')
        lines.append(f'      <visual name="arcade_floor"><pose>0 12.5 0.08 0 0 0</pose><geometry><box><size>{length-2.0:.1f} 3.5 0.02</size></box></geometry><material><ambient>0.60 0.58 0.56 1</ambient><diffuse>0.68 0.66 0.64 1</diffuse></material></visual>')
        lines.append(f'      <visual name="arcade_ceiling"><pose>0 12.5 4.5 0 0 0</pose><geometry><box><size>{length-2.0:.1f} 3.5 0.25</size></box></geometry><material><ambient>0.25 0.25 0.28 1</ambient><diffuse>0.30 0.30 0.34 1</diffuse></material></visual>')
        
        # 沿線商鋪櫥窗與招牌
        n_shops = int(length / 20.0)
        for i in range(n_shops):
            cx = -length/2.0 + 10.0 + i * 20.0
            lines.append(f'      <visual name="shop_sign_{i}"><pose>{cx:.1f} 14.1 4.6 0 0 0</pose><geometry><box><size>16.0 0.15 1.4</size></box></geometry><material><ambient>0.25 0.28 0.32 1</ambient><diffuse>0.32 0.36 0.40 1</diffuse></material></visual>')
            lines.append(f'      <visual name="shop_glass_{i}"><pose>{cx:.1f} 14.05 2.2 0 0 0</pose><geometry><box><size>15.0 0.1 3.8</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
            
        lines.append(f'      <!-- 主塔樓立面 ({floors}F, 高 {height}m) -->')
        lines.append(f'      <visual name="tower_main_vis"><pose>0 0 {height/2.0:.1f} 0 0 0</pose><geometry><box><size>{length-4.0:.1f} 24.0 {height:.1f}</size></box></geometry><material><ambient>0.76 0.74 0.72 1</ambient><diffuse>0.82 0.80 0.78 1</diffuse></material></visual>')
        lines.append(f'      <visual name="balconies_front"><pose>0 12.2 {height/2.0 + 2.0:.1f} 0 0 0</pose><geometry><box><size>{length-10.0:.1f} 0.8 {height - 12.0:.1f}</size></box></geometry><material><ambient>0.22 0.26 0.32 0.9</ambient><diffuse>0.28 0.34 0.40 0.9</diffuse></material></visual>')
        lines.append(f'      <visual name="roof_parapet"><pose>0 0 {height + 0.9:.1f} 0 0 0</pose><geometry><box><size>{length-2.0:.1f} 22.0 1.8</size></box></geometry><material><ambient>0.30 0.30 0.32 1</ambient><diffuse>0.35 0.35 0.38 1</diffuse></material></visual>')
        
        lines.append('    </link>')
        lines.append('  </model>')
        lines.append('</sdf>')
        save_model(model_name, f"Guangfu Road South Continuous Commercial & Residential Strip ({floors}F, {length}m)", '\n'.join(lines))

# ==============================================================================
# Model 4: 昌益藍海 / 璞石景觀名邸 (Changyi Blue Ocean & Jade Luxury Residence, 15F)
# ==============================================================================
def create_changyi_blue_ocean():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="changyi_blue_ocean_residence">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="blue_ocean_link">')
    
    lines.append('      <collision name="podium_col"><pose>0 0 4.0 0 0 0</pose><geometry><box><size>62.0 32.0 8.0</size></box></geometry></collision>')
    lines.append('      <collision name="tower_col"><pose>0 0 27.0 0 0 0</pose><geometry><box><size>58.0 28.0 42.0</size></box></geometry></collision>')
    
    lines.append('      <visual name="podium_vis"><pose>0 0 4.0 0 0 0</pose><geometry><box><size>62.0 32.0 8.0</size></box></geometry><material><ambient>0.75 0.73 0.70 1</ambient><diffuse>0.82 0.80 0.76 1</diffuse></material></visual>')
    # 騎樓 (Y = +14.5m facing Guanxin Rd)
    lines.append('      <visual name="arcade_floor"><pose>0 14.5 0.08 0 0 0</pose><geometry><box><size>60.0 3.6 0.02</size></box></geometry><material><ambient>0.65 0.62 0.60 1</ambient><diffuse>0.72 0.70 0.68 1</diffuse></material></visual>')
    lines.append('      <visual name="arcade_ceiling"><pose>0 14.5 4.2 0 0 0</pose><geometry><box><size>60.0 3.6 0.25</size></box></geometry><material><ambient>0.28 0.28 0.30 1</ambient><diffuse>0.32 0.32 0.35 1</diffuse></material></visual>')
    for x_c in [-22.0, -11.0, 0.0, 11.0, 22.0]:
        lines.append(f'      <visual name="arcade_col_{int(x_c)}"><pose>{x_c} 15.8 2.1 0 0 0</pose><geometry><cylinder><radius>0.42</radius><length>4.2</length></cylinder></geometry><material><ambient>0.38 0.4 0.42 1</ambient><diffuse>0.45 0.48 0.50 1</diffuse></material></visual>')
    
    # 烘焙名店與精品診所
    lines.append('      <visual name="bakery_fascia"><pose>-14.0 16.1 4.5 0 0 0</pose><geometry><box><size>18.0 0.15 1.4</size></box></geometry><material><ambient>0.82 0.52 0.18 1</ambient><diffuse>0.92 0.60 0.22 1</diffuse><emissive>0.3 0.18 0.05 1</emissive></material></visual>')
    lines.append('      <visual name="bakery_glass"><pose>-14.0 16.05 2.1 0 0 0</pose><geometry><box><size>17.0 0.1 3.6</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <visual name="clinic_fascia"><pose>14.0 16.1 4.5 0 0 0</pose><geometry><box><size>18.0 0.15 1.4</size></box></geometry><material><ambient>0.12 0.42 0.62 1</ambient><diffuse>0.18 0.55 0.78 1</diffuse><emissive>0.08 0.25 0.38 1</emissive></material></visual>')
    lines.append('      <visual name="clinic_glass"><pose>14.0 16.05 2.1 0 0 0</pose><geometry><box><size>17.0 0.1 3.6</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    
    # 15F 塔樓主體
    lines.append('      <visual name="tower_main_vis"><pose>0 0 27.0 0 0 0</pose><geometry><box><size>58.0 28.0 42.0</size></box></geometry><material><ambient>0.78 0.76 0.72 1</ambient><diffuse>0.84 0.82 0.78 1</diffuse></material></visual>')
    lines.append('      <visual name="balconies_front"><pose>0 14.2 27.0 0 0 0</pose><geometry><box><size>52.0 0.8 36.0</size></box></geometry><material><ambient>0.22 0.28 0.34 0.9</ambient><diffuse>0.28 0.35 0.42 0.9</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <visual name="tower_crown"><pose>0 0 49.5 0 0 0</pose><geometry><box><size>54.0 24.0 3.0</size></box></geometry><material><ambient>0.30 0.32 0.35 1</ambient><diffuse>0.36 0.38 0.42 1</diffuse></material></visual>')
    
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("changyi_blue_ocean_residence", "Changyi Blue Ocean & Jade Luxury Residence 15F Tower with Ground Arcade", '\n'.join(lines))

# ==============================================================================
# Model 5: 豐邑一極高層住宅名邸 (Fengyi Landmark High-Rise Residence, 20F)
# ==============================================================================
def create_fengyi_landmark_residence():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="fengyi_landmark_residence">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="fengyi_link">')
    
    lines.append('      <collision name="podium_col"><pose>0 0 5.0 0 0 0</pose><geometry><box><size>72.0 34.0 10.0</size></box></geometry></collision>')
    lines.append('      <collision name="tower_col"><pose>0 0 35.0 0 0 0</pose><geometry><box><size>68.0 28.0 54.0</size></box></geometry></collision>')
    
    # 新古典崗石基座
    lines.append('      <visual name="podium_vis"><pose>0 0 5.0 0 0 0</pose><geometry><box><size>72.0 34.0 10.0</size></box></geometry><material><ambient>0.76 0.74 0.70 1</ambient><diffuse>0.82 0.80 0.76 1</diffuse></material></visual>')
    lines.append('      <visual name="arcade_floor"><pose>0 15.5 0.08 0 0 0</pose><geometry><box><size>70.0 3.8 0.02</size></box></geometry><material><ambient>0.65 0.62 0.60 1</ambient><diffuse>0.72 0.70 0.68 1</diffuse></material></visual>')
    lines.append('      <visual name="arcade_ceiling"><pose>0 15.5 4.8 0 0 0</pose><geometry><box><size>70.0 3.8 0.25</size></box></geometry><material><ambient>0.28 0.28 0.30 1</ambient><diffuse>0.32 0.32 0.35 1</diffuse></material></visual>')
    for x_c in [-28.0, -14.0, 0.0, 14.0, 28.0]:
        lines.append(f'      <visual name="roman_col_{int(x_c)}"><pose>{x_c} 17.0 2.4 0 0 0</pose><geometry><cylinder><radius>0.48</radius><length>4.8</length></cylinder></geometry><material><ambient>0.42 0.40 0.38 1</ambient><diffuse>0.50 0.48 0.45 1</diffuse></material></visual>')
    
    # 頂級生鮮超市與精品咖啡
    lines.append('      <visual name="organic_fascia"><pose>-18.0 17.2 5.2 0 0 0</pose><geometry><box><size>24.0 0.15 1.6</size></box></geometry><material><ambient>0.15 0.45 0.22 1</ambient><diffuse>0.22 0.62 0.30 1</diffuse><emissive>0.08 0.25 0.12 1</emissive></material></visual>')
    lines.append('      <visual name="organic_glass"><pose>-18.0 17.15 2.4 0 0 0</pose><geometry><box><size>22.0 0.1 4.2</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <visual name="cafe_fascia"><pose>18.0 17.2 5.2 0 0 0</pose><geometry><box><size>24.0 0.15 1.6</size></box></geometry><material><ambient>0.45 0.28 0.15 1</ambient><diffuse>0.55 0.36 0.20 1</diffuse><emissive>0.20 0.12 0.05 1</emissive></material></visual>')
    lines.append('      <visual name="cafe_glass"><pose>18.0 17.15 2.4 0 0 0</pose><geometry><box><size>22.0 0.1 4.2</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    
    # 20F 雙子塔樓主體 (高 65m)
    lines.append('      <visual name="tower_main_vis"><pose>0 0 36.0 0 0 0</pose><geometry><box><size>68.0 28.0 52.0</size></box></geometry><material><ambient>0.78 0.76 0.74 1</ambient><diffuse>0.84 0.82 0.80 1</diffuse></material></visual>')
    lines.append('      <visual name="balconies_front"><pose>0 14.2 36.0 0 0 0</pose><geometry><box><size>64.0 0.8 44.0</size></box></geometry><material><ambient>0.20 0.25 0.32 0.9</ambient><diffuse>0.25 0.32 0.40 0.9</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <!-- 雙冠頂造型 (Twin Crowns) -->')
    lines.append('      <visual name="crown_left"><pose>-18.0 0 64.0 0 0 0</pose><geometry><box><size>26.0 22.0 4.0</size></box></geometry><material><ambient>0.28 0.28 0.32 1</ambient><diffuse>0.34 0.34 0.38 1</diffuse></material></visual>')
    lines.append('      <visual name="crown_right"><pose>18.0 0 64.0 0 0 0</pose><geometry><box><size>26.0 22.0 4.0</size></box></geometry><material><ambient>0.28 0.28 0.32 1</ambient><diffuse>0.34 0.34 0.38 1</diffuse></material></visual>')
    
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("fengyi_landmark_residence", "Fengyi Landmark 20F Luxury High-Rise Residence (65m) with Neoclassical Podium", '\n'.join(lines))

# ==============================================================================
# Model 6: 關新名品商務會館 (Guanxin Prestige Commercial Center, 14F)
# ==============================================================================
def create_guanxin_prestige_center():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="guanxin_prestige_center">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="prestige_link">')
    lines.append('      <collision name="tower_col"><pose>0 0 23.0 0 0 0</pose><geometry><box><size>44.0 28.0 46.0</size></box></geometry></collision>')
    lines.append('      <visual name="tower_vis"><pose>0 0 23.0 0 0 0</pose><geometry><box><size>44.0 28.0 46.0</size></box></geometry><material><ambient>0.74 0.75 0.76 1</ambient><diffuse>0.80 0.82 0.84 1</diffuse></material></visual>')
    # 現代玻璃帷幕立面
    lines.append('      <visual name="glass_curtain"><pose>0 14.1 23.0 0 0 0</pose><geometry><box><size>40.0 0.2 42.0</size></box></geometry><material><ambient>0.15 0.25 0.35 0.92</ambient><diffuse>0.20 0.35 0.50 0.92</diffuse><specular>0.95 0.98 1.0 1</specular></material></visual>')
    lines.append('      <visual name="retail_arcade"><pose>0 13.0 0.08 0 0 0</pose><geometry><box><size>42.0 3.2 0.02</size></box></geometry><material><ambient>0.62 0.62 0.62 1</ambient><diffuse>0.70 0.70 0.70 1</diffuse></material></visual>')
    lines.append('      <visual name="med_fascia"><pose>0 14.2 4.5 0 0 0</pose><geometry><box><size>28.0 0.15 1.5</size></box></geometry><material><ambient>0.10 0.40 0.55 1</ambient><diffuse>0.15 0.55 0.75 1</diffuse><emissive>0.08 0.25 0.35 1</emissive></material></visual>')
    lines.append('      <visual name="roof_top"><pose>0 0 47.0 0 0 0</pose><geometry><box><size>38.0 22.0 2.0</size></box></geometry><material><ambient>0.30 0.30 0.32 1</ambient><diffuse>0.35 0.35 0.38 1</diffuse></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("guanxin_prestige_center", "Guanxin Prestige Commercial Center 14F Glass Curtain Medical & Boutique Tower", '\n'.join(lines))

# ==============================================================================
# Model 7: 公園首席景觀名邸 (Park Prime Residence South, 18F)
# ==============================================================================
def create_park_prime_residence():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="park_prime_residence">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="park_prime_link">')
    lines.append('      <collision name="tower_col"><pose>0 0 28.0 0 0 0</pose><geometry><box><size>46.0 30.0 56.0</size></box></geometry></collision>')
    lines.append('      <visual name="tower_vis"><pose>0 0 28.0 0 0 0</pose><geometry><box><size>46.0 30.0 56.0</size></box></geometry><material><ambient>0.76 0.74 0.70 1</ambient><diffuse>0.82 0.80 0.76 1</diffuse></material></visual>')
    lines.append('      <!-- 1F 面向日光公園景觀餐廳 -->')
    lines.append('      <visual name="bistro_fascia"><pose>0 15.1 4.5 0 0 0</pose><geometry><box><size>32.0 0.15 1.5</size></box></geometry><material><ambient>0.50 0.20 0.15 1</ambient><diffuse>0.68 0.26 0.20 1</diffuse><emissive>0.25 0.08 0.05 1</emissive></material></visual>')
    lines.append('      <visual name="bistro_glass"><pose>0 15.05 2.2 0 0 0</pose><geometry><box><size>30.0 0.1 3.8</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse></material></visual>')
    # 公園景觀陽台
    lines.append('      <visual name="parkview_balconies"><pose>0 15.2 30.0 0 0 0</pose><geometry><box><size>40.0 0.9 44.0</size></box></geometry><material><ambient>0.20 0.26 0.32 0.9</ambient><diffuse>0.26 0.34 0.42 0.9</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <visual name="tower_crown"><pose>0 0 57.5 0 0 0</pose><geometry><box><size>42.0 24.0 3.0</size></box></geometry><material><ambient>0.28 0.28 0.32 1</ambient><diffuse>0.34 0.34 0.38 1</diffuse></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("park_prime_residence", "Park Prime Residence 18F Luxury Parkview Tower Facing Nikko Park", '\n'.join(lines))

# ==============================================================================
# Model 8: 晴空樹高層景觀大樓 (Skytree Parkview High-Rise North, 22F)
# ==============================================================================
def create_skytree_parkview_tower():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="skytree_parkview_tower">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="skytree_link">')
    lines.append('      <collision name="tower_col"><pose>0 0 35.0 0 0 0</pose><geometry><box><size>44.0 30.0 70.0</size></box></geometry></collision>')
    lines.append('      <visual name="tower_vis"><pose>0 0 35.0 0 0 0</pose><geometry><box><size>44.0 30.0 70.0</size></box></geometry><material><ambient>0.78 0.78 0.80 1</ambient><diffuse>0.85 0.85 0.88 1</diffuse></material></visual>')
    # 香檳金垂直裝飾格柵與玻璃陽台
    lines.append('      <visual name="gold_fins"><pose>0 15.1 36.0 0 0 0</pose><geometry><box><size>38.0 0.3 56.0</size></box></geometry><material><ambient>0.65 0.52 0.25 1</ambient><diffuse>0.82 0.68 0.32 1</diffuse><specular>0.8 0.7 0.4 1</specular></material></visual>')
    lines.append('      <visual name="tea_fascia"><pose>0 15.2 4.5 0 0 0</pose><geometry><box><size>28.0 0.15 1.5</size></box></geometry><material><ambient>0.22 0.42 0.28 1</ambient><diffuse>0.30 0.58 0.38 1</diffuse><emissive>0.10 0.25 0.15 1</emissive></material></visual>')
    # 璀璨天際線冠頂
    lines.append('      <visual name="crown_illuminated"><pose>0 0 71.5 0 0 0</pose><geometry><box><size>40.0 24.0 3.0</size></box></geometry><material><ambient>0.75 0.75 0.80 1</ambient><diffuse>0.90 0.90 0.95 1</diffuse><emissive>0.3 0.3 0.35 1</emissive></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("skytree_parkview_tower", "Skytree Parkview 22F High-Rise Tower (70m) with Architectural Gold Fins", '\n'.join(lines))

# ==============================================================================
# Model 9: 關新北路角隅精品商廈 (Corner Prestige Boutique Plaza, 9F)
# ==============================================================================
def create_corner_boutique_plaza():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="corner_boutique_plaza">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="plaza_link">')
    lines.append('      <collision name="col"><pose>0 0 16.0 0 0 0</pose><geometry><box><size>22.0 24.0 32.0</size></box></geometry></collision>')
    lines.append('      <visual name="main_vis"><pose>0 0 16.0 0 0 0</pose><geometry><box><size>22.0 24.0 32.0</size></box></geometry><material><ambient>0.75 0.74 0.72 1</ambient><diffuse>0.82 0.80 0.78 1</diffuse></material></visual>')
    lines.append('      <visual name="shop_fascia"><pose>0 12.1 3.8 0 0 0</pose><geometry><box><size>18.0 0.15 1.4</size></box></geometry><material><ambient>0.85 0.45 0.15 1</ambient><diffuse>0.95 0.55 0.18 1</diffuse><emissive>0.3 0.15 0.05 1</emissive></material></visual>')
    lines.append('      <visual name="glass_front"><pose>0 12.05 1.8 0 0 0</pose><geometry><box><size>17.0 0.1 3.0</size></box></geometry><material><ambient>0.15 0.25 0.35 0.88</ambient><diffuse>0.20 0.35 0.45 0.88</diffuse></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("corner_boutique_plaza", "Corner Prestige Boutique Plaza 9F Commercial Building", '\n'.join(lines))

# ==============================================================================
# Model 10: 關東路口科技金融大樓 (Guandong Corner Tech Tower, 15F)
# ==============================================================================
def create_guandong_corner_tech_tower():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="guandong_corner_tech_tower">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="tower_link">')
    lines.append('      <collision name="col"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>50.0 24.0 48.0</size></box></geometry></collision>')
    lines.append('      <visual name="main_vis"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>50.0 24.0 48.0</size></box></geometry><material><ambient>0.74 0.76 0.78 1</ambient><diffuse>0.80 0.82 0.85 1</diffuse></material></visual>')
    lines.append('      <visual name="curtain_vis"><pose>0 12.1 24.0 0 0 0</pose><geometry><box><size>46.0 0.2 42.0</size></box></geometry><material><ambient>0.15 0.28 0.42 0.9</ambient><diffuse>0.20 0.38 0.55 0.9</diffuse><specular>0.95 0.98 1.0 1</specular></material></visual>')
    lines.append('      <visual name="bank_sign"><pose>0 12.2 4.8 0 0 0</pose><geometry><box><size>26.0 0.15 1.5</size></box></geometry><material><ambient>0.82 0.18 0.15 1</ambient><diffuse>0.95 0.22 0.18 1</diffuse><emissive>0.4 0.08 0.06 1</emissive></material></visual>')
    lines.append('      <visual name="crown"><pose>0 0 49.5 0 0 0</pose><geometry><box><size>44.0 20.0 3.0</size></box></geometry><material><ambient>0.28 0.30 0.34 1</ambient><diffuse>0.34 0.36 0.40 1</diffuse></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("guandong_corner_tech_tower", "Guandong Corner Financial & Tech Tower 15F High-Rise", '\n'.join(lines))

# ==============================================================================
# Model 11: 關東名邸與新莊商務街區 (Guandong West Commercial & Residential Block, 15F)
# ==============================================================================
def create_guandong_west_commercial_block():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="guandong_west_commercial_block">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="gd_link">')
    lines.append('      <collision name="col"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>80.0 26.0 48.0</size></box></geometry></collision>')
    lines.append('      <visual name="main_vis"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>80.0 26.0 48.0</size></box></geometry><material><ambient>0.74 0.72 0.68 1</ambient><diffuse>0.80 0.78 0.74 1</diffuse></material></visual>')
    lines.append('      <visual name="arcade_floor"><pose>0 11.5 0.08 0 0 0</pose><geometry><box><size>78.0 3.2 0.02</size></box></geometry><material><ambient>0.62 0.60 0.58 1</ambient><diffuse>0.70 0.68 0.66 1</diffuse></material></visual>')
    for i in range(4):
        cx = -30.0 + i * 20.0
        lines.append(f'      <visual name="store_sign_{i}"><pose>{cx} 13.1 4.5 0 0 0</pose><geometry><box><size>15.0 0.15 1.3</size></box></geometry><material><ambient>0.3 0.32 0.35 1</ambient><diffuse>0.38 0.40 0.45 1</diffuse></material></visual>')
    lines.append('      <visual name="balconies"><pose>0 11.2 26.0 0 0 0</pose><geometry><box><size>74.0 0.8 38.0</size></box></geometry><material><ambient>0.22 0.26 0.32 0.9</ambient><diffuse>0.28 0.34 0.40 0.9</diffuse></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("guandong_west_commercial_block", "Guandong West Commercial & Residential Block 15F", '\n'.join(lines))

# ==============================================================================
# Model 12: 新莊車站前西側商旅轉運大樓 (Xinzhuang Transit Hotel, 14F)
# ==============================================================================
def create_xinzhuang_transit_hotel():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="xinzhuang_transit_hotel">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="hotel_link">')
    lines.append('      <collision name="col"><pose>0 0 22.5 0 0 0</pose><geometry><box><size>44.0 28.0 45.0</size></box></geometry></collision>')
    lines.append('      <visual name="main_vis"><pose>0 0 22.5 0 0 0</pose><geometry><box><size>44.0 28.0 45.0</size></box></geometry><material><ambient>0.75 0.76 0.78 1</ambient><diffuse>0.82 0.84 0.86 1</diffuse></material></visual>')
    lines.append('      <visual name="hotel_curtain"><pose>0 14.1 22.5 0 0 0</pose><geometry><box><size>40.0 0.2 40.0</size></box></geometry><material><ambient>0.15 0.25 0.35 0.92</ambient><diffuse>0.20 0.35 0.48 0.92</diffuse><specular>0.9 0.95 1.0 1</specular></material></visual>')
    lines.append('      <visual name="hotel_sign"><pose>0 14.2 4.5 0 0 0</pose><geometry><box><size>26.0 0.15 1.5</size></box></geometry><material><ambient>0.82 0.65 0.15 1</ambient><diffuse>0.95 0.78 0.20 1</diffuse><emissive>0.3 0.22 0.05 1</emissive></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("xinzhuang_transit_hotel", "Xinzhuang Station Transit Hotel & Commercial Tower 14F", '\n'.join(lines))

# ==============================================================================
# Model 13: 新莊車站東側科技商辦大樓 (Xinzhuang Station East Tech Tower, 15F)
# ==============================================================================
def create_xinzhuang_station_east_tower():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="xinzhuang_station_east_tower">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="east_tower_link">')
    lines.append('      <collision name="col"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>50.0 26.0 48.0</size></box></geometry></collision>')
    lines.append('      <visual name="main_vis"><pose>0 0 24.0 0 0 0</pose><geometry><box><size>50.0 26.0 48.0</size></box></geometry><material><ambient>0.74 0.76 0.78 1</ambient><diffuse>0.80 0.82 0.85 1</diffuse></material></visual>')
    lines.append('      <visual name="glass_vis"><pose>0 13.1 24.0 0 0 0</pose><geometry><box><size>46.0 0.2 42.0</size></box></geometry><material><ambient>0.15 0.28 0.42 0.9</ambient><diffuse>0.20 0.38 0.55 0.9</diffuse><specular>0.95 0.98 1.0 1</specular></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("xinzhuang_station_east_tower", "Xinzhuang Station East Tech Office Tower 15F", '\n'.join(lines))

# ==============================================================================
# Model 14: 日光公園現代景觀玻璃咖啡亭與休憩長廊 (Nikko Glass Cafe Pavilion & Pergola)
# ==============================================================================
def create_nikko_glass_cafe_pavilion():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="nikko_glass_cafe_pavilion">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="pavilion_link">')
    
    # 戶外木平台地坪
    lines.append('      <collision name="deck_col"><pose>0 0 0.15 0 0 0</pose><geometry><box><size>22.0 16.0 0.3</size></box></geometry></collision>')
    lines.append('      <visual name="deck_vis"><pose>0 0 0.15 0 0 0</pose><geometry><box><size>22.0 16.0 0.3</size></box></geometry><material><ambient>0.48 0.32 0.18 1</ambient><diffuse>0.58 0.40 0.24 1</diffuse></material></visual>')
    
    # 玻璃咖啡亭本體 (14m x 8m x 4.2m)
    lines.append('      <collision name="cafe_col"><pose>-3.0 0 2.4 0 0 0</pose><geometry><box><size>14.0 8.0 4.2</size></box></geometry></collision>')
    lines.append('      <visual name="cafe_glass"><pose>-3.0 0 2.4 0 0 0</pose><geometry><box><size>14.0 8.0 4.2</size></box></geometry><material><ambient>0.15 0.25 0.35 0.85</ambient><diffuse>0.20 0.35 0.48 0.85</diffuse><specular>0.95 0.98 1.0 1</specular></material></visual>')
    # 弧形實木與青銅雨遮屋頂
    lines.append('      <visual name="cafe_roof"><pose>-3.0 0 4.6 0 0 0</pose><geometry><box><size>15.5 9.5 0.35</size></box></geometry><material><ambient>0.42 0.28 0.15 1</ambient><diffuse>0.55 0.38 0.22 1</diffuse><specular>0.7 0.5 0.2 1</specular></material></visual>')
    
    # 戶外露天遮陽傘與咖啡雅座
    for px, py in [(6.0, -4.5), (6.0, 4.5), (7.5, 0.0)]:
        lines.append(f'      <visual name="table_{int(px)}_{int(py)}"><pose>{px} {py} 0.75 0 0 0</pose><geometry><cylinder><radius>0.6</radius><length>0.75</length></cylinder></geometry><material><ambient>0.3 0.3 0.32 1</ambient><diffuse>0.35 0.35 0.38 1</diffuse></material></visual>')
        lines.append(f'      <visual name="umbrella_{int(px)}_{int(py)}"><pose>{px} {py} 2.6 0 0 0</pose><geometry><cylinder><radius>1.6</radius><length>0.35</length></cylinder></geometry><material><ambient>0.85 0.82 0.75 1</ambient><diffuse>0.92 0.88 0.80 1</diffuse></material></visual>')
        
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("nikko_glass_cafe_pavilion", "Nikko Park Modern Glass Cafe Pavilion with Cedar Deck and Umbrellas", '\n'.join(lines))

# ==============================================================================
# Model 15: 日光綠蔭花園社區與文創商場 (Nikko Garden Residences East, 14F)
# ==============================================================================
def create_nikko_garden_residences_east():
    for name, length, width, height, floors in [("south", 70.0, 45.0, 45.0, 14), ("north", 65.0, 40.0, 42.0, 13)]:
        model_name = f"nikko_garden_block_{name}"
        lines = []
        lines.append('<?xml version="1.0" ?>')
        lines.append('<sdf version="1.8">')
        lines.append(f'  <model name="{model_name}">')
        lines.append('    <static>true</static>')
        lines.append('    <link name="garden_link">')
        lines.append(f'      <collision name="col"><pose>0 0 {height/2.0:.1f} 0 0 0</pose><geometry><box><size>{length:.1f} {width:.1f} {height:.1f}</size></box></geometry></collision>')
        lines.append(f'      <visual name="main_vis"><pose>0 0 {height/2.0:.1f} 0 0 0</pose><geometry><box><size>{length:.1f} {width:.1f} {height:.1f}</size></box></geometry><material><ambient>0.74 0.73 0.70 1</ambient><diffuse>0.80 0.79 0.76 1</diffuse></material></visual>')
        lines.append(f'      <visual name="balconies"><pose>0 0 {height/2.0:.1f} 0 0 0</pose><geometry><box><size>{length-4.0:.1f} {width+0.6:.1f} {height-8.0:.1f}</size></box></geometry><material><ambient>0.20 0.25 0.30 0.88</ambient><diffuse>0.25 0.32 0.38 0.88</diffuse></material></visual>')
        lines.append('    </link>')
        lines.append('  </model>')
        lines.append('</sdf>')
        save_model(model_name, f"Nikko Garden Residential Community & Creative Studios {name} ({floors}F)", '\n'.join(lines))

# ==============================================================================
# Model 16: 各橫向街道端點連貫街區 (Cross-Streets Extension Blocks)
# ==============================================================================
def create_cross_street_blocks():
    blocks = [
        ("gx1_west_end_block", 45.0, 24.0, 42.0, "關新一街西端住宅街區大樓 (13F)"),
        ("gx2_west_end_block", 60.0, 26.0, 45.0, "關新二街西端商住街區大樓 (14F)"),
        ("gxn_west_end_block", 55.0, 26.0, 45.0, "關新北路西端住宅街區大樓 (14F)"),
        ("guangfu_east_tech_block", 75.0, 26.0, 46.0, "光復路東段科技商辦大樓 (14F)"),
        ("guandong_east_commercial_block", 65.0, 22.0, 36.0, "關東路東段南側商住大樓 (11F)"),
        ("gxe_north_commercial_block", 52.0, 22.0, 38.0, "關新東路北段商務大樓 (12F)")
    ]
    for b_name, l, w, h, desc in blocks:
        lines = []
        lines.append('<?xml version="1.0" ?>')
        lines.append('<sdf version="1.8">')
        lines.append(f'  <model name="{b_name}">')
        lines.append('    <static>true</static>')
        lines.append('    <link name="block_link">')
        lines.append(f'      <collision name="col"><pose>0 0 {h/2.0:.1f} 0 0 0</pose><geometry><box><size>{l:.1f} {w:.1f} {h:.1f}</size></box></geometry></collision>')
        lines.append(f'      <visual name="main_vis"><pose>0 0 {h/2.0:.1f} 0 0 0</pose><geometry><box><size>{l:.1f} {w:.1f} {h:.1f}</size></box></geometry><material><ambient>0.73 0.72 0.70 1</ambient><diffuse>0.80 0.78 0.75 1</diffuse></material></visual>')
        lines.append(f'      <visual name="balconies"><pose>0 0 {h/2.0:.1f} 0 0 0</pose><geometry><box><size>{l-4.0:.1f} {w+0.6:.1f} {h-8.0:.1f}</size></box></geometry><material><ambient>0.22 0.26 0.32 0.88</ambient><diffuse>0.28 0.34 0.40 0.88</diffuse></material></visual>')
        lines.append('    </link>')
        lines.append('  </model>')
        lines.append('</sdf>')
        save_model(b_name, desc, '\n'.join(lines))

def main():
    print("Generating all 16 new high-detail models...")
    create_giant_bronze_sculpture_monument()
    create_guanxin_imperial_plaza()
    create_guangfu_south_commercial_strip()
    create_changyi_blue_ocean()
    create_fengyi_landmark_residence()
    create_guanxin_prestige_center()
    create_park_prime_residence()
    create_skytree_parkview_tower()
    create_corner_boutique_plaza()
    create_guandong_corner_tech_tower()
    create_guandong_west_commercial_block()
    create_xinzhuang_transit_hotel()
    create_xinzhuang_station_east_tower()
    create_nikko_glass_cafe_pavilion()
    create_nikko_garden_residences_east()
    create_cross_street_blocks()
    print("All models successfully created!")

if __name__ == "__main__":
    main()

# ==============================================================================
# Model 17: 街角青銅公共藝術微雕塑 (Bronze Street Sculptures for Plazas & Nodes)
# ==============================================================================
def create_bronze_street_sculpture():
    lines = []
    lines.append('<?xml version="1.0" ?>')
    lines.append('<sdf version="1.8">')
    lines.append('  <model name="bronze_street_sculpture">')
    lines.append('    <static>true</static>')
    lines.append('    <link name="sculpture_link">')
    lines.append('      <collision name="pedestal_col"><pose>0 0 0.45 0 0 0</pose><geometry><box><size>1.6 1.6 0.9</size></box></geometry></collision>')
    lines.append('      <visual name="pedestal_vis"><pose>0 0 0.45 0 0 0</pose><geometry><box><size>1.6 1.6 0.9</size></box></geometry><material><ambient>0.3 0.3 0.32 1</ambient><diffuse>0.38 0.38 0.42 1</diffuse></material></visual>')
    lines.append('      <!-- 現代幾何青銅雕塑體 (高 3.2m) -->')
    lines.append('      <visual name="bronze_body_lower"><pose>0 0 1.5 0.2 0.3 0.4</pose><geometry><box><size>0.6 0.4 1.4</size></box></geometry><material><ambient>0.42 0.28 0.14 1</ambient><diffuse>0.65 0.45 0.22 1</diffuse><specular>0.88 0.70 0.35 1</specular></material></visual>')
    lines.append('      <visual name="bronze_body_ring"><pose>0 0 2.2 0.4 0.2 0.8</pose><geometry><cylinder><radius>0.65</radius><length>0.25</length></cylinder></geometry><material><ambient>0.50 0.35 0.16 1</ambient><diffuse>0.75 0.55 0.26 1</diffuse><specular>0.92 0.78 0.40 1</specular></material></visual>')
    lines.append('      <visual name="bronze_body_spire"><pose>0 0 2.8 0 0 0</pose><geometry><box><size>0.25 0.25 1.1</size></box></geometry><material><ambient>0.58 0.42 0.18 1</ambient><diffuse>0.85 0.65 0.30 1</diffuse><specular>0.98 0.88 0.50 1</specular></material></visual>')
    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')
    save_model("bronze_street_sculpture", "Modern Geometric Bronze Civic Sculpture (3.2m)", '\n'.join(lines))

def generate_world_includes():
    includes = []
    includes.append('\n    <!-- ==================== Phase 8: 全域路網街道立面全線補全、內部街區與巨型青銅藝術裝置 ==================== -->')
    includes.append('    <!-- 達成目標: 所有道路接觸面均有連貫建物街區、道路圍塑內部街區補全、日光公園中央設置超級大青銅裝置藝術 -->')
    
    # 1. 日光公園中央核心: 超級大銅製裝置藝術
    m_e, m_n = pt_road(416.0, 62.0)
    includes.append('\n    <!-- 1. 日光公園核心地標：超級大青銅裝置藝術「風之冠．無限科技之環」(19.5m 雙翼螺旋莫比烏斯環青銅雕塑) -->')
    includes.append('    <include>')
    includes.append('      <name>giant_bronze_sculpture_monument</name>')
    includes.append('      <uri>model://giant_bronze_sculpture_monument</uri>')
    includes.append(f'      <pose>{m_e:.3f} {m_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 2. 日光公園現代景觀玻璃咖啡亭
    c_e, c_n = pt_road(375.0, 85.0)
    includes.append('\n    <!-- 2. 日光公園現代景觀玻璃咖啡亭與露天遮陽雅座 -->')
    includes.append('    <include>')
    includes.append('      <name>nikko_glass_cafe_pavilion</name>')
    includes.append('      <uri>model://nikko_glass_cafe_pavilion</uri>')
    includes.append(f'      <pose>{c_e:.3f} {c_n:.3f} 0.10 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 3. 關新帝國商業名邸大樓 (東南角, 17F)
    imp_e, imp_n = pt_road(48.0, 28.0)
    includes.append('\n    <!-- 3. 關新帝國商業名邸大樓 (光復路與關新路口東南角, 17F 豪宅商辦、玉山銀行旗艦分行、挑高騎樓) -->')
    includes.append('    <include>')
    includes.append('      <name>guanxin_imperial_plaza</name>')
    includes.append('      <uri>model://guanxin_imperial_plaza</uri>')
    includes.append(f'      <pose>{imp_e:.3f} {imp_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 4. 光復路南側連續住商街區 (西段 & 東段)
    gfw_e, gfw_n = pt_road(-36.0, -75.0)
    gfe_e, gfe_n = pt_road(-36.0, 80.0)
    includes.append('\n    <!-- 4. 光復路南側全線連續住商大樓群 (15F~16F, 挑高連續騎樓、銀行、連鎖名店、生活商圈) -->')
    includes.append('    <include>')
    includes.append('      <name>guangfu_south_strip_west</name>')
    includes.append('      <uri>model://guangfu_south_strip_west</uri>')
    includes.append(f'      <pose>{gfw_e:.3f} {gfw_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    includes.append('    <include>')
    includes.append('      <name>guangfu_south_strip_east</name>')
    includes.append('      <uri>model://guangfu_south_strip_east</uri>')
    includes.append(f'      <pose>{gfe_e:.3f} {gfe_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 5. 光復路東段科技商辦大樓
    gft_e, gft_n = pt_road(35.0, 95.0)
    includes.append('\n    <!-- 5. 光復路東段科技商辦大樓 (14F) -->')
    includes.append('    <include>')
    includes.append('      <name>guangfu_east_tech_block</name>')
    includes.append('      <uri>model://guangfu_east_tech_block</uri>')
    includes.append(f'      <pose>{gft_e:.3f} {gft_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 6. 關新一街西端住宅街區大樓
    gx1w_e, gx1w_n = pt_road(88.0, -72.0)
    includes.append('\n    <!-- 6. 關新一街西端住宅街區大樓 (13F) -->')
    includes.append('    <include>')
    includes.append('      <name>gx1_west_end_block</name>')
    includes.append('      <uri>model://gx1_west_end_block</uri>')
    includes.append(f'      <pose>{gx1w_e:.3f} {gx1w_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 7. 昌益藍海 / 璞石景觀名邸 (15F)
    bo_e, bo_n = pt_road(125.0, -32.0)
    includes.append('\n    <!-- 7. 昌益藍海 / 璞石景觀名邸 (關新一街與關新路西北角, 15F, 騎樓、精品烘焙、牙醫診所) -->')
    includes.append('    <include>')
    includes.append('      <name>changyi_blue_ocean_residence</name>')
    includes.append('      <uri>model://changyi_blue_ocean_residence</uri>')
    includes.append(f'      <pose>{bo_e:.3f} {bo_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 8. 豐邑一極高層住宅名邸 (20F, 高 65m)
    fy_e, fy_n = pt_road(195.0, -34.0)
    includes.append('\n    <!-- 8. 豐邑一極高層住宅名邸 (關新路西側中南段, 20F, 高 65m, 新古典崗石羅馬列柱、有機超市、精品咖啡) -->')
    includes.append('    <include>')
    includes.append('      <name>fengyi_landmark_residence</name>')
    includes.append('      <uri>model://fengyi_landmark_residence</uri>')
    includes.append(f'      <pose>{fy_e:.3f} {fy_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 9. 關新名品商務會館 (14F)
    pc_e, pc_n = pt_road(285.0, -30.0)
    includes.append('\n    <!-- 9. 關新名品商務會館 (月影會館與橘時咖啡之間, 14F, 現代藍灰玻璃帷幕、醫美診所、名牌精品) -->')
    includes.append('    <include>')
    includes.append('      <name>guanxin_prestige_center</name>')
    includes.append('      <uri>model://guanxin_prestige_center</uri>')
    includes.append(f'      <pose>{pc_e:.3f} {pc_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 10. 關新二街西端商住街區大樓
    gx2w_e, gx2w_n = pt_road(344.5, -85.0)
    includes.append('\n    <!-- 10. 關新二街西端商住街區大樓 (14F) -->')
    includes.append('    <include>')
    includes.append('      <name>gx2_west_end_block</name>')
    includes.append('      <uri>model://gx2_west_end_block</uri>')
    includes.append(f'      <pose>{gx2w_e:.3f} {gx2w_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 11. 公園首席景觀名邸 (18F)
    pp_e, pp_n = pt_road(375.0, -33.0)
    includes.append('\n    <!-- 11. 公園首席景觀名邸 (關新路西側正對日光公園南半段, 18F, 景觀義式餐廳、全景陽台) -->')
    includes.append('    <include>')
    includes.append('      <name>park_prime_residence</name>')
    includes.append('      <uri>model://park_prime_residence</uri>')
    includes.append(f'      <pose>{pp_e:.3f} {pp_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 12. 晴空樹高層景觀大樓 (22F, 高 70m)
    st_e, st_n = pt_road(458.0, -33.0)
    includes.append('\n    <!-- 12. 晴空樹高層景觀大樓 (東京中城北側正對日光公園, 22F, 高 70m, 香檳金格柵、茶藝文化館、璀璨天際線冠頂) -->')
    includes.append('    <include>')
    includes.append('      <name>skytree_parkview_tower</name>')
    includes.append('      <uri>model://skytree_parkview_tower</uri>')
    includes.append(f'      <pose>{st_e:.3f} {st_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 13. 關新北路西端住宅街區大樓
    gxnw_e, gxnw_n = pt_road(488.0, -75.0)
    includes.append('\n    <!-- 13. 關新北路西端住宅街區大樓 (14F) -->')
    includes.append('    <include>')
    includes.append('      <name>gxn_west_end_block</name>')
    includes.append('      <uri>model://gxn_west_end_block</uri>')
    includes.append(f'      <pose>{gxnw_e:.3f} {gxnw_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 14. 關新北路角隅精品商廈 (9F)
    cp_e, cp_n = pt_road(502.0, 26.0)
    includes.append('\n    <!-- 14. 關新北路角隅精品商廈 (全聯南側, 9F, 精品手搖茶飲、生活商鋪) -->')
    includes.append('    <include>')
    includes.append('      <name>corner_boutique_plaza</name>')
    includes.append('      <uri>model://corner_boutique_plaza</uri>')
    includes.append(f'      <pose>{cp_e:.3f} {cp_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 15. 關東路口科技金融大樓 (15F)
    gct_e, gct_n = pt_road(560.0, 26.0)
    includes.append('\n    <!-- 15. 關東路口科技金融大樓 (全聯北側至關東路口, 15F, 商業銀行、金融科技中心、空中連廊) -->')
    includes.append('    <include>')
    includes.append('      <name>guandong_corner_tech_tower</name>')
    includes.append('      <uri>model://guandong_corner_tech_tower</uri>')
    includes.append(f'      <pose>{gct_e:.3f} {gct_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 16. 關東名邸與新莊商務街區 (15F)
    gdw_e, gdw_n = pt_road(588.0, -75.0)
    includes.append('\n    <!-- 16. 關東名邸與新莊商務街區 (關東路西段, 15F, 在地美食街、連鎖藥妝、騎樓商鋪) -->')
    includes.append('    <include>')
    includes.append('      <name>guandong_west_commercial_block</name>')
    includes.append('      <uri>model://guandong_west_commercial_block</uri>')
    includes.append(f'      <pose>{gdw_e:.3f} {gdw_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 17. 關東路東段南側商住大樓 (11F)
    gde_e, gde_n = pt_road(588.0, 75.0)
    includes.append('\n    <!-- 17. 關東路東段南側商住大樓 (11F) -->')
    includes.append('    <include>')
    includes.append('      <name>guandong_east_commercial_block</name>')
    includes.append('      <uri>model://guandong_east_commercial_block</uri>')
    includes.append(f'      <pose>{gde_e:.3f} {gde_n:.3f} 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 18. 關新東路北段商務大樓 (12F)
    gxen_e, gxen_n = pt_road(538.0, 105.0)
    includes.append('\n    <!-- 18. 關新東路北段商務大樓 (12F) -->')
    includes.append('    <include>')
    includes.append('      <name>gxe_north_commercial_block</name>')
    includes.append('      <uri>model://gxe_north_commercial_block</uri>')
    includes.append(f'      <pose>{gxen_e:.3f} {gxen_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 19. 新莊車站前西側商旅轉運大樓 (14F)
    xth_e, xth_n = pt_road(618.0, -32.0)
    includes.append('\n    <!-- 19. 新莊車站前西側商旅轉運大樓 (14F, 鐵道咖啡、旅客行李托運中心、商旅大廳) -->')
    includes.append('    <include>')
    includes.append('      <name>xinzhuang_transit_hotel</name>')
    includes.append('      <uri>model://xinzhuang_transit_hotel</uri>')
    includes.append(f'      <pose>{xth_e:.3f} {xth_n:.3f} 0.0 0 0 {WEST_BLDG_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 20. 新莊車站東側科技商辦大樓 (15F)
    xte_e, xte_n = pt_road(618.0, 65.0)
    includes.append('\n    <!-- 20. 新莊車站東側科技商辦大樓 (15F, 高鐵台鐵轉乘商務樞紐、研發中心) -->')
    includes.append('    <include>')
    includes.append('      <name>xinzhuang_station_east_tower</name>')
    includes.append('      <uri>model://xinzhuang_station_east_tower</uri>')
    includes.append(f'      <pose>{xte_e:.3f} {xte_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 21. 日光綠蔭花園社區與文創商場 (東側後勤內部街區補全: 南區 14F & 北區 13F)
    ngs_e, ngs_n = pt_road(145.0, 85.0)
    ngn_e, ngn_n = pt_road(295.0, 80.0)
    includes.append('\n    <!-- 21. 東側後勤服務巷弄與關新東路之間內部大型花園住宅名邸 (南區 14F & 北區 13F) -->')
    includes.append('    <include>')
    includes.append('      <name>nikko_garden_block_south</name>')
    includes.append('      <uri>model://nikko_garden_block_south</uri>')
    includes.append(f'      <pose>{ngs_e:.3f} {ngs_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    includes.append('    <include>')
    includes.append('      <name>nikko_garden_block_north</name>')
    includes.append('      <uri>model://nikko_garden_block_north</uri>')
    includes.append(f'      <pose>{ngn_e:.3f} {ngn_n:.3f} 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    # 22. 街道節點青銅公共藝術雕塑
    sc1_e, sc1_n = pt_road(16.0, 12.0)
    sc2_e, sc2_n = pt_road(340.0, -12.0)
    sc3_e, sc3_n = pt_road(582.0, 12.0)
    includes.append('\n    <!-- 22. 街道節點青銅公共藝術雕塑 (光復路口、關新二街口、關東路口) -->')
    includes.append('    <include>')
    includes.append('      <name>bronze_sculpture_guangfu</name>')
    includes.append('      <uri>model://bronze_street_sculpture</uri>')
    includes.append(f'      <pose>{sc1_e:.3f} {sc1_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    includes.append('    <include>')
    includes.append('      <name>bronze_sculpture_gx2</name>')
    includes.append('      <uri>model://bronze_street_sculpture</uri>')
    includes.append(f'      <pose>{sc2_e:.3f} {sc2_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    includes.append('      <include>')
    includes.append('      <name>bronze_sculpture_guandong</name>')
    includes.append('      <uri>model://bronze_street_sculpture</uri>')
    includes.append(f'      <pose>{sc3_e:.3f} {sc3_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}</pose>')
    includes.append('    </include>')
    
    return '\n'.join(includes)

def apply_to_world():
    print(f"Reading world file from {WORLD_PATH}...")
    with open(WORLD_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 移除先前的 Phase 8 區塊 (如果存在)
    p8_pat = r'<!-- ==================== Phase 8:.*?<!-- ==================== POI: 新竹市東區關東國民小學'
    # 或者如果已經有在末尾
    if '<!-- ==================== Phase 8:' in content:
        content = re.sub(r'<!-- ==================== Phase 8:.*?(</world>)', r'\1', content, flags=re.DOTALL)
        
    includes_str = generate_world_includes()
    
    target = '  </world>'
    if target not in content:
        print("Error: Could not find </world> tag!")
        return False
        
    new_content = content.replace(target, includes_str + "\n  </world>")
    
    print(f"Writing updated world to {WORLD_PATH}...")
    with open(WORLD_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    if os.path.exists(INSTALL_WORLD_PATH):
        try:
            with open(INSTALL_WORLD_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Synced to install directory: {INSTALL_WORLD_PATH}")
        except Exception as e:
            print(f"Notice: Could not sync install world ({e})")
            
    print("World SDF successfully updated with Phase 8 full urban infill and giant bronze sculpture!")
    return True

# Update main execution
if __name__ == "__main__":
    create_bronze_street_sculpture()
    apply_to_world()
