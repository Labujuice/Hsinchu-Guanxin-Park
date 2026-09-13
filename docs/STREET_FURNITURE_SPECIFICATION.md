# 新竹市關新商圈模組化街道家具庫與環境動態要素規格書
## (Modular Street Furniture Library Specification - Phase 6)

> **專案代號**：`Guanxin-Digital-Twin-Transformation`  
> **技術標準**：Gazebo Harmonic (SDF 1.8) + Local ENU + ODE 500Hz 物理引擎  
> **階段進度**：Phase 6 完工交付  
> **建立日期**：2026-09-13  

---

## 📌 一、 核心目標與模組化標準 (Overview & Modular Standards)

在 **Phase 6** 中，全面建立一套**高精度、低物理負載、可重複利用**之台灣都市標準街道家具庫。所有模組化資產均嚴格遵守以下標準：
1. **原點規範**：局部坐標系原點一律位於**底面幾何中心 `[0.0, 0.0, 0.0]`**，方便依據路緣、人行道與綠帶精確吸附定位。
2. **物理/視覺解耦 (Decoupled Physics)**：碰撞剛體嚴格簡化為 Box 或 Cylinder 原生幾何體，徹底杜絕 Mesh 碰撞導致的穿模或 500Hz 物理運算延遲。
3. **台灣街景特色 (Taiwanese Streetscape DNA)**：
   * 鍍鋅錐形立桿與懸臂 LED 節能路燈；
   * 台電經典墨綠色高壓雙門變電箱與黃色閃電警戒標；
   * 中華電信光纖接續箱 (Chunghwa Telecom)；
   * 地上式高光紅烤漆雙出水口消防栓；
   * 智慧路邊收費車位內停放之典型休旅車 (SUV) 與中型房車 (Sedan)。

---

## 🛋️ 二、 模組化街道家具資產清單 (Furniture Library Matrix)

| 家具類別 | 模型名稱 / URI | 尺度規格 (長x寬x高) | 外觀特徵與幾何細節 | 碰撞幾何簡化 |
| :--- | :--- | :---: | :--- | :--- |
| **懸臂 LED 路燈** | `model://street_light` | $2.0\text{m} \times 0.28\text{m} \times 7.4\text{m}$ | 熱浸鍍鋅錐形鋼管、弧形延伸 2.0m 懸臂、流線型低風阻燈頭、5000K 自發光 LED 透鏡。 | 垂直圓柱 (R=0.12m, L=7.0m) |
| **地上式消防栓** | `model://fire_hydrant` | $0.44\text{m} \times 0.36\text{m} \times 0.98\text{m}$ | 台灣標準安全紅高光琺瑯漆、圓頂蓋、頂部五角操作閥螺母、雙側黃銅出水噴嘴。 | 單一垂直圓柱 (R=0.18m, L=0.84m) |
| **電信接續箱** | `model://telecom_box` | $0.85\text{m} \times 0.55\text{m} \times 1.15\text{m}$ | 中信灰防雨金屬箱體、混凝土基座、微斜排水頂蓋、中華電信深藍企業識別標牌。 | 單一剛體 Box (0.8x0.5x1.1m) |
| **台電變電箱** | `model://taipower_box` | $1.25\text{m} \times 0.75\text{m} \times 1.35\text{m}$ | 台電標準深綠色金屬烤漆、雙開維修門、散熱百葉窗、高壓黃色閃電警戒標誌。 | 單一剛體 Box (1.2x0.7x1.3m) |
| **停放中型房車** | `model://parked_car_sedan` | $4.6\text{m} \times 1.82\text{m} \times 1.4\text{m}$ | 深灰金屬漆四門房車、傾斜前後擋風玻璃、四輪實體輪胎、頭尾燈組。 | 單一剛體 Box (4.6x1.82x1.4m) |
| **停放運動休旅車** | `model://parked_car_suv` | $4.7\text{m} \times 1.88\text{m} \times 1.75\text{m}$ | 珍珠白運動休旅車、高底盤大輪拱、車頂金屬行李架導軌、深色隱私車窗。 | 單一剛體 Box (4.7x1.88x1.6m) |

---

## 📍 三、 全域佈設拓撲與空間坐標 (Deployment Topology)

1. **關新路兩側連續路燈走廊**：
   * 東側路緣：佈設 13 盞 `street_light`，間距 45m ($s = 50\text{m} \sim 590\text{m}$)，懸臂朝西指向車道；
   * 西側路緣：佈設 13 盞 `street_light`，間距 45m ($s = 50\text{m} \sim 590\text{m}$)，懸臂朝東指向車道。
2. **關鍵十字路口消防栓**：
   * 關新一街口、關新二街口、關新北路口、關東路口東側人行道各配置 1 座 `fire_hydrant`。
3. **路邊公共電力與通訊設施**：
   * 配置 `taipower_box` 與 `telecom_box` 於主要商業門市外圍人行道綠帶，提升街道細節密度。
4. **路邊智慧車位停放車輛**：
   * 東西兩側智慧停車柱 (`smart_parking_meter_pole`) 旁，自然交替停放 4 輛轎車 (`parked_car_sedan`) 與 4 輛休旅車 (`parked_car_suv`)，呈現真實日常商圈生活場景。

---

## 🧪 四、 驗收與性能檢驗

1. **SDF 1.8 格式語法校驗**：
   ```bash
   gz sdf -k src/guanxin_sim/models/street_light/model.sdf
   gz sdf -k src/guanxin_sim/models/fire_hydrant/model.sdf
   gz sdf -k src/guanxin_sim/models/telecom_box/model.sdf
   gz sdf -k src/guanxin_sim/models/parked_car_sedan/model.sdf
   gz sdf -k src/guanxin_sim/models/parked_car_suv/model.sdf
   ```
   *結果*：全部輸出 **`Valid.`**。
2. **物理穩定性**：所有物件中心對齊地面，車輛底部平貼路面 ($Z=0.02\text{m}$)，無穿模震顫。
