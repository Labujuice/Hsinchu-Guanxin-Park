# 新竹市關新商圈核心連鎖商圈與特色 POI 組合技規格書
## (Core Commercial Establishments & POIs Specification - Phase 5)

> **專案代號**：`Guanxin-Digital-Twin-Transformation`  
> **技術標準**：Gazebo Harmonic (SDF 1.8) + Local ENU + ODE 500Hz 物理引擎  
> **階段進度**：Phase 5 完工交付  
> **建立日期**：2026-09-13  

---

## 📌 一、 核心目標與實作原則 (Overview & Principles)

在 **Phase 5** 中，全面落實「**組合技建模標準 (Combo Technique Standard)**」，徹底摒棄無景深平面貼圖，為關新商圈注入高度真實的商業繁榮度與生活機能。重點構建新竹關新商圈極具代表性之指標門市與設施：
1. **全聯福利中心 (PX Mart)**：雙層超市旗艦量體、企業雙色橫幅、自體發光燈箱、生鮮進貨卸貨月台與手推車收納棚。
2. **鼎盛十里鍋物 (Dingsheng Shili Hotpot)**：日式禪風黑木旗艦店、大型和風發光燈籠光雕、出簷黑瓦歇山頂、迎賓水景鏡池與石階步道。
3. **7-ELEVEN 統一超商門市**：經典橘綠紅三色飾帶、直立式高空發光招牌塔、4000K 暖白透光玻璃櫥窗、獨立 ATM 服務專區。
4. **關新智慧收費停車場 (Paid Surface Parking Lot)**：真實瀝青地面、標準停車格標線、車牌辨識立柱 (ALPR)、黑黃條紋電動起落桿、自動繳費機亭、高燈桿投光照明與停放車輛。
5. **昌益一品大觀 (Yipin Daguan Complex)**：雙塔 22 層新古典石材豪宅、挑高愛奧尼克迎賓柱廊車道大門 (Porte-Cochère)。

---

## 🏬 二、 Phase 5 商業 POI 幾何與規格參數 (Commercial POIs Matrix)

| 建築 / 設施名稱 | 模型 URI | 空間尺度 (長x寬x高) | 關鍵建築語彙與機能細節 | 坐標 `[E, N, U]` / Yaw |
| :--- | :--- | :---: | :--- | :--- |
| **7-ELEVEN 關新門市** | `model://convenience_store_711` | $16.0\text{m} \times 12.0\text{m} \times 4.8\text{m}$ | 經典橘綠紅三色彩帶招牌、7 米立式雙面發光燈箱柱、4000K 暖白室內穿透照明、自動玻璃推拉門、獨立 ATM 提款專區。 | `[+126.90, +463.35, 0.0]`<br>$\text{yaw}=1.34512$ |
| **全聯福利中心** (關新店) | `model://px_mart_store` | $32.0\text{m} \times 22.0\text{m} \times 8.2\text{m}$ | 企業深藍與紅白高對比橫幅看板、自體發光 PX MART 燈箱與同心圓標誌、落地採光櫥窗、懸挑鋼構雨遮、不銹鋼防撞柱、戶外購物手推車收納棚、後方物流高架裝卸貨月台與雙樘金屬工業捲門。 | `[+140.87, +506.32, 0.0]`<br>$\text{yaw}=1.34512$ |
| **鼎盛十里鍋物旗艦店** | `model://dingsheng_shili_restaurant` | $38.0\text{m} \times 28.0\text{m} \times 10.2\text{m}$ | 燒杉板碳化黑木立面、水平木紋遮陽格柵、深灰黑瓦雙層出簷屋頂、挑高實木迎賓大門、大型雙座暖黃和風發光燈籠（"鼎盛十里"）、黑色鏡面迎賓水景池與花崗石步道、庭園造景黑松。 | `[+231.54, +373.92, 0.0]`<br>$\text{yaw}=1.34512$ |
| **智慧地面收費停車場** | `model://paid_parking_lot` | $42.0\text{m} \times 30.0\text{m} \times 7.5\text{m}$ | 實體瀝青基座、18 格標準劃線車位、車道黃色導引線、安全島、入口 ALPR 車牌辨識鏡頭柱、黃黑相間升降柵欄機、綠色 LED 車位指示看板、防雨自助繳費亭、2 座 7.5m 高桅桿 LED 投光燈、停放休旅車/轎車。 | `[+244.97, +432.40, 0.0]`<br>$\text{yaw}=1.34512$ |
| **昌益一品大觀** | `model://yipin_daguan_complex` | $84.0\text{m} \times 36.0\text{m} \times 68.0\text{m}$ | 雙塔 22 層豪宅、新古典厚重石材基座與腰帶分段線條、4 根大型羅馬圓柱挑高迎賓車道大迴廊、頂樓歐式冠頂框架。 | `[+260.74, +492.14, 0.0]`<br>$\text{yaw}=1.34512$ |

---

## 🛠️ 三、 物理碰撞解耦與渲染效能優化 (Optimization Strategy)

1. **碰撞幾何全面簡化 (Decoupled Collision Primitives)**：
   * 所有裝飾性燈籠、水池倒影、屋頂空調機、手推車、立旗等細節皆設為純 `<visual>`，無碰撞負擔；
   * 主建築剛體碰撞嚴格簡化為 Box/Cylinder 複合體，徹底消除網格碰撞帶來的 ODE 步進延遲。
2. **PBR 材質與發光光雕 (PBR & Emissive Channels)**：
   * 招牌與室內採光引入物理發光材質 (`<emissive>`)，在夜晚或黃昏環境下呈現逼真自發光效果；
   * 玻璃與水景採用高透光帶微折射材質，營造真實空間感。

---

## 🧪 四、 驗收與測試

1. **SDF 1.8 格式校驗**：
   ```bash
   gz sdf -k src/guanxin_sim/models/px_mart_store/model.sdf
   gz sdf -k src/guanxin_sim/models/dingsheng_shili_restaurant/model.sdf
   gz sdf -k src/guanxin_sim/models/convenience_store_711/model.sdf
   gz sdf -k src/guanxin_sim/models/paid_parking_lot/model.sdf
   gz sdf -k src/guanxin_sim/models/yipin_daguan_complex/model.sdf
   ```
   *結果*：全部輸出 **`Valid.`**。
2. **全域世界檔關聯性**：
   * 各 POI 坐標嚴格依據路緣與人行道邊界對齊，無任何破面與重疊。
