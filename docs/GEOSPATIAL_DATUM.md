# 新竹市關新商圈數位孿生地理基準與座標系統規格書
## (Geospatial Datum & Rigid Coordinate System Specification)

> **專案代號**：`Guanxin-Digital-Twin-Transformation`  
> **技術標準**：WGS84 (EPSG:4326) / Local ENU (East-North-Up) / Gazebo Harmonic (SDF 1.8)  
> **基準版本**：v1.0.0 (Phase 1 基準確立)  
> **建立日期**：2026-09-13  

---

## 📌 一、 概述與標定宗旨 (Overview & Principles)

在大型智慧城市與高真實度自駕模擬（Digital Twin Simulation）中，幾何模型的準確度取決於嚴謹的空間幾何參考框架。為解決過往模型坐標系與真實衛星遙測數據（GIS / OpenStreetMap / Google Earth）之間的縮放、旋轉偏轉與原點漂移問題，本計畫在 **Phase 1** 明確建立統一的 **地理基準原點 (Geodetic Datum)** 與 **局部東北天坐標系 (Local ENU Frame)**。

### 核心原則：
1. **零漂移世界原點 (Zero-Drift Origin)**：以新竹市東區關新商圈南側門戶——光復路一段與關新路口交匯中心為坐標系 `(0, 0, 0)`。
2. **局部東北天 (Local ENU)**：
   * $+X$ 軸指向正東方 (East)。
   * $+Y$ 軸指向正北方 (North)。
   * $+Z$ 軸垂直向上 (Up, 橢球面法線向上)。
3. **高精度剛體變換 (Sub-Millimeter Rigid Transform)**：採用標準 WGS84 參考橢球體與 ECEF (地心地固) 旋轉矩陣，確保全區 58 公頃範圍內數值轉換誤差 $< 0.001\text{ mm}$。

---

## 🌐 二、 基準原點 (Datum Origin) 規格

| 參數項目 | 規格數值 | 說明 |
| :--- | :--- | :--- |
| **基準點標號** | **Point 1 (P1) / GCP 1** | 光復路一段與關新路口交會中心 |
| **地理坐標 (度分秒 DMS)** | `24°46'54.64"N, 121°01'15.51"E` | 衛星精測中心基準 |
| **十進位緯度 (Latitude)** | `24.78184444° N` | 8 位小數點精確度（約 1.1mm 解析度） |
| **十進位經度 (Longitude)** | `121.02097500° E` | 8 位小數點精確度（約 1.0mm 解析度） |
| **基準海拔 (Elevation)** | `35.00 m` (公尺) | 台灣高程基準 (TWVD2001) / 橢球高 |
| **Gazebo 世界坐標** | `[X: 0.000, Y: 0.000, Z: 0.000]` | 剛體轉換原點 $(0, 0, 0)$ |
| **主幹道走勢方位角 (Bearing)** | `12.93° ~ 14.03°` (正北偏東) | 關新路主軸朝向台鐵新莊車站 |

---

## 🗺️ 三、 邊界多邊形 (58 公頃範圍) 頂點映射表

目標數位孿生多邊形範圍由以下 5 個控制頂點封閉包圍：

| 頂點編號 | 邊界名稱與重要特徵 | WGS84 經緯度 (度分秒) | 十進位經緯度 | Local ENU 坐標 `[E, N, U]` (公尺) |
| :---: | :--- | :--- | :--- | :--- |
| **P1** | **南界（原點）**：光復路一段 / 關新路交叉口 | `24°46'54.64"N, 121°01'15.51"E` | `24.7818444°N, 121.0209750°E` | `[   +0.00,    +0.00,  +0.00]` |
| **P2** | **東界**：關新東路 / 埔頂路口與東側商住交界 | `24°47'10.48"N, 121°01'28.57"E` | `24.7862444°N, 121.0246028°E` | `[ +366.86,  +487.39,  -0.83]` |
| **P3** | **東北界**：台鐵新莊車站東側 / 關新北路口外圍 | `24°47'25.79"N, 121°01'24.04"E` | `24.7904972°N, 121.0233444°E` | `[ +239.60,  +958.47,  -2.58]` |
| **P4** | **西北界**：台鐵高架鐵路廊道西側 / 關新北路外圍 | `24°47'25.82"N, 121°01'07.91"E` | `24.7905056°N, 121.0188639°E` | `[ -213.48,  +959.40,  -2.28]` |
| **P5** | **西界**：新莊街 / 關新西街延伸社區聚落交會處 | `24°47'02.78"N, 121°00'55.31"E` | `24.7841056°N, 121.0153639°E` | `[ -567.43,  +250.48,  -0.53]` |

### 多邊形幾何特徵統計：
* **多邊形涵蓋面積**：$580,123.6\text{ m}^2$（約 **58.01 公頃** / **175,487 坪**）。
* **東西向跨度 (East-West Width)**：$934.29\text{ m}$（$-567.43\text{m} \sim +366.86\text{m}$）。
* **南北向跨度 (South-North Length)**：$959.40\text{ m}$（$0.00\text{m} \sim +959.40\text{m}$）。
* **地形高差**：由南向北（光復路往台鐵新莊車站）微幅緩降約 $2.5\text{m}$。

---

## 🎯 四、 地面控制點 (GCP) 目錄與校準坐標

為確保後續各階段道路網、大型建築、公園地景與街道家具組裝時具備絕對精準的對位錨點，設立 7 組核心地面控制點 (Ground Control Points)：

| GCP 編號 | 控制點名稱與現場地貌特徵 | WGS84 十進位經緯度 | 海拔 | Local ENU 坐標 `[X(東), Y(北), Z(上)]` | 實體校準功能 |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **GCP 1** | **光復路 / 關新路口中心 (Datum Origin)** | `24.7818444°N, 121.0209750°E` | 35.0m | `[   +0.00,    +0.00,  +0.00]` | 世界基準原點，車輛起始點 |
| **GCP 2** | **關新路 / 關新一街口中心** | `24.7826180°N, 121.0211680°E` | 34.8m | `[  +19.52,   +85.69,  -0.20]` | 中南段商業十字路口基準 |
| **GCP 3** | **關新路 / 關新二街口（星巴克日光門市角）** | `24.7848760°N, 121.0217340°E` | 34.2m | `[  +76.75,  +335.81,  -0.81]` | 核心商圈十字路口、45度切角建築 |
| **GCP 4** | **關新公園（日光公園）中心休憩涼亭** | `24.7856420°N, 121.0225100°E` | 34.0m | `[ +155.23,  +420.66,  -1.02]` | 日光公園中心休閒綠帶原點 |
| **GCP 5** | **台鐵新莊車站挑高大廳中心** | `24.7891000°N, 121.0228000°E` | 32.6m | `[ +184.55,  +803.70,  -2.45]` | 北側交通大動脈、高架鐵路交叉點 |
| **GCP 6** | **關新東路 / 關新二街口中心** | `24.7848600°N, 121.0232500°E` | 34.0m | `[ +230.06,  +334.04,  -1.01]` | 東側南北貫通幹道路網對齊點 |
| **GCP 7** | **關新北路 / 新莊車站前迎賓廣場口** | `24.7896100°N, 121.0229300°E` | 32.5m | `[ +197.69,  +860.19,  -2.56]` | 車站前人行道、計程車站與廣場對齊點 |

---

## 📐 五、 數學轉換模型 (Mathematical Formulation)

### 1. WGS84 橢球體基礎常數
* 長半軸 $a = 6378137.0\text{ m}$
* 扁率倒數 $1/f = 298.257223563$
* 短半軸 $b = a(1 - f) \approx 6356752.314245\text{ m}$
* 第一偏心率平方 $e^2 = 2f - f^2 \approx 0.00669437999014$

### 2. WGS84 地理坐標 $(\phi, \lambda, h) \longrightarrow$ ECEF $(X, Y, Z)$
卯酉圈曲率半徑 (Radius of Curvature in Prime Vertical)：
$$N(\phi) = \frac{a}{\sqrt{1 - e^2 \sin^2 \phi}}$$

$$X = (N(\phi) + h) \cos \phi \cos \lambda$$
$$Y = (N(\phi) + h) \cos \phi \sin \lambda$$
$$Z = (N(\phi)(1 - e^2) + h) \sin \phi$$

### 3. ECEF 坐標差值 $\longrightarrow$ Local ENU 剛體旋轉
設基準原點 ECEF 坐標為 $(X_0, Y_0, Z_0)$，待轉點之 ECEF 向量差為 $[\Delta X, \Delta Y, \Delta Z]^T$：
$$\begin{bmatrix} E \\ N \\ U \end{bmatrix} = \begin{bmatrix} -\sin \lambda_0 & \cos \lambda_0 & 0 \\ -\sin \phi_0 \cos \lambda_0 & -\sin \phi_0 \sin \lambda_0 & \cos \phi_0 \\ \cos \phi_0 \cos \lambda_0 & \cos \phi_0 \sin \lambda_0 & \sin \phi_0 \end{bmatrix} \begin{bmatrix} X - X_0 \\ Y - Y_0 \\ Z - Z_0 \end{bmatrix}$$

### 4. Local ENU 坐標 $\longrightarrow$ WGS84 反向轉換
透過旋轉矩陣之轉置矩陣逆算至 ECEF，再採用 **Bowring 演算法** 進行閉合解反算，確保在任何高度下均具備亞微米級數值穩定度。

---

## 🏗️ 六、 Gazebo Harmonic (SDF 1.8) 配置實現

於世界主設定檔 `src/guanxin_sim/worlds/guanxin.sdf` 中，在 `<world name="guanxin_world">` 根節點下嵌入標準 `<spherical_coordinates>` 區塊：

```xml
    <!-- ==================== WGS84 地理基準原點 (Geospatial Datum) ==================== -->
    <spherical_coordinates>
      <surface_model>EARTH_WGS84</surface_model>
      <world_frame_orientation>ENU</world_frame_orientation>
      <latitude_deg>24.7818444</latitude_deg>
      <longitude_deg>121.0209750</longitude_deg>
      <elevation>35.0</elevation>
      <heading_deg>0.0</heading_deg>
    </spherical_coordinates>
```

* **`surface_model`**：設定為 `EARTH_WGS84`。
* **`world_frame_orientation`**：設定為 `ENU`（East=X, North=Y, Up=Z）。
* **`latitude_deg`** / **`longitude_deg`**：光復路一段 / 關新路口真實座標。
* **`heading_deg`**：設定為 `0.0`（World $+Y$ 對齊真北 True North）。

---

## 🛠️ 七、 轉換工具腳本使用說明 (`scripts/geo_datum_tool.py`)

本專案提供原生 Python 3 工具 `scripts/geo_datum_tool.py`，支援經緯度與 Gazebo 世界坐標的雙向互動式查詢與管線化自動轉換。

### 1. 執行自我精度檢驗：
```bash
python3 scripts/geo_datum_tool.py --test
```
*驗驗輸出*：
* 原點精準度：`(0.000000, 0.000000, 0.000000) m`
* 雙向轉換最大閉合誤差：`0.000000 mm` (水平) / `0.000001 mm` (垂直)
* 58 公頃多邊形面積驗證：$580,123.6\text{ m}^2$

### 2. 顯示多邊形與 GCP 清冊：
```bash
python3 scripts/geo_datum_tool.py --polygon
python3 scripts/geo_datum_tool.py --gcps
```

### 3. 單點經緯度轉 Gazebo ENU 座標：
```bash
# 查詢台鐵新莊車站之 ENU 坐標 (Lat, Lon, [Elev])
python3 scripts/geo_datum_tool.py --wgs84-to-enu 24.7891000 121.0228000 32.6
# 輸出: ENU: [East: +184.5501 m, North: +803.7024 m, Up: -2.4512 m]
```

### 4. Gazebo ENU 坐標反查經緯度：
```bash
# 查詢 Local 坐標 (X=+76.75, Y=+335.81) 對應之 WGS84 經緯度
python3 scripts/geo_datum_tool.py --enu-to-wgs84 76.75 335.81
# 輸出: WGS84: (24.78487600° N, 121.02173400° E, 34.1923 m)
```

---

## ✅ 八、 驗收結論

Phase 1 基準工作已全數完成：
1. 原點、邊界、GCP 均完成數學級封閉定義。
2. 雙向轉換精度達亞毫米級 ($< 0.001\text{ mm}$)。
3. 世界規格書、CLI 工具與 Gazebo 世界描述檔已全面同步。
