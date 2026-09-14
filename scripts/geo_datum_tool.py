#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeoDatumTool - WGS84 Geodetic Datum to Local ENU / Gazebo World Coordinate Converter
Author: Autonomous Robotics & Simulation Team
Project: Guanxin Road Commercial Area Digital Twin Simulation

Geodetic Datum Specification:
  Surface Model: EARTH_WGS84 (EPSG:4326)
  World Frame: Local ENU (East-North-Up)
  Origin (0,0,0): Point 1 (Guangfu Rd. Sec. 1 / Guanxin Rd. Junction)
    Latitude:  24°46'54.64" N -> 24.78184444° N
    Longitude: 121°01'15.51" E -> 121.02097500° E
    Elevation: 35.00 m ASL
"""

import sys
import math
import json
import argparse
from typing import Tuple, List, Dict, Any

# ==================== WGS84 Ellipsoid Constants ====================
WGS84_A = 6378137.0                # Semi-major axis in meters
WGS84_F = 1.0 / 298.257223563      # Flattening
WGS84_B = WGS84_A * (1.0 - WGS84_F) # Semi-minor axis (~6356752.314245m)
WGS84_E2 = 2.0 * WGS84_F - WGS84_F ** 2  # First eccentricity squared (~0.00669437999014)
WGS84_EP2 = (WGS84_A ** 2 - WGS84_B ** 2) / (WGS84_B ** 2)  # Second eccentricity squared

# ==================== Project Datum Definition ====================
DATUM_ORIGIN_LAT = 24.781844444444444  # 24°46'54.64" N
DATUM_ORIGIN_LON = 121.02097500000000  # 121°01'15.51" E
DATUM_ORIGIN_ELEV = 35.0               # Height in meters ASL

# Guanxin Road main corridor orientation (~14.0 deg East of True North)
GUANXIN_ROAD_BEARING_DEG = 14.03


class GeoDatum:
    """Rigid Geodetic Datum transformation engine for WGS84 <-> Local ENU."""

    def __init__(self, ref_lat: float = DATUM_ORIGIN_LAT,
                 ref_lon: float = DATUM_ORIGIN_LON,
                 ref_elev: float = DATUM_ORIGIN_ELEV):
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self.ref_elev = ref_elev

        self.ref_lat_rad = math.radians(ref_lat)
        self.ref_lon_rad = math.radians(ref_lon)

        # Precompute reference ECEF coordinate
        self.x0, self.y0, self.z0 = self.wgs84_to_ecef(self.ref_lat, self.ref_lon, self.ref_elev)

        # Precompute rotation matrix from ECEF to ENU
        # [E]   [ -sin(lon)          cos(lon)         0         ] [dX]
        # [N] = [ -sin(lat)cos(lon) -sin(lat)sin(lon) cos(lat)  ] [dY]
        # [U]   [  cos(lat)cos(lon)  cos(lat)sin(lon) sin(lat)  ] [dZ]
        sin_lat = math.sin(self.ref_lat_rad)
        cos_lat = math.cos(self.ref_lat_rad)
        sin_lon = math.sin(self.ref_lon_rad)
        cos_lon = math.cos(self.ref_lon_rad)

        self.rot_ecef_to_enu = [
            [-sin_lon, cos_lon, 0.0],
            [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
            [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat]
        ]

        # Inverse rotation (ENU to ECEF) is transpose of orthogonal matrix
        self.rot_enu_to_ecef = [
            [self.rot_ecef_to_enu[0][0], self.rot_ecef_to_enu[1][0], self.rot_ecef_to_enu[2][0]],
            [self.rot_ecef_to_enu[0][1], self.rot_ecef_to_enu[1][1], self.rot_ecef_to_enu[2][1]],
            [self.rot_ecef_to_enu[0][2], self.rot_ecef_to_enu[1][2], self.rot_ecef_to_enu[2][2]]
        ]

    @staticmethod
    def wgs84_to_ecef(lat_deg: float, lon_deg: float, elev_m: float) -> Tuple[float, float, float]:
        """Converts WGS84 Geodetic Coordinates (lat, lon, elev) to Earth-Centered Earth-Fixed (ECEF)."""
        lat_rad = math.radians(lat_deg)
        lon_rad = math.radians(lon_deg)
        sin_lat = math.sin(lat_rad)
        cos_lat = math.cos(lat_rad)
        sin_lon = math.sin(lon_rad)
        cos_lon = math.cos(lon_rad)

        # Radius of curvature in the prime vertical
        n = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat ** 2)

        x = (n + elev_m) * cos_lat * cos_lon
        y = (n + elev_m) * cos_lat * sin_lon
        z = (n * (1.0 - WGS84_E2) + elev_m) * sin_lat
        return x, y, z

    @staticmethod
    def ecef_to_wgs84(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Converts ECEF coordinates (x, y, z) back to WGS84 (lat, lon, elev) using Bowring's method."""
        p = math.sqrt(x ** 2 + y ** 2)
        if p < 1e-6:
            # Polar singularity
            lat = 90.0 if z > 0 else -90.0
            lon = 0.0
            elev = abs(z) - WGS84_B
            return lat, lon, elev

        # Parametric latitude (Bowring's algorithm)
        theta = math.atan2(z * WGS84_A, p * WGS84_B)
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)

        lat_rad = math.atan2(
            z + WGS84_EP2 * WGS84_B * (sin_theta ** 3),
            p - WGS84_E2 * WGS84_A * (cos_theta ** 3)
        )
        lon_rad = math.atan2(y, x)

        sin_lat = math.sin(lat_rad)
        cos_lat = math.cos(lat_rad)
        n = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat ** 2)
        elev = p / cos_lat - n

        return math.degrees(lat_rad), math.degrees(lon_rad), elev

    def wgs84_to_enu(self, lat_deg: float, lon_deg: float, elev_m: float = None) -> Tuple[float, float, float]:
        """Converts WGS84 geodetic point to Local East-North-Up (ENU) coordinates relative to Datum origin."""
        if elev_m is None:
            elev_m = self.ref_elev

        x, y, z = self.wgs84_to_ecef(lat_deg, lon_deg, elev_m)
        dx = x - self.x0
        dy = y - self.y0
        dz = z - self.z0

        e = self.rot_ecef_to_enu[0][0] * dx + self.rot_ecef_to_enu[0][1] * dy + self.rot_ecef_to_enu[0][2] * dz
        n = self.rot_ecef_to_enu[1][0] * dx + self.rot_ecef_to_enu[1][1] * dy + self.rot_ecef_to_enu[1][2] * dz
        u = self.rot_ecef_to_enu[2][0] * dx + self.rot_ecef_to_enu[2][1] * dy + self.rot_ecef_to_enu[2][2] * dz
        return e, n, u

    def enu_to_wgs84(self, east_m: float, north_m: float, up_m: float = 0.0) -> Tuple[float, float, float]:
        """Converts Local East-North-Up (ENU) coordinates back to WGS84 geodetic coordinates."""
        dx = self.rot_enu_to_ecef[0][0] * east_m + self.rot_enu_to_ecef[0][1] * north_m + self.rot_enu_to_ecef[0][2] * up_m
        dy = self.rot_enu_to_ecef[1][0] * east_m + self.rot_enu_to_ecef[1][1] * north_m + self.rot_enu_to_ecef[1][2] * up_m
        dz = self.rot_enu_to_ecef[2][0] * east_m + self.rot_enu_to_ecef[2][1] * north_m + self.rot_enu_to_ecef[2][2] * up_m

        x = self.x0 + dx
        y = self.y0 + dy
        z = self.z0 + dz

        return self.ecef_to_wgs84(x, y, z)


# ==================== Ground Truth Data Sets ====================

POLYGON_VERTICES = [
    {
        "id": "P1",
        "name": "Point 1 (南界 / 原點)",
        "desc": "光復路一段 / 關新路交叉口核心起點 (World Origin Datum)",
        "dms": ("24°46'54.64\"N", "121°01'15.51\"E"),
        "lat": 24.781844444444444,
        "lon": 121.02097500000000,
        "elev": 35.0
    },
    {
        "id": "P2",
        "name": "Point 2 (東界)",
        "desc": "關新東路 / 埔頂路延伸與東側住宅商務區邊界",
        "dms": ("24°47'10.48\"N", "121°01'28.57\"E"),
        "lat": 24.786244444444444,
        "lon": 121.02460277777778,
        "elev": 34.2
    },
    {
        "id": "P3",
        "name": "Point 3 (東北界)",
        "desc": "台鐵新莊車站東側 / 關新北路口外圍",
        "dms": ("24°47'25.79\"N", "121°01'24.04\"E"),
        "lat": 24.790497222222222,
        "lon": 121.02334444444445,
        "elev": 32.5
    },
    {
        "id": "P4",
        "name": "Point 4 (西北界)",
        "desc": "台鐵高架鐵路廊道西側 / 關新北路外圍住宅區",
        "dms": ("24°47'25.82\"N", "121°01'07.91\"E"),
        "lat": 24.790505555555556,
        "lon": 121.01886388888888,
        "elev": 32.8
    },
    {
        "id": "P5",
        "name": "Point 5 (西界)",
        "desc": "新莊街 / 關新西街延伸社區聚落交會處",
        "dms": ("24°47'02.78\"N", "121°00'55.31\"E"),
        "lat": 24.784105555555554,
        "lon": 121.01536388888889,
        "elev": 34.5
    }
]

GROUND_CONTROL_POINTS = [
    {
        "id": "GCP_1",
        "name": "光復路一段 / 關新路口中心 (Datum Origin)",
        "desc": "關新商圈南側端點，Gazebo 世界坐標原點 (0, 0, 0)",
        "lat": 24.781844444444444,
        "lon": 121.02097500000000,
        "elev": 35.0
    },
    {
        "id": "GCP_2",
        "name": "關新路 / 關新一街口中心",
        "desc": "中南商圈樞紐，麥當勞與商辦大樓交匯點",
        "lat": 24.7826180,
        "lon": 121.0211680,
        "elev": 34.8
    },
    {
        "id": "GCP_3",
        "name": "關新路 / 關新二街口星巴克日光門市角",
        "desc": "核心商圈十字路口，日光門市 45 度轉角建築",
        "lat": 24.7848760,
        "lon": 121.0217340,
        "elev": 34.2
    },
    {
        "id": "GCP_4",
        "name": "關新公園（日光公園）中心休憩涼亭",
        "desc": "公共休閒綠帶核心，景觀步道與地標滑梯交匯處",
        "lat": 24.7856420,
        "lon": 121.0225100,
        "elev": 34.0
    },
    {
        "id": "GCP_5",
        "name": "台鐵新莊車站挑高大廳中心",
        "desc": "北側交通大動脈，高架雙軌橋墩與站體交會處",
        "lat": 24.7891000,
        "lon": 121.0228000,
        "elev": 32.6
    },
    {
        "id": "GCP_6",
        "name": "關新東路 / 關新二街口中心",
        "desc": "商圈東側主要貫通道路與住宅街區路口",
        "lat": 24.7848600,
        "lon": 121.0232500,
        "elev": 34.0
    },
    {
        "id": "GCP_7",
        "name": "關新北路 / 新莊車站前迎賓廣場口",
        "desc": "新莊車站正前方人行斑馬線與排班避車彎道起點",
        "lat": 24.7896100,
        "lon": 121.0229300,
        "elev": 32.5
    }
]


def calculate_polygon_area_enu(pts_enu: List[Tuple[float, float]]) -> float:
    """Calculates 2D planar polygon area in m² using the Shoelace formula."""
    n = len(pts_enu)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += pts_enu[i][0] * pts_enu[j][1]
        area -= pts_enu[j][0] * pts_enu[i][1]
    return abs(area) / 2.0


def run_self_tests(datum: GeoDatum) -> bool:
    """Runs rigorous round-trip transformation tests and validates GCP precision."""
    print("=" * 80)
    print("   GEODATUM TOOL SELF-TEST SUITE: WGS84 <-> LOCAL ENU (RIGID BODY)")
    print("=" * 80)

    # 1. Origin Test
    e0, n0, u0 = datum.wgs84_to_enu(DATUM_ORIGIN_LAT, DATUM_ORIGIN_LON, DATUM_ORIGIN_ELEV)
    print(f"[TEST 1] Origin Check: ({e0:.6f}, {n0:.6f}, {u0:.6f}) m")
    if abs(e0) > 1e-4 or abs(n0) > 1e-4 or abs(u0) > 1e-4:
        print("  FAILED: Origin is not precisely zero!")
        return False
    print("  PASSED: Origin is identically (0.0, 0.0, 0.0) m.")

    # 2. Round-trip conversion tests on all polygon points and GCPs
    print("\n[TEST 2] Precision Round-trip Tests (WGS84 -> ENU -> WGS84):")
    all_points = [(p["name"], p["lat"], p["lon"], p["elev"]) for p in POLYGON_VERTICES] + \
                 [(p["name"], p["lat"], p["lon"], p["elev"]) for p in GROUND_CONTROL_POINTS]

    max_err_horiz_m = 0.0
    max_err_vert_m = 0.0

    for name, lat, lon, elev in all_points:
        e, n, u = datum.wgs84_to_enu(lat, lon, elev)
        lat_back, lon_back, elev_back = datum.enu_to_wgs84(e, n, u)

        # Calculate coordinate error in meters
        e_err, n_err, u_err = datum.wgs84_to_enu(lat_back, lon_back, elev_back)
        horiz_err = math.sqrt((e - e_err) ** 2 + (n - n_err) ** 2)
        vert_err = abs(u - u_err)

        if horiz_err > max_err_horiz_m:
            max_err_horiz_m = horiz_err
        if vert_err > max_err_vert_m:
            max_err_vert_m = vert_err

    print(f"  Max Horizontal Round-trip Error: {max_err_horiz_m * 1000.0:.6f} mm")
    print(f"  Max Vertical Round-trip Error:   {max_err_vert_m * 1000.0:.6f} mm")
    if max_err_horiz_m > 0.001:  # 1 mm tolerance
        print("  FAILED: Round-trip error exceeds 1mm!")
        return False
    print("  PASSED: Sub-millimeter conversion accuracy achieved.")

    # 3. Polygon bounds and area
    print("\n[TEST 3] Target 58-Hectare Boundary Polygon Dimensions:")
    poly_enu = []
    for p in POLYGON_VERTICES:
        e, n, u = datum.wgs84_to_enu(p["lat"], p["lon"], p["elev"])
        poly_enu.append((e, n))

    xs = [pt[0] for pt in poly_enu]
    ys = [pt[1] for pt in poly_enu]
    width_x = max(xs) - min(xs)
    length_y = max(ys) - min(ys)
    area_m2 = calculate_polygon_area_enu(poly_enu)
    hectares = area_m2 / 10000.0
    ping = area_m2 * 0.3025

    print(f"  East-West Span (Width X):  {width_x:.2f} m (Min E: {min(xs):.2f}m, Max E: {max(xs):.2f}m)")
    print(f"  South-North Span (Length Y): {length_y:.2f} m (Min N: {min(ys):.2f}m, Max N: {max(ys):.2f}m)")
    print(f"  Polygon Area: {area_m2:,.1f} m² (~{hectares:.2f} ha / ~{ping:,.0f} 坪)")

    # 4. Guanxin road heading check
    gcp1_e, gcp1_n, _ = datum.wgs84_to_enu(GROUND_CONTROL_POINTS[0]["lat"], GROUND_CONTROL_POINTS[0]["lon"])
    gcp5_e, gcp5_n, _ = datum.wgs84_to_enu(GROUND_CONTROL_POINTS[4]["lat"], GROUND_CONTROL_POINTS[4]["lon"])
    bearing_rad = math.atan2(gcp5_e - gcp1_e, gcp5_n - gcp1_n)
    bearing_deg = math.degrees(bearing_rad)
    corridor_len = math.sqrt((gcp5_e - gcp1_e) ** 2 + (gcp5_n - gcp1_n) ** 2)
    print(f"\n[TEST 4] Guanxin Road Main Corridor Alignment:")
    print(f"  GCP 1 (Origin) -> GCP 5 (TRA Xin-Zhuang Station):")
    print(f"  Corridor Distance: {corridor_len:.2f} m")
    print(f"  Bearing from True North: {bearing_deg:.2f}° (East of North)")
    print("=" * 80)
    print("ALL TESTS PASSED SUCCESSFULLY.")
    print("=" * 80)
    return True


def print_polygon_table(datum: GeoDatum):
    """Outputs the polygon vertices in formatted Markdown."""
    print("\n### 📍 Boundary Polygon Vertices (WGS84 <-> Local ENU)\n")
    print("| 頂點 | 名稱與描述 | WGS84 經緯度 (度分秒) | 十進位經緯度 | Local ENU [E, N, U] (m) |")
    print("| :---: | :--- | :--- | :--- | :--- |")
    for p in POLYGON_VERTICES:
        e, n, u = datum.wgs84_to_enu(p["lat"], p["lon"], p["elev"])
        dms_str = f"{p['dms'][0]}, {p['dms'][1]}"
        deg_str = f"`{p['lat']:.7f}°N, {p['lon']:.7f}°E`"
        enu_str = f"`[{e:+8.2f}, {n:+8.2f}, {u:+5.2f}]`"
        print(f"| **{p['id']}** | {p['name']}<br>*{p['desc']}* | {dms_str} | {deg_str} | {enu_str} |")


def print_gcp_table(datum: GeoDatum):
    """Outputs the Ground Control Points (GCPs) in formatted Markdown."""
    print("\n### 🎯 Ground Control Points (GCP) Catalog\n")
    print("| GCP 編號 | 控制點地標名稱與現場特徵 | 十進位經緯度 (WGS84) | 海拔 (m) | Local ENU 坐標 [X(東), Y(北), Z(上)] | 備註 |")
    print("| :---: | :--- | :--- | :---: | :--- | :--- |")
    for p in GROUND_CONTROL_POINTS:
        e, n, u = datum.wgs84_to_enu(p["lat"], p["lon"], p["elev"])
        deg_str = f"`{p['lat']:.7f}°N, {p['lon']:.7f}°E`"
        enu_str = f"`[{e:+8.2f}, {n:+8.2f}, {u:+5.2f}]`"
        print(f"| **{p['id']}** | {p['name']}<br>*{p['desc']}* | {deg_str} | {p['elev']:.1f}m | {enu_str} | 基準校準點 |")


def main():
    parser = argparse.ArgumentParser(
        description="Guanxin Digital Twin Geospatial Datum Tool (WGS84 <-> ENU)"
    )
    parser.add_argument("--test", action="store_true", help="Run comprehensive precision self-tests")
    parser.add_argument("--polygon", action="store_true", help="Display 5-point boundary polygon table")
    parser.add_argument("--gcps", action="store_true", help="Display Ground Control Points (GCP) table")
    parser.add_argument("--wgs84-to-enu", nargs="+", type=float, metavar="VAL",
                        help="Convert WGS84 (lat lon [elev]) to Local ENU")
    parser.add_argument("--enu-to-wgs84", nargs="+", type=float, metavar="VAL",
                        help="Convert Local ENU (east north [up]) to WGS84")
    parser.add_argument("--json", action="store_true", help="Format single conversion output as JSON")

    args = parser.parse_args()
    datum = GeoDatum()

    if args.test:
        success = run_self_tests(datum)
        sys.exit(0 if success else 1)

    if args.polygon:
        print_polygon_table(datum)
        return

    if args.gcps:
        print_gcp_table(datum)
        return

    if args.wgs84_to_enu:
        lat = args.wgs84_to_enu[0]
        lon = args.wgs84_to_enu[1]
        elev = args.wgs84_to_enu[2] if len(args.wgs84_to_enu) > 2 else DATUM_ORIGIN_ELEV
        e, n, u = datum.wgs84_to_enu(lat, lon, elev)
        if args.json:
            print(json.dumps({"east": round(e, 4), "north": round(n, 4), "up": round(u, 4)}))
        else:
            print(f"WGS84: ({lat:.7f}°, {lon:.7f}°, {elev:.2f}m)")
            print(f"ENU:   [East: {e:+.4f} m, North: {n:+.4f} m, Up: {u:+.4f} m]")
        return

    if args.enu_to_wgs84:
        east = args.enu_to_wgs84[0]
        north = args.enu_to_wgs84[1]
        up = args.enu_to_wgs84[2] if len(args.enu_to_wgs84) > 2 else 0.0
        lat, lon, elev = datum.enu_to_wgs84(east, north, up)
        if args.json:
            print(json.dumps({"lat": round(lat, 8), "lon": round(lon, 8), "elev": round(elev, 4)}))
        else:
            print(f"ENU:   [East: {east:+.4f} m, North: {north:+.4f} m, Up: {up:+.4f} m]")
            print(f"WGS84: ({lat:.8f}° N, {lon:.8f}° E, {elev:.4f} m)")
        return

    # Default action if no arguments: run self test
    run_self_tests(datum)


if __name__ == "__main__":
    main()
