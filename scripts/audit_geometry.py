#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Precise 2D OBB Geometry Collision Auditor for Guanxin Digital Twin
Author: Autonomous Robotics & Simulation Team
"""

import os
import sys
import math
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(REPO_DIR, "src", "guanxin_sim", "models")
WORLD_PATH = os.path.join(REPO_DIR, "src", "guanxin_sim", "worlds", "guanxin.sdf")

# Coordinate transforms
def compose_pose_2d(parent_x, parent_y, parent_yaw, child_x, child_y, child_yaw):
    cos_p = math.cos(parent_yaw)
    sin_p = math.sin(parent_yaw)
    gx = parent_x + child_x * cos_p - child_y * sin_p
    gy = parent_y + child_x * sin_p + child_y * cos_p
    gyaw = parent_yaw + child_yaw
    while gyaw > math.pi: gyaw -= 2*math.pi
    while gyaw <= -math.pi: gyaw += 2*math.pi
    return gx, gy, gyaw

def get_box_vertices(cx, cy, yaw, sx, sy):
    """Return 4 vertices of a 2D oriented box."""
    hx = sx / 2.0
    hy = sy / 2.0
    cos_y = math.cos(yaw)
    sin_y = math.sin(yaw)
    
    corners = [
        (-hx, -hy),
        (hx, -hy),
        (hx, hy),
        (-hx, hy)
    ]
    verts = []
    for dx, dy in corners:
        vx = cx + dx * cos_y - dy * sin_y
        vy = cy + dx * sin_y + dy * cos_y
        verts.append((vx, vy))
    return verts

def sat_overlap(verts1, verts2):
    """Separating Axis Theorem to check if two convex polygons overlap.
    Returns (overlap_bool, min_penetration)
    """
    polys = [verts1, verts2]
    min_overlap = float('inf')
    
    for poly in polys:
        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]
            
            # Normal vector
            edge_x = p2[0] - p1[0]
            edge_y = p2[1] - p1[1]
            length = math.hypot(edge_x, edge_y)
            if length == 0: continue
            axis_x = -edge_y / length
            axis_y = edge_x / length
            
            # Project poly 1
            min1 = float('inf')
            max1 = float('-inf')
            for vx, vy in verts1:
                proj = vx * axis_x + vy * axis_y
                if proj < min1: min1 = proj
                if proj > max1: max1 = proj
                
            # Project poly 2
            min2 = float('inf')
            max2 = float('-inf')
            for vx, vy in verts2:
                proj = vx * axis_x + vy * axis_y
                if proj < min2: min2 = proj
                if proj > max2: max2 = proj
                
            # Check gap
            if max1 < min2 or max2 < min1:
                return False, 0.0
                
            overlap = min(max1, max2) - max(min1, min2)
            if overlap < min_overlap:
                min_overlap = overlap
                
    return True, min_overlap

def parse_pose(text):
    if text is None: return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    parts = [float(p) for p in text.strip().split()]
    while len(parts) < 6: parts.append(0.0)
    return tuple(parts[:6])

def load_collisions_from_model_sdf(model_sdf_path):
    collisions = []
    if not os.path.exists(model_sdf_path):
        return collisions
    try:
        tree = ET.parse(model_sdf_path)
        root = tree.getroot()
        model = root.find('model')
        if model is None: model = root
        for link in model.findall('link'):
            for col in link.findall('collision'):
                col_name = col.get('name', 'unnamed')
                pose_elem = col.find('pose')
                col_pose = parse_pose(pose_elem.text if pose_elem is not None else None)
                geom = col.find('geometry')
                if geom is None: continue
                box = geom.find('box')
                cyl = geom.find('cylinder')
                if box is not None:
                    sz_elem = box.find('size')
                    if sz_elem is not None:
                        sizes = [float(s) for s in sz_elem.text.strip().split()]
                        collisions.append({
                            'name': col_name,
                            'type': 'box',
                            'pose': col_pose,
                            'size': sizes
                        })
                elif cyl is not None:
                    rad_elem = cyl.find('radius')
                    len_elem = cyl.find('length')
                    rad = float(rad_elem.text.strip()) if rad_elem is not None else 1.0
                    l = float(len_elem.text.strip()) if len_elem is not None else 1.0
                    collisions.append({
                        'name': col_name,
                        'type': 'cylinder',
                        'pose': col_pose,
                        'size': [rad*2, rad*2, l]
                    })
    except Exception as e:
        print(f"Error parsing {model_sdf_path}: {e}")
    return collisions

def audit_world():
    print(f"Loading world from {WORLD_PATH}...")
    tree = ET.parse(WORLD_PATH)
    world = tree.getroot().find('world')
    
    roads = [] # name, verts, pose, size
    sidewalks = []
    buildings = [] # model_name, collision_name, verts, center_x, center_y, z_min, z_max
    
    # 1. Parse inline models in world
    for m in world.findall('model'):
        m_name = m.get('name')
        m_pose = parse_pose(m.find('pose').text if m.find('pose') is not None else None)
        
        for link in m.findall('link'):
            link_pose = parse_pose(link.find('pose').text if link.find('pose') is not None else None)
            
            for col in link.findall('collision'):
                c_name = col.get('name')
                c_pose = parse_pose(col.find('pose').text if col.find('pose') is not None else None)
                geom = col.find('geometry')
                if geom is None: continue
                box = geom.find('box')
                if box is None: continue
                sz = [float(s) for s in box.find('size').text.strip().split()]
                
                # Combine poses
                # Link pose in model
                lx, ly, lyaw = compose_pose_2d(m_pose[0], m_pose[1], m_pose[5], link_pose[0], link_pose[1], link_pose[5])
                # Col pose in link
                gx, gy, gyaw = compose_pose_2d(lx, ly, lyaw, c_pose[0], c_pose[1], c_pose[5])
                gz = m_pose[2] + link_pose[2] + c_pose[2]
                
                verts = get_box_vertices(gx, gy, gyaw, sz[0], sz[1])
                
                entry = {
                    'model': m_name,
                    'col': c_name,
                    'verts': verts,
                    'center': (gx, gy),
                    'z_range': (gz - sz[2]/2.0, gz + sz[2]/2.0),
                    'yaw': gyaw,
                    'size': sz
                }
                
                if m_name == 'road_network':
                    if 'sw_' in c_name or 'sidewalk' in c_name:
                        sidewalks.append(entry)
                    else:
                        roads.append(entry)
                elif m_name == 'sun_park_landscape':
                    # Park landscape
                    pass
                else:
                    buildings.append(entry)
                    
    # 2. Parse includes in world
    for inc in world.findall('include'):
        inc_name = inc.find('name').text.strip() if inc.find('name') is not None else 'unnamed'
        uri = inc.find('uri').text.strip() if inc.find('uri') is not None else ''
        inc_pose = parse_pose(inc.find('pose').text if inc.find('pose') is not None else None)
        
        # Skip vehicles, trees, poles, lights for building audit
        if any(x in inc_name for x in ['pole', 'tree', 'light', 'scooter', 'hydrant', 'box', 'model_y', 'car_parked', 'mcd_lot_car']):
            continue
            
        if uri.startswith('model://'):
            mod_folder = uri.replace('model://', '')
            model_sdf_path = os.path.join(MODELS_DIR, mod_folder, 'model.sdf')
            cols = load_collisions_from_model_sdf(model_sdf_path)
            
            for c in cols:
                # Combine pose
                gx, gy, gyaw = compose_pose_2d(inc_pose[0], inc_pose[1], inc_pose[5], c['pose'][0], c['pose'][1], c['pose'][5])
                gz = inc_pose[2] + c['pose'][2]
                sz = c['size']
                verts = get_box_vertices(gx, gy, gyaw, sz[0], sz[1])
                
                entry = {
                    'model': inc_name,
                    'col': c['name'],
                    'verts': verts,
                    'center': (gx, gy),
                    'z_range': (gz - sz[2]/2.0, gz + sz[2]/2.0),
                    'yaw': gyaw,
                    'size': sz
                }
                buildings.append(entry)
                
    print(f"\nAudit elements found:")
    print(f"  Road Carriageways: {len(roads)}")
    print(f"  Sidewalks:        {len(sidewalks)}")
    print(f"  Building Collision Components: {len(buildings)}")
    
    # 1. Check Building vs Road Carriageways
    print("\n" + "="*80)
    print("CHECK 1: Buildings encroaching on Road Carriageways (建物壓到馬路)")
    print("="*80)
    road_encroachments = []
    for b in buildings:
        for r in roads:
            # Check Z overlap: roads are near ground z ~ 0.0 to 0.2
            if b['z_range'][0] > 0.5: # building starts high in air
                continue
            overlap, pen = sat_overlap(b['verts'], r['verts'])
            if overlap:
                road_encroachments.append((b, r, pen))
                print(f"[ROAD ENCROACHMENT] Building '{b['model']}' ({b['col']}) overlaps with Road '{r['col']}'! Penetration depth: {pen:.3f}m")
                
    if not road_encroachments:
        print("  >> None! Zero buildings encroach on road carriageways.")
    else:
        print(f"  >> Found {len(road_encroachments)} road encroachment collisions!")
        
    # 2. Check Building vs Building Overlaps
    print("\n" + "="*80)
    print("CHECK 2: Building vs Building Overlaps (建物與建物重疊)")
    print("="*80)
    bldg_overlaps = []
    n_b = len(buildings)
    for i in range(n_b):
        for j in range(i + 1, n_b):
            b1 = buildings[i]
            b2 = buildings[j]
            # Skip collision components of the same model
            if b1['model'] == b2['model']:
                continue
                
            # Check Z overlap
            z_min = max(b1['z_range'][0], b2['z_range'][0])
            z_max = min(b1['z_range'][1], b2['z_range'][1])
            if z_min >= z_max:
                continue # No height overlap
                
            overlap, pen = sat_overlap(b1['verts'], b2['verts'])
            if overlap:
                bldg_overlaps.append((b1, b2, pen))
                print(f"[BUILDING OVERLAP] '{b1['model']}' ({b1['col']}) overlaps with '{b2['model']}' ({b2['col']})! Penetration depth: {pen:.3f}m, Z overlap: [{z_min:.1f}, {z_max:.1f}]m")
                
    if not bldg_overlaps:
        print("  >> None! Zero building-building overlaps.")
    else:
        print(f"  >> Found {len(bldg_overlaps)} building-building overlaps!")
        
    return road_encroachments, bldg_overlaps

if __name__ == '__main__':
    audit_world()
