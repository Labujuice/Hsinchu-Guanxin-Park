#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Guanxin World SDF with Phase 4 Education & Major Residential Complexes:
  - Guanpu Elementary School Campus (model://guanpu_elementary_school)
  - Tokyo Roppongi Luxury Twin Towers 24F (model://tokyo_roppongi_towers)
  - Yipin Daguan Neoclassical Complex 22F (model://yipin_daguan_complex)
  - Changyi Danish/Finland/Norway 15F with Continuous Arcade (model://changyi_residential_block)
  - Fu Yu Jun Ding Landmark 24F with Sky Crown (model://fuyu_junding_tower)
Author: Autonomous Robotics & Simulation Team
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

ROAD_YAW = 1.34512
CROSS_YAW = -0.22568

def generate_phase4_block():
    lines = []
    lines.append('    <!-- ==================== Phase 4: 教育園區與代表性大型住商豪宅街區 ==================== -->')
    lines.append('    <!-- 確立街區天際線與真實建築陰影：關埔國小、東京中城(24F)、一品大觀(22F)、昌益丹麥芬蘭(15F)、富宇君鼎(24F) -->')

    # 1. 昌益丹麥 / 芬蘭社區 (15F 現代社區, 挑高連續騎樓與大圓柱)
    lines.append('\n    <!-- 1. 昌益丹麥 / 芬蘭 / 挪威現代住宅社區 (15層樓, 48m, 1F 挑高深凹連續騎樓走廊與圓柱列) -->')
    lines.append('    <include>')
    lines.append('      <name>changyi_residential_block</name>')
    lines.append('      <uri>model://changyi_residential_block</uri>')
    lines.append(f'      <pose>-21.95 56.34 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 2. 一品大觀新古典豪宅 (22F, 68m, 崗石名邸, 挑高迎賓車道大門)
    lines.append('\n    <!-- 2. 一品大觀新古典崗石名邸 (22層樓, 68m, 挑高迎賓車道大門 Porte-Cochère, 崗石厚重基座) -->')
    lines.append('    <include>')
    lines.append('      <name>yipin_daguan_complex</name>')
    lines.append('      <uri>model://yipin_daguan_complex</uri>')
    lines.append(f'      <pose>28.68 285.83 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 3. 東京中城現代雙塔豪宅 (24F, 72m, 日光公園正對面, 挑高大理石基座, 垂直遮陽格柵)
    lines.append('\n    <!-- 3. 東京中城雙塔現代豪宅地標 (24層樓, 72m, 日光公園西側對街, 挑高大理石精品商鋪基座, 垂直金屬格柵) -->')
    lines.append('    <include>')
    lines.append('      <name>tokyo_roppongi_towers</name>')
    lines.append('      <uri>model://tokyo_roppongi_towers</uri>')
    lines.append(f'      <pose>57.99 413.51 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 4. 富宇君鼎高層豪宅 (24F, 78m, 天際線冠頂 82m, 關新北路站前地標)
    lines.append('\n    <!-- 4. 富宇君鼎 24 層天際線豪宅地標 (高 78m, 發光造型冠頂 82m, 新莊車站迎賓廣場西北側) -->')
    lines.append('    <include>')
    lines.append('      <name>fuyu_junding_tower</name>')
    lines.append('      <uri>model://fuyu_junding_tower</uri>')
    lines.append(f'      <pose>92.17 553.41 0.0 0 0 {CROSS_YAW:.5f}</pose>')
    lines.append('    </include>')

    # 5. 關埔國小校園 (有機聚落式校舍、200m跑道操場、體育館、綠化露台)
    lines.append('\n    <!-- 5. 新竹市立關埔國小校園 (有機低矮聚落校舍、木紋清水模立面、200m 紅土 PU 跑道操場、穿透式金屬格柵圍牆) -->')
    lines.append('    <include>')
    lines.append('      <name>guanpu_elementary_school</name>')
    lines.append('      <uri>model://guanpu_elementary_school</uri>')
    lines.append(f'      <pose>296.56 219.20 0.0 0 0 {ROAD_YAW:.5f}</pose>')
    lines.append('    </include>')

    return '\n'.join(lines)

def main():
    with open(WORLD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Locate old west_side_blocks
    old_west_pat = r'<!-- ==================== 西側街區群 \(West Side Blocks:.*?<!-- ==================== Phase 3: 重點交通與公共休閒地標建模'
    if not re.search(old_west_pat, content, flags=re.DOTALL):
        print("Error: Could not locate old west_side_blocks in world SDF!")
        return False

    phase4_block = generate_phase4_block()
    replacement_str = phase4_block + "\n\n    <!-- ==================== Phase 3: 重點交通與公共休閒地標建模"

    updated_content = re.sub(
        old_west_pat,
        replacement_str,
        content,
        flags=re.DOTALL
    )

    with open(WORLD_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Successfully updated {WORLD_PATH} with Phase 4 Education & Residential Landmarks!")
    return True

if __name__ == '__main__':
    main()
