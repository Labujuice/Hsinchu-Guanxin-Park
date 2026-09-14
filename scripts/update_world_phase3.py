#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Guanxin World SDF with Phase 3 Landmarks:
  - TRA Xin-Zhuang Station Building (model://xinzhuang_station at GCP 5)
  - Railway Viaduct & Pillars (model://railway_viaduct across Guanxin Rd, clearance 5.4m >= 4.8m)
  - Station Front Plaza & Taxi Bay
  - Sun Park (Guanxin Park) Landscape (120m x 91m, GCP 4, walls, walkways, lawn, pavilion, restrooms, fitness)
  - Terrazzo Slide anchored at exact park coordinates
Author: Autonomous Robotics & Simulation Team
"""

import os
import re
from generate_phase3_landmarks import generate_phase3_sdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

def main():
    with open(WORLD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove old sunlight_park and terrazzo_slide block
    # from <!-- ==================== 日光公園全區 to right before <!-- ==================== 中街現代住宅社區群
    old_park_pat = r'<!-- ==================== 日光公園全區.*?<!-- ==================== 中街現代住宅社區群'
    if not re.search(old_park_pat, content, flags=re.DOTALL):
        print("Error: Could not find old park block in world SDF!")
        return False

    content = re.sub(
        old_park_pat,
        '<!-- ==================== 中街現代住宅社區群',
        content,
        flags=re.DOTALL
    )

    # 2. Remove old placeholder xinzhuang_station_block
    # from <!-- ==================== 北端街區 (新莊車站 & 富宇君鼎 to right before <!-- ==================== 載入 Tesla Model Y
    old_station_pat = r'<!-- ==================== 北端街區 \(新莊車站 & 富宇君鼎.*?<!-- ==================== 載入 Tesla Model Y'
    if not re.search(old_station_pat, content, flags=re.DOTALL):
        print("Error: Could not find old station block in world SDF!")
        return False

    # 3. Generate Phase 3 SDF block
    phase3_sdf = generate_phase3_sdf()

    # 4. Insert Phase 3 block right before <!-- ==================== 載入 Tesla Model Y
    replacement_str = phase3_sdf + "\n\n    <!-- ==================== 載入 Tesla Model Y"
    updated_content = re.sub(
        old_station_pat,
        replacement_str,
        content,
        flags=re.DOTALL
    )

    with open(WORLD_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Successfully updated {WORLD_PATH} with Phase 3 Landmarks!")
    return True

if __name__ == '__main__':
    main()
