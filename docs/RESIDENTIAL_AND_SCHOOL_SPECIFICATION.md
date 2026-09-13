# 新竹市關新商圈數位孿生教育園區與代表性大型住商街區規格書
## (School & Major Residential Complexes Specification - Phase 4)

> **專案代號**：`Guanxin-Digital-Twin-Transformation`  
> **技術標準**：Gazebo Harmonic (SDF 1.8) + Local ENU + ODE 500Hz 物理引擎  
> **階段進度**：Phase 4 完工交付  
> **建立日期**：2026-09-13  

---

## 📌 一、 核心目標與實作範圍 (Overview & Objectives)

在 **Phase 4** 中，確立關新路全域天際線（Skyline）與自然陽光下的真實建築立體陰影（Dynamic Shadows）。完成東南側教育文教核心——**新竹市立關埔國小**，以及關新路西側與北側 4 座最具指標性的大型豪宅社區大樓之高真實度數位建模。

---

## 🏫 二、 關埔國小校園 (`model://guanpu_elementary_school`)

* **模型 URI**：`model://guanpu_elementary_school`
* **空間坐標**：位於關新東路以東文教用地 (`pose: 296.56 219.20 0.0 0 0 1.34512`)。
* **校園規模**：佔地 $140.0\text{m} \times 110.0\text{m}$（約 1.54 公頃）。
* **建築特色與田中央有機聚落語彙**：
  * **有機聚落校舍群**：
    * 教學大樓 A 棟（4層樓，高 15m）：清水模主牆面、南向木紋垂直遮陽格柵（Timber Slats）、斜面深灰金屬折板屋頂。
    * 教學大樓 B 棟（3層樓，高 12m）：頂樓配置戶外自然觀察生態綠化露台。
    * 行政圖書資訊中心（2層樓，高 8.5m）：大面積採光落地玻璃帷幕。
    * 室內多功能體育館（挑高 12m）：大跨度圓弧型拱頂。
  * **操場與運動場系統**：
    * 200 米標準紅色 PU 橢圓田徑跑道，劃設白色跑道分道線。
    * 跑道中央設有 $52\text{m} \times 28\text{m}$ 天然草皮足球與綜合活動草坪。
    * 戶外多功能球場（藍綠雙色耐磨地坪）。
  * **校門與防護邊界**：
    * 現代穿透式墨綠色金屬格柵圍牆（高 2.2m），消除傳統學校封閉壓迫感。
    * 校門警衛傳達室與花崗石「新竹市立關埔國民小學」金字校名石碑。

---

## 🏙️ 三、 四大指標型住商大樓規格 (Major Residential Complexes)

| 建物名稱 | 樓層與高度 | 幾何佔地 (長x寬) | 建築風格與立面語彙 | 空間坐標 `[E, N, U]` (Local ENU) |
| :--- | :---: | :---: | :--- | :--- |
| **東京中城 (Tokyo Roppongi)** | 雙塔 24F (72m) | $74\text{m} \times 36\text{m}$ | 現代雙塔、挑高 7.5m 大理石精品基座、垂直深灰金屬遮陽格柵、深凹玻璃陽台、頂樓冠頂框架 | `[+57.99, +413.51, 0.0]` (日光公園正對面西側) |
| **一品大觀 (Yipin Daguan)** | 22F (68m) | $84\text{m} \times 36\text{m}$ | 新古典崗石名邸、挑高 5.4m 迎賓車道大門 (Porte-Cochère) 配 4 根古典羅馬石柱、崗石基座與飛簷 | `[+28.68, +285.83, 0.0]` (關新路西側中南段) |
| **昌益丹麥/芬蘭/挪威** | 15F (48m) | $64\text{m} \times 35\text{m}$ | 現代住商社區、1F 挑高深凹連續騎樓走廊 (寬 3.8m，大圓柱列)、店鋪玻璃門面與幾何陽台 | `[-21.95, +56.34, 0.0]` (關新路西側南段) |
| **富宇君鼎 (Fu Yu Jun Ding)** | 24F (78m / 冠頂82m) | $52\text{m} \times 34\text{m}$ | 站前地標高層豪宅、石材迎賓基座、全景景觀陽台、頂部鋼構天際線夜間自體發光冠頂 (Sky Crown) | `[+92.17, +553.41, 0.0]` (新莊車站前廣場西北側) |

---

## ☀️ 四、 陰影層次與天際線效果 (Skyline & Shadows)

1. **視覺與碰撞分離 (Decoupled Collision & Visual)**：
   * 所有超高層大樓碰撞體均簡化為外擴邊界剛體 Box，避免高空細節面造成 ODE 物理引擎負擔；
   * 視覺體具備真實的深凹騎樓（3.8m）、陽台進深（1.2m）與百葉格柵，在 Gazebo Harmonic 的定向太陽光源照射下，於關新路與人行道上投射出層次極其豐富的實時斜向陰影。
2. **街道封閉感與尺度感 (Enclosure Ratio)**：
   * 關新路西側由 48m ~ 72m 的高樓天際線連續排列，東側由日光公園與 1F~5F 的商業街廓開闊展開，精確重現新竹關新商圈特有之「西側現代高樓豪宅、東側綠意陽光公園」都市空間感。

---

## 🧪 五、 驗收與測試數據

1. **Gazebo Harmonic SDF 驗證**：
   ```bash
   gz sdf -k .../guanxin.sdf
   gz sdf -k .../guanpu_elementary_school/model.sdf
   gz sdf -k .../tokyo_roppongi_towers/model.sdf
   gz sdf -k .../yipin_daguan_complex/model.sdf
   gz sdf -k .../changyi_residential_block/model.sdf
   gz sdf -k .../fuyu_junding_tower/model.sdf
   ```
   *結果*：全部回傳 **`Valid.`**。
2. **ROS 2 編譯測試**：
   ```bash
   colcon build --symlink-install
   ```
   *結果*：`Finished <<< guanxin_sim [1.69s]`，零 Error。
3. **無縫接合**：
   * 大樓基座與關新路西側人行道零破面、零縫隙接合。
