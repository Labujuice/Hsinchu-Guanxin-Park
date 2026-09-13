# 新竹市關新商圈數位孿生重點地標建築與公共設施規格書
## (Key Landmarks & Public Infrastructure Specification - Phase 3)

> **專案代號**：`Guanxin-Digital-Twin-Transformation`  
> **技術標準**：Gazebo Harmonic (SDF 1.8) + Local ENU + ODE 500Hz 物理引擎  
> **階段進度**：Phase 3 完工交付  
> **建立日期**：2026-09-13  

---

## 📌 一、 核心目標與實作範圍 (Overview & Objectives)

在 **Phase 3** 中，依據地理基準（Local ENU 原點於光復路口、關新路方位角 $12.93^\circ$）完成數位孿生全區三大重點公共交通與遊憩地標的精確三維數位建模：
1. **台鐵新莊車站大樓 (TRA Xin-Zhuang Station)**：北側交通門戶樞紐。
2. **台鐵高架鐵路跨街橋梁與橋墩 (Railway Viaduct & Pillars)**：橫跨關新路之高架軌道結構，確保橋下淨空 $\ge 4.8\text{m}$。
3. **關新公園（日光公園）全區景觀與遊憩設施 (Sun Park Landscape)**：面積 $120\text{m} \times 91\text{m}$ 之公共休閒核心綠帶。

---

## 🚉 二、 台鐵新莊車站大樓 (`model://xinzhuang_station`)

* **模型 URI**：`model://xinzhuang_station`
* **空間坐標**：`GCP 5` 站體核心 (依真實地圖校準 Local ENU `[E: +372.58, N: +617.28, U: 0.0]`)，走向對齊鐵路廊道軸線 (`yaw = -0.2257 rad`)。
* **建築量體與結構**：
  * **1F 地面售票大廳 (Concourse)**：長 $52\text{m} \times$ 寬 $22\text{m} \times$ 高 $4.4\text{m}$。
    * 清水模混凝土結構大柱、青透採光玻璃帷幕（帶深色鋁合金窗框）。
    * 挑高懸挑鋼構迎賓雨遮（寬 $32\text{m}$，挑出 $5.5\text{m}$，高度 $4.0\text{m}$）。
    * **經典台鐵發光招牌**：深藍底板、立體台鐵局徽與白色「新莊車站 TRA Xin-Zhuang Station」自體發光字。
    * 自動售票機櫃與出入驗票閘門。
  * **2F 高架月台層 (Elevated Platform & Tracks)**：高出地面 $8.0\text{m}$，長 $76\text{m} \times$ 寬 $18\text{m}$。
    * 鋼筋混凝土厚重連續箱梁橋板、半透玻璃防護安全欄杆、月台黃色警戒停等線、視障引導磚。
    * 雙向南北軌道（道碴碎石床、混凝土軌枕、標準 $1067\text{mm}$ 鋼軌）。
    * 兩座東西向垂直核心筒（大理石電梯井與疏散階梯）。
  * **月台大跨度鋼構拱形雨棚 (Steel Truss Curved Canopy)**：總高達 $14.5\text{m}$。
    * Y 型圓柱鋼構支撐柱、銀灰金屬波浪烤漆屋面、月台發光站名燈箱。
* **站前迎賓廣場與計程車排班彎道 (`xinzhuang_station_plaza`)**：
  * 鋪設 $42\text{m} \times 26\text{m}$ 灰色花崗岩地磚廣場 (`[E: +343.34, N: +624.00, U: 0.075, yaw = -0.2257 rad]`)，包含綠化植栽花台與車站門前旗桿座，正對關新路東彎道終點。

---

## 🌉 三、 台鐵高架鐵路橋梁與橋墩 (`model://railway_viaduct`)

* **模型 URI**：`model://railway_viaduct`
* **空間坐標**：橫跨關新路東彎道延伸段與關東路交會點上方 (中心 `[E: +338.46, N: +625.11, U: 0.0]`, `yaw = -0.2257 rad`)。
* **工程與物理規格**：
  * **橋下淨空 (Underbridge Clearance)**：**$5.40\text{ 米}$**（嚴格高於法規要求的 $\ge 4.8\text{ 米}$ 限高標準，大型自駕巴士、消防車與貨櫃車安全通過無穿模）。
  * **雙柱式橋墩 (Concrete Pier Columns)**：兩座長 $2.4\text{m} \times$ 寬 $2.2\text{m} \times$ 高 $5.4\text{m}$ 鋼筋混凝土橋墩，精確退縮至關新路兩側人行道外側 ($Y = \pm 12.5\text{m}$)，零侵入車道與人行道。
  * **T 型蓋梁與連續預力混凝土箱梁 (Box Girder)**：總跨度 $60.0\text{m}$，橋寬 $10.5\text{m}$，梁深 $1.4\text{m}$。
  * **梁底防撞警示系統**：
    * 橋梁跨越關新路車道正面設置長 $18.0\text{m}$ 黃黑相間反光警示斜紋貼條。
    * 車道正上方設置直徑 $0.9\text{m}$ 紅白雙色「限高 4.8 公尺」警示圓盤。
  * **高架防噪隔音牆 (Acoustic Noise Barriers)**：
    * 橋面兩側設置高 $2.2\text{m}$ 複合隔音牆（下段金屬微孔吸音板 + 上段鋼化壓克力透明採光窗）。
  * **電車線設備**：H 型鋼電車線支柱與懸臂支撐架。

---

## 🌳 四、 關新公園（日光公園）全區景觀深化 (`sun_park_landscape`)

* **佔地規模**：長 $120.0\text{m} \times$ 寬 $91.0\text{m}$（面積約 $10,920\text{ m}^2$ / 約 1.1 公頃）。
* **地理位置**：`GCP 4` 公園核心 (`24.7856420°N, 121.0225100°E`, Local ENU `[E: +155.23, N: +420.66]`)。
* **細部景觀系統配置**：
  1. **四周低矮洗石子花台圍牆 (Perimeter Planter Walls)**：
     * 高 $0.45\text{m}$，寬 $0.6\text{m}$，採用洗石子材質，圍塑公園邊界並提供散步者隨時歇腳。
     * 四角均留設寬闊入口無障礙動線。
  2. **西南角地標名牌石碑 (Park Monument)**：
     * 位於星巴克十字路口斜對角入口，深色花崗岩基座嵌黃金字體「新竹市東區關新公園 (日光公園)」名牌。
  3. **環園步道與中央主穿越道 (Walkways)**：
     * 外環設置寬 $2.8\text{m}$ 經典紅磚透水散步道（全長逾 380 米）。
     * 中央設置貫穿東西之寬 $3.2\text{m}$ 棕灰大地磚林蔭休閒主步道。
  4. **中央陽光大草坪與地形微丘 (Central Sun Lawn & Topo Mounds)**：
     * 開闊 $75\text{m} \times 52\text{m}$ 社區大草坪。
     * 東南側草坡微丘（高 $0.7\text{m}$）與西北側休閒小丘（高 $0.6\text{m}$），形成層次豐富之自然起伏地貌。
  5. **現代景觀休憩涼亭 (Rest Pavilion at GCP 4)**：
     * 長 $10\text{m} \times$ 寬 $8\text{m}$，四根防鏽深色鋼管立柱、木紋百葉格柵採光遮陽棚、內建天然柚木景觀長椅。
  6. **現代公園景觀公廁 (Public Restroom Building)**：
     * 位於公園東北角，長 $12.0\text{m} \times$ 寬 $7.5\text{m} \times$ 高 $4.0\text{m}$。
     * 清水模主體立面、木紋通風防視格柵、挑高平屋頂。
  7. **標誌性磨石子大溜滑梯 (`model://terrazzo_slide`)**：
     * 重新校準錨定至兒童遊憩專區地面（$s = 406\text{m}, \text{offset} = +30\text{m}$），滑梯正面朝向公園中央大草坪。
     * 周圍鋪設 $24\text{m} \times 18\text{m}$ 藍黃雙色高彈性橡膠吸震安全地墊。
  8. **兒童遊戲與體健運動設施區 (Playground & Fitness Station)**：
     * 雙人安全盪鞦韆組（紅灰鋼管架、橡膠懸掛座椅）。
     * 社區體健雙人漫步機與轉腰器運動區。

---

## 🧪 五、 驗收與測試數據

1. **Gazebo Harmonic SDF 驗證**：
   ```bash
   gz sdf -k /ros2_ws/src/guanxin_sim/worlds/guanxin.sdf
   gz sdf -k /ros2_ws/src/guanxin_sim/models/xinzhuang_station/model.sdf
   gz sdf -k /ros2_ws/src/guanxin_sim/models/railway_viaduct/model.sdf
   ```
   *結果*：全部回傳 **`Valid.`**。
2. **ROS 2 系統編譯**：
   ```bash
   colcon build --symlink-install
   ```
   *結果*：`Finished <<< guanxin_sim [1.52s]`，零 Error。
3. **物理淨空測試**：
   * 鐵路橋梁橫跨關新路主幹道梁底淨高為 $5.4\text{m}$，路面車輛通過零穿模。
