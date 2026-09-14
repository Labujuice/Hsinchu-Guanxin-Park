#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve all remaining 3 road encroachments and 7 building overlaps.
"""

import os, sys, re, math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

BEARING_DEG = 12.930438
BEARING_RAD = math.radians(BEARING_DEG)
ROAD_YAW = math.radians(90.0 - BEARING_DEG)
CROSS_YAW = ROAD_YAW - math.radians(90.0)
WEST_BLDG_YAW = CROSS_YAW - math.radians(90.0)
U_ROAD = (math.sin(BEARING_RAD), math.cos(BEARING_RAD))
U_PERP = (math.cos(BEARING_RAD), -math.sin(BEARING_RAD))
def pt_road(s, perp):
    return s * U_ROAD[0] + perp * U_PERP[0], s * U_ROAD[1] + perp * U_PERP[1]

# 1. Update railway_viaduct model.sdf
viaduct_sdf_path = os.path.join(REPO_DIR, "src", "guanxin_sim", "models", "railway_viaduct", "model.sdf")
with open(viaduct_sdf_path, "r", encoding="utf-8") as f:
    v_content = f.read()

# Shift piers in X by -1.5m so they clear Guanxin road completely
v_content = re.sub(
    r'<collision name="pier_west_col">\s*<pose>[^<]+</pose>\s*<geometry><box><size>[^<]+</size></box></geometry>',
    '<collision name="pier_west_col">\n        <pose>-1.6 -12.5 2.7 0 0 0</pose>\n        <geometry><box><size>1.6 2.2 5.4</size></box></geometry>',
    v_content
)
v_content = re.sub(
    r'<collision name="pier_east_col">\s*<pose>[^<]+</pose>\s*<geometry><box><size>[^<]+</size></box></geometry>',
    '<collision name="pier_east_col">\n        <pose>-1.6 12.5 2.7 0 0 0</pose>\n        <geometry><box><size>1.6 2.2 5.4</size></box></geometry>',
    v_content
)
# Shorten girder deck collision to clear station core column
v_content = re.sub(
    r'<collision name="girder_deck_col">\s*<pose>[^<]+</pose>\s*<geometry><box><size>[^<]+</size></box></geometry>',
    '<collision name="girder_deck_col">\n        <pose>-1.0 0 6.1 0 0 0</pose>\n        <geometry><box><size>57.0 10.5 1.4</size></box></geometry>',
    v_content
)
with open(viaduct_sdf_path, "w", encoding="utf-8") as f:
    f.write(v_content)
print("Updated railway_viaduct/model.sdf")

# 2. Update changyi_residential_block/model.sdf park_ground_col
changyi_sdf_path = os.path.join(REPO_DIR, "src", "guanxin_sim", "models", "changyi_residential_block", "model.sdf")
with open(changyi_sdf_path, "r", encoding="utf-8") as f:
    c_content = f.read()
c_content = re.sub(
    r'<collision name="park_ground_col">\s*<pose>[^<]+</pose>\s*<geometry><box><size>[^<]+</size></box></geometry>',
    '<collision name="park_ground_col">\n        <pose>20.0 75.0 0.05 0 0 0</pose>\n        <geometry><box><size>24.0 68.0 0.10</size></box></geometry>',
    c_content
)
with open(changyi_sdf_path, "w", encoding="utf-8") as f:
    f.write(c_content)
print("Updated changyi_residential_block/model.sdf")

# 3. Update world file
with open(WORLD_PATH, "r", encoding="utf-8") as f:
    w_content = f.read()

# Fix cathay_ramp_col pose to match visual pose (73.419, 258.116)
w_content = re.sub(
    r'<collision name="cathay_ramp_col"><pose>[^<]+</pose>',
    '<collision name="cathay_ramp_col"><pose>73.419 258.116 0.180 0 0 1.34512</pose>',
    w_content
)

# Fix plaza_deck_col size from 30x24 to 30x14, centered at s = 632.0 (pose 168.212 609.803)
w_content = re.sub(
    r'<collision name="plaza_deck_col"><pose>[^<]+</pose><geometry><box><size>[^<]+</size></box></geometry></collision>',
    '<collision name="plaza_deck_col"><pose>168.212 609.803 0.075 0 0 -0.22568</pose><geometry><box><size>30.0 14.0 0.15</size></box></geometry></collision>',
    w_content
)

# In Phase 8 block:
# a) Remove xinzhuang_transit_hotel (conflicts with diagonal Guandong Rd seg 13)
w_content = re.sub(
    r'\s*<!-- 14\. 新莊車站前西側商旅轉運大樓.*?<include>\s*<name>xinzhuang_transit_hotel</name>.*?</include>',
    '',
    w_content,
    flags=re.DOTALL
)

# b) Relocate bronze_sculpture_guangfu to corner plaza at s = 14.0, perp = 13.0
bgf_e, bgf_n = pt_road(14.0, 13.0)
w_content = re.sub(
    r'(<include>\s*<name>bronze_sculpture_guangfu</name>\s*<uri>model://bronze_street_sculpture</uri>\s*<pose>)[^<]+(</pose>\s*</include>)',
    f'\\g<1>{bgf_e:.3f} {bgf_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}\\g<2>',
    w_content
)

# c) Relocate bronze_sculpture_gx2 to Nikko Park entrance corner plaza at s = 340.0, perp = 15.0
bgx2_e, bgx2_n = pt_road(340.0, 15.0)
w_content = re.sub(
    r'(<include>\s*<name>bronze_sculpture_gx2</name>\s*<uri>model://bronze_street_sculpture</uri>\s*<pose>)[^<]+(</pose>\s*</include>)',
    f'\\g<1>{bgx2_e:.3f} {bgx2_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}\\g<2>',
    w_content
)

# d) Relocate bronze_sculpture_xinzhuang to station plaza at s = 630.0, perp = 14.0
bxz_e, bxz_n = pt_road(630.0, 14.0)
w_content = re.sub(
    r'(<include>\s*<name>bronze_sculpture_xinzhuang</name>\s*<uri>model://bronze_street_sculpture</uri>\s*<pose>)[^<]+(</pose>\s*</include>)',
    f'\\g<1>{bxz_e:.3f} {bxz_n:.3f} 0.20 0 0 {ROAD_YAW:.5f}\\g<2>',
    w_content
)

with open(WORLD_PATH, "w", encoding="utf-8") as f:
    f.write(w_content)
print("Updated world file successfully!")

