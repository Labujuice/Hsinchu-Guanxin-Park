#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate photo-realistic and authentic Taiwanese architectural facades & surface textures
for Guanxin Simulation World.

Targets:
1. 7-ELEVEN Convenience Store (convenience_store_711)
2. PX MART Supermarket (px_mart_store)
3. Xinzhuang Old Street Shophouses (xinzhuang_street_block)
4. Changyi Danmark Residence High-Rise (changyi_danmark_residence)
5. Guandong Civic Market & Hakka Cultural Hall (guandong_civic_market)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_REGULAR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc" if os.path.exists("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc") else FONT_BOLD

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_tiled_pattern(draw, box, tile_w, tile_h, color1, color2, mortar_color=(180, 180, 180), mortar_w=1):
    x0, y0, x1, y1 = box
    cols = int((x1 - x0) / tile_w) + 1
    rows = int((y1 - y0) / tile_h) + 1
    for r in range(rows):
        offset = (tile_w // 2) if (r % 2 == 1) else 0
        for c in range(-1, cols + 1):
            tx0 = x0 + c * tile_w + offset
            ty0 = y0 + r * tile_h
            tx1 = tx0 + tile_w - mortar_w
            ty1 = ty0 + tile_h - mortar_w
            cx0 = max(x0, min(x1, tx0))
            cy0 = max(y0, min(y1, ty0))
            cx1 = max(x0, min(x1, tx1))
            cy1 = max(y0, min(y1, ty1))
            if cx1 > cx0 and cy1 > cy0:
                factor = ((c * 7 + r * 13) % 17) / 17.0 * 0.15 - 0.075
                col = tuple(int(max(0, min(255, c_val * (1.0 + factor)))) for c_val in color1)
                draw.rectangle([cx0, cy0, cx1, cy1], fill=col)
                if mortar_w > 0:
                    draw.rectangle([cx0, cy1, cx1, min(y1, ty1 + mortar_w)], fill=mortar_color)
                    draw.rectangle([cx1, cy0, min(x1, tx1 + mortar_w), cy1], fill=mortar_color)

# ==============================================================================
# 1. 7-ELEVEN Textures
# ==============================================================================
def generate_711_textures():
    out_dir = "src/guanxin_sim/models/convenience_store_711/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    # 1.1 Facade (1024 x 512)
    W, H = 1024, 512
    im = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(im)

    # Header fascia (Y: 0 ~ 170)
    draw.rectangle([0, 0, W, 170], fill=(255, 255, 255))
    # 7-Eleven Classic Tri-Color Stripes
    draw.rectangle([0, 20, W, 58], fill=(234, 91, 12))     # 7-Eleven Orange
    draw.rectangle([0, 58, W, 96], fill=(0, 132, 61))      # 7-Eleven Green
    draw.rectangle([0, 96, W, 134], fill=(227, 27, 35))    # 7-Eleven Red
    draw.rectangle([0, 134, W, 170], fill=(250, 250, 250))
    draw.line([0, 170, W, 170], fill=(70, 70, 70), width=3)

    # 7-Eleven Logo Box on the left
    draw.rectangle([40, 15, 170, 140], fill=(255, 255, 255), outline=(0, 132, 61), width=4)
    draw.rectangle([50, 25, 160, 130], fill=(0, 132, 61))
    font_logo_7 = get_font(FONT_BOLD, 86)
    font_logo_elev = get_font(FONT_BOLD, 22)
    draw.text((68, 25), "7", font=font_logo_7, fill=(234, 91, 12))
    draw.rectangle([50, 72, 160, 98], fill=(227, 27, 35))
    draw.text((54, 73), "ELEVEN", font=font_logo_elev, fill=(255, 255, 255))

    # Main Title on Header
    font_title = get_font(FONT_BOLD, 42)
    font_sub = get_font(FONT_BOLD, 22)
    font_badge = get_font(FONT_BOLD, 18)

    draw.text((200, 38), "7-ELEVEN", font=font_title, fill=(255, 255, 255))
    draw.text((430, 44), "新竹關新門市", font=font_title, fill=(255, 255, 255))
    draw.text((200, 98), "24 HOURS OPEN・歡迎光臨", font=font_sub, fill=(255, 255, 255))

    # Badges on right side of header
    draw.rectangle([760, 26, 880, 70], fill=(255, 215, 0), outline=(200, 160, 0), width=2)
    draw.text((772, 34), "★ 24H 營業", font=font_badge, fill=(40, 40, 40))
    draw.rectangle([760, 80, 880, 124], fill=(234, 91, 12), outline=(180, 70, 10), width=2)
    draw.text((775, 90), "CITY CAFE", font=font_badge, fill=(255, 255, 255))

    draw.rectangle([895, 26, 1000, 124], fill=(245, 245, 245), outline=(0, 132, 61), width=3)
    draw.text((910, 42), "iBon", font=get_font(FONT_BOLD, 28), fill=(227, 27, 35))
    draw.text((915, 82), "ATM", font=get_font(FONT_BOLD, 24), fill=(0, 132, 61))

    # Storefront Glazing & Mullions (Y: 170 ~ 460)
    draw.rectangle([0, 170, W, 460], fill=(30, 45, 55)) # glass tone
    mullion_x = [0, 180, 360, 540, 720, 900, 1024]
    for mx in mullion_x:
        draw.rectangle([mx - 4, 170, mx + 4, 460], fill=(45, 48, 52))

    # Glass tint / interior display shelves simulation
    for i in range(len(mullion_x) - 1):
        gx0, gx1 = mullion_x[i] + 4, mullion_x[i+1] - 4
        draw.rectangle([gx0 + 10, 180, gx1 - 10, 195], fill=(255, 250, 220))
        draw.rectangle([gx0 + 15, 250, gx1 - 15, 440], fill=(60, 75, 85))
        for sy in [290, 330, 370, 410]:
            draw.line([gx0 + 15, sy, gx1 - 15, sy], fill=(120, 140, 155), width=2)

    # Automatic Sliding Door in Center (X: 360 ~ 540)
    draw.rectangle([360, 170, 540, 460], fill=(40, 60, 70))
    draw.rectangle([446, 170, 454, 460], fill=(60, 65, 70))
    draw.rectangle([385, 260, 515, 300], fill=(0, 132, 61))
    draw.text((400, 266), "歡 迎 光 臨", font=get_font(FONT_BOLD, 22), fill=(255, 255, 255))
    draw.rectangle([415, 320, 485, 345], fill=(234, 91, 12))
    draw.text((426, 323), "PUSH", font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))

    # Window Promo Posters
    draw.rectangle([40, 230, 150, 390], fill=(35, 25, 20), outline=(200, 160, 100), width=3)
    draw.text((50, 240), "CITY PRIMA", font=get_font(FONT_BOLD, 16), fill=(240, 210, 160))
    draw.text((55, 270), "精品咖啡", font=get_font(FONT_BOLD, 20), fill=(255, 255, 255))
    draw.text((50, 310), "第 2 杯", font=get_font(FONT_BOLD, 26), fill=(255, 215, 0))
    draw.text((55, 350), "半  價", font=get_font(FONT_BOLD, 26), fill=(255, 60, 60))

    draw.rectangle([740, 230, 880, 390], fill=(245, 245, 245), outline=(0, 132, 61), width=3)
    draw.text((755, 240), "OPEN POINT", font=get_font(FONT_BOLD, 18), fill=(234, 91, 12))
    draw.text((760, 275), "超值便當", font=get_font(FONT_BOLD, 22), fill=(0, 132, 61))
    draw.text((755, 315), "鮮食熱炒", font=get_font(FONT_BOLD, 20), fill=(40, 40, 40))
    draw.text((760, 350), "24H 熱食供", font=get_font(FONT_BOLD, 16), fill=(227, 27, 35))

    # Base Kickplate & Pavement (Y: 460 ~ 512)
    draw.rectangle([0, 460, W, 512], fill=(60, 62, 65))
    for tx in range(0, W, 40):
        draw.line([tx, 460, tx, 512], fill=(45, 47, 50), width=2)
    draw.line([0, 485, W, 485], fill=(45, 47, 50), width=2)

    im.save(os.path.join(out_dir, "seven_eleven_facade.png"))

    # 1.2 Protruding Sign (256 x 512)
    im_sign = Image.new("RGB", (256, 512), (255, 255, 255))
    ds = ImageDraw.Draw(im_sign)
    ds.rectangle([0, 0, 256, 512], fill=(250, 250, 250), outline=(60, 60, 60), width=8)
    ds.rectangle([8, 8, 28, 504], fill=(234, 91, 12))
    ds.rectangle([28, 8, 44, 504], fill=(0, 132, 61))
    ds.rectangle([44, 8, 58, 504], fill=(227, 27, 35))

    ds.rectangle([80, 30, 220, 170], fill=(0, 132, 61), outline=(234, 91, 12), width=4)
    ds.text((115, 35), "7", font=get_font(FONT_BOLD, 95), fill=(234, 91, 12))
    ds.rectangle([80, 95, 220, 125], fill=(227, 27, 35))
    ds.text((88, 98), "ELEVEN", font=get_font(FONT_BOLD, 24), fill=(255, 255, 255))

    font_v = get_font(FONT_BOLD, 46)
    chars = ["關", "新", "門", "市"]
    y_start = 200
    for ch in chars:
        ds.text((120, y_start), ch, font=font_v, fill=(0, 132, 61))
        y_start += 56

    ds.rectangle([75, 435, 225, 485], fill=(234, 91, 12))
    ds.text((95, 445), "24H 營業", font=get_font(FONT_BOLD, 26), fill=(255, 255, 255))
    im_sign.save(os.path.join(out_dir, "seven_eleven_protruding_sign.png"))
    print("✓ 7-ELEVEN textures generated.")

# ==============================================================================
# 2. PX MART Textures
# ==============================================================================
def generate_pxmart_textures():
    out_dir = "src/guanxin_sim/models/px_mart_store/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1024, 512
    im = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(im)

    # 2.1 Header: Iconic PX Mart Blue & Red Banner (Y: 0 ~ 160)
    draw.rectangle([0, 0, W, 140], fill=(0, 45, 110))
    draw.rectangle([0, 140, W, 160], fill=(215, 20, 40))

    cx, cy, cr = 85, 70, 45
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255))
    draw.ellipse([cx - cr + 10, cy - cr + 10, cx + cr - 10, cy + cr - 10], fill=(0, 45, 110))
    draw.ellipse([cx - cr + 22, cy - cr + 22, cx + cr - 22, cy + cr - 22], fill=(215, 20, 40))
    draw.ellipse([cx - cr + 32, cy - cr + 32, cx + cr - 32, cy + cr - 32], fill=(255, 255, 255))

    font_px_main = get_font(FONT_BOLD, 52)
    font_px_en = get_font(FONT_BOLD, 36)
    font_slogan = get_font(FONT_BOLD, 22)

    draw.text((160, 24), "全聯福利中心", font=font_px_main, fill=(255, 255, 255))
    draw.text((500, 35), "PX MART", font=font_px_en, fill=(255, 255, 255))
    draw.text((700, 40), "關新旗艦店", font=get_font(FONT_BOLD, 28), fill=(255, 215, 0))

    draw.text((165, 95), "買進美好生活・生鮮蔬果・請支援收銀！", font=font_slogan, fill=(255, 235, 120))
    draw.text((700, 95), "營業時間 08:00 - 23:00", font=font_slogan, fill=(255, 255, 255))

    # 2.2 Storefront & Supermarket Glazing (Y: 160 ~ 460)
    draw.rectangle([0, 160, W, 460], fill=(32, 44, 54))
    mullions = [0, 200, 400, 624, 824, 1024]
    for mx in mullions:
        draw.rectangle([mx - 5, 160, mx + 5, 460], fill=(50, 55, 60))

    for i in range(len(mullions) - 1):
        gx0, gx1 = mullions[i] + 5, mullions[i+1] - 5
        draw.rectangle([gx0 + 15, 175, gx1 - 15, 195], fill=(255, 255, 240))
        draw.rectangle([gx0 + 20, 260, gx1 - 20, 440], fill=(55, 70, 80))
        for sy in [295, 335, 375, 415]:
            draw.line([gx0 + 20, sy, gx1 - 20, sy], fill=(180, 200, 215), width=2)

    # Center Entrance (X: 400 ~ 624)
    draw.rectangle([400, 160, 624, 460], fill=(45, 65, 75))
    draw.rectangle([508, 160, 516, 460], fill=(65, 70, 75))
    draw.rectangle([420, 220, 604, 260], fill=(0, 45, 110))
    draw.text((435, 226), "全 聯 歡 迎 您", font=get_font(FONT_BOLD, 24), fill=(255, 255, 255))
    draw.rectangle([455, 280, 569, 310], fill=(215, 20, 40))
    draw.text((472, 284), "自動門 AUTO", font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))

    # Supermarket Posters
    draw.rectangle([40, 210, 160, 390], fill=(20, 75, 40), outline=(255, 255, 255), width=3)
    draw.text((55, 225), "全聯生鮮", font=get_font(FONT_BOLD, 20), fill=(255, 255, 255))
    draw.text((50, 265), "產地履歷", font=get_font(FONT_BOLD, 22), fill=(255, 215, 0))
    draw.text((50, 305), "特級高麗菜", font=get_font(FONT_BOLD, 18), fill=(255, 255, 255))
    draw.text((65, 345), "特價 49", font=get_font(FONT_BOLD, 22), fill=(255, 80, 80))

    draw.rectangle([860, 210, 980, 390], fill=(0, 70, 150), outline=(255, 255, 255), width=3)
    draw.text((880, 225), "PX Pay", font=get_font(FONT_BOLD, 24), fill=(255, 255, 255))
    draw.text((875, 265), "行動支付", font=get_font(FONT_BOLD, 22), fill=(255, 215, 0))
    draw.text((875, 305), "滿千送百", font=get_font(FONT_BOLD, 22), fill=(255, 80, 80))
    draw.text((875, 345), "福利卡點數", font=get_font(FONT_BOLD, 18), fill=(255, 255, 255))

    draw.rectangle([0, 460, W, 512], fill=(55, 58, 62))
    for tx in range(0, W, 32):
        draw.line([tx, 460, tx, 512], fill=(42, 45, 48), width=2)

    im.save(os.path.join(out_dir, "pxmart_facade.png"))

    # 2.2 Protruding Sign (256 x 512)
    im_sign = Image.new("RGB", (256, 512), (0, 45, 110))
    ds = ImageDraw.Draw(im_sign)
    ds.rectangle([0, 0, 256, 512], outline=(255, 255, 255), width=6)
    ds.rectangle([10, 480, 246, 502], fill=(215, 20, 40))

    cx, cy, cr = 128, 80, 45
    ds.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255))
    ds.ellipse([cx - cr + 10, cy - cr + 10, cx + cr - 10, cy + cr - 10], fill=(0, 45, 110))
    ds.ellipse([cx - cr + 22, cy - cr + 22, cx + cr - 22, cy + cr - 22], fill=(215, 20, 40))
    ds.ellipse([cx - cr + 32, cy - cr + 32, cx + cr - 32, cy + cr - 32], fill=(255, 255, 255))

    font_v = get_font(FONT_BOLD, 46)
    chars = ["全", "聯", "福", "利", "中", "心"]
    y_start = 145
    for ch in chars:
        ds.text((88, y_start), ch, font=font_v, fill=(255, 255, 255))
        y_start += 52

    im_sign.save(os.path.join(out_dir, "pxmart_protruding_sign.png"))
    print("✓ PX MART textures generated.")

# ==============================================================================
# 3. Xinzhuang Old Street Facade (2048 x 1024)
# ==============================================================================
def generate_xinzhuang_old_street_textures():
    out_dir = "src/guanxin_sim/models/xinzhuang_street_block/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 2048, 1024
    im = Image.new("RGB", (W, H), (230, 225, 215))
    draw = ImageDraw.Draw(im)

    unit_w = W // 4

    # --------------------------------------------------------------------------
    # Unit 1 (0 ~ 512): 林記老麵手工小籠包・永和豆漿
    # --------------------------------------------------------------------------
    u0 = 0
    draw_tiled_pattern(draw, (u0, 0, u0 + unit_w, 650), tile_w=32, tile_h=16,
                       color1=(235, 220, 175), color2=(225, 210, 165),
                       mortar_color=(190, 185, 170), mortar_w=2)
    draw.rectangle([u0 + 60, 80, u0 + 452, 280], fill=(40, 55, 65))
    for bx in range(u0 + 60, u0 + 452, 24):
        draw.line([bx, 80, bx, 280], fill=(210, 215, 220), width=3)
    for by in range(80, 280, 40):
        draw.line([u0 + 60, by, u0 + 452, by], fill=(210, 215, 220), width=3)
    draw.rectangle([u0 + 40, 50, u0 + 472, 85], fill=(30, 140, 70), outline=(20, 100, 50), width=2)

    draw.rectangle([u0 + 80, 360, u0 + 360, 540], fill=(45, 60, 70))
    draw.rectangle([u0 + 70, 340, u0 + 370, 365], fill=(25, 120, 60))
    draw.rectangle([u0 + 375, 420, u0 + 485, 520], fill=(240, 240, 240), outline=(150, 150, 150), width=2)
    draw.ellipse([u0 + 395, 435, u0 + 465, 505], fill=(210, 210, 210), outline=(100, 100, 100), width=2)
    draw.text((u0 + 415, 425), "HITACHI", font=get_font(FONT_BOLD, 12), fill=(100, 100, 100))

    draw.rectangle([u0 + 10, 650, u0 + unit_w - 10, 770], fill=(255, 220, 0), outline=(200, 40, 20), width=4)
    draw.text((u0 + 30, 665), "林 記 老 麵 手 工 小 籠 包", font=get_font(FONT_BOLD, 34), fill=(210, 20, 20))
    draw.text((u0 + 45, 715), "永和豆漿・手工蛋餅・飯糰・燒餅油條", font=get_font(FONT_BOLD, 22), fill=(30, 30, 30))

    draw.rectangle([u0, 770, u0 + unit_w, 1024], fill=(240, 235, 225))
    draw.rectangle([u0, 770, u0 + 60, 1024], fill=(160, 65, 45))
    draw.rectangle([u0 + unit_w - 60, 770, u0 + unit_w, 1024], fill=(160, 65, 45))
    draw.rectangle([u0 + 80, 840, u0 + 432, 980], fill=(220, 225, 230), outline=(120, 125, 130), width=3)
    for stx in [u0 + 120, u0 + 200, u0 + 280]:
        for sty in range(860, 960, 25):
            draw.rectangle([stx, sty, stx + 60, sty + 20], fill=(210, 175, 125), outline=(160, 120, 70), width=2)
    draw.rectangle([u0 + 350, 790, u0 + 440, 850], fill=(255, 255, 255), outline=(200, 20, 20), width=2)
    draw.text((u0 + 360, 795), "價目表\n小籠包 90\n豆漿 25", font=get_font(FONT_BOLD, 14), fill=(30, 30, 30))

    # --------------------------------------------------------------------------
    # Unit 2 (512 ~ 1024): 光陽機車行・排氣定檢站 (KYMCO)
    # --------------------------------------------------------------------------
    u1 = unit_w
    draw_tiled_pattern(draw, (u1, 0, u1 + unit_w, 650), tile_w=8, tile_h=8,
                       color1=(185, 185, 180), color2=(165, 165, 160),
                       mortar_color=(150, 150, 145), mortar_w=1)
    draw.rectangle([u1 + 70, 70, u1 + 442, 270], fill=(130, 50, 35))
    draw.rectangle([u1 + 100, 100, u1 + 412, 240], fill=(40, 50, 60))
    draw.rectangle([u1 + 50, 45, u1 + 462, 75], fill=(20, 80, 180), outline=(10, 50, 120), width=2)
    draw.rectangle([u1 + 60, 350, u1 + 452, 550], fill=(50, 55, 60))
    for bx in range(u1 + 60, u1 + 452, 20):
        draw.line([bx, 350, bx, 550], fill=(190, 195, 200), width=2)
    for by in range(350, 550, 35):
        draw.line([u1 + 60, by, u1 + 452, by], fill=(190, 195, 200), width=2)

    draw.rectangle([u1 + 10, 650, u1 + unit_w - 10, 770], fill=(225, 25, 35), outline=(0, 40, 120), width=4)
    draw.rectangle([u1 + 10, 680, u1 + unit_w - 10, 740], fill=(255, 255, 255))
    draw.text((u1 + 30, 685), "KYMCO 光陽機車", font=get_font(FONT_BOLD, 40), fill=(225, 25, 35))
    draw.text((u1 + 40, 655), "環保署指定 排氣定檢站 No.3508", font=get_font(FONT_BOLD, 18), fill=(255, 255, 255))
    draw.text((u1 + 40, 744), "專業保修・道路救援・正廠零件・換機油 150 起", font=get_font(FONT_BOLD, 18), fill=(255, 255, 255))

    draw.rectangle([u1, 770, u1 + unit_w, 1024], fill=(220, 220, 220))
    draw.rectangle([u1 + 80, 780, u1 + 432, 1024], fill=(80, 85, 90))
    draw.rectangle([u1 + 90, 820, u1 + 180, 970], fill=(180, 30, 30), outline=(220, 220, 220), width=2)
    draw.text((u1 + 100, 840), "工具車", font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))
    for ty in [820, 870, 920]:
        draw.ellipse([u1 + 350, ty, u1 + 410, ty + 40], fill=(20, 20, 20), outline=(60, 60, 60), width=6)
    draw.rectangle([u1 + 210, 890, u1 + 310, 1024], fill=(50, 50, 50), outline=(255, 215, 0), width=3)

    # --------------------------------------------------------------------------
    # Unit 3 (1024 ~ 1536): 清心福全冷飲站
    # --------------------------------------------------------------------------
    u2 = unit_w * 2
    draw_tiled_pattern(draw, (u2, 0, u2 + unit_w, 650), tile_w=16, tile_h=36,
                       color1=(245, 245, 240), color2=(235, 235, 230),
                       mortar_color=(205, 205, 200), mortar_w=2)
    draw.rectangle([u2 + 80, 90, u2 + 432, 270], fill=(35, 45, 55), outline=(50, 50, 50), width=4)
    draw.rectangle([u2 + 80, 370, u2 + 432, 550], fill=(35, 45, 55), outline=(50, 50, 50), width=4)
    draw.rectangle([u2 + 340, 440, u2 + 460, 530], fill=(245, 245, 245), outline=(160, 160, 160), width=2)
    draw.ellipse([u2 + 360, 450, u2 + 430, 520], fill=(220, 220, 220), outline=(120, 120, 120), width=2)

    draw.rectangle([u2 + 10, 650, u2 + unit_w - 10, 770], fill=(0, 135, 90), outline=(255, 255, 255), width=3)
    draw.ellipse([u2 + 35, 680, u2 + 75, 720], fill=(225, 30, 40))
    draw.text((u2 + 85, 670), "清心福全", font=get_font(FONT_BOLD, 44), fill=(255, 255, 255))
    draw.text((u2 + 285, 685), "新竹新莊店", font=get_font(FONT_BOLD, 24), fill=(255, 230, 140))
    draw.text((u2 + 85, 725), "烏龍綠茶・珍珠奶茶・優多綠・鮮奶茶", font=get_font(FONT_BOLD, 18), fill=(240, 255, 245))

    draw.rectangle([u2, 770, u2 + unit_w, 1024], fill=(245, 245, 245))
    draw.rectangle([u2 + 70, 840, u2 + 442, 970], fill=(225, 230, 235), outline=(140, 145, 150), width=3)
    for dx in range(u2 + 100, u2 + 420, 60):
        draw.rectangle([dx, 810, dx + 45, 870], fill=(190, 40, 40), outline=(100, 20, 20), width=2)
        draw.text((dx + 12, 830), "茶", font=get_font(FONT_BOLD, 16), fill=(255, 255, 255))
    draw.rectangle([u2 + 120, 880, u2 + 392, 950], fill=(0, 135, 90))
    draw.text((u2 + 140, 895), "清心福全 人氣熱銷飲品", font=get_font(FONT_BOLD, 20), fill=(255, 255, 255))

    # --------------------------------------------------------------------------
    # Unit 4 (1536 ~ 2048): 台灣第一家碳烤鹽酥雞・信安中醫診所
    # --------------------------------------------------------------------------
    u3 = unit_w * 3
    draw_tiled_pattern(draw, (u3, 0, u3 + unit_w, 650), tile_w=36, tile_h=16,
                       color1=(180, 85, 60), color2=(165, 75, 50),
                       mortar_color=(195, 185, 175), mortar_w=2)

    draw.rectangle([u3 + 60, 360, u3 + 452, 540], fill=(40, 55, 65))
    draw.rectangle([u3 + 80, 380, u3 + 432, 520], fill=(255, 255, 255), outline=(0, 100, 50), width=4)
    draw.text((u3 + 110, 400), "信 安 中 醫 診 所", font=get_font(FONT_BOLD, 28), fill=(0, 110, 60))
    draw.text((u3 + 120, 445), "健保特約・針灸・推拿・傷科", font=get_font(FONT_BOLD, 18), fill=(220, 30, 30))
    draw.text((u3 + 135, 480), "門診時間 09:00 - 21:30", font=get_font(FONT_BOLD, 16), fill=(40, 40, 40))

    draw.rectangle([u3 + 60, 80, u3 + 452, 260], fill=(45, 55, 60))
    draw.rectangle([u3 + 40, 50, u3 + 472, 80], fill=(20, 80, 160))
    for bx in range(u3 + 60, u3 + 452, 22):
        draw.line([bx, 80, bx, 260], fill=(210, 210, 210), width=2)
    for px in range(u3 + 90, u3 + 430, 70):
        draw.rectangle([px, 240, px + 40, 260], fill=(160, 80, 40))
        draw.ellipse([px - 5, 215, px + 45, 245], fill=(30, 140, 50))

    draw.rectangle([u3 + 10, 650, u3 + unit_w - 10, 770], fill=(220, 30, 20), outline=(255, 215, 0), width=4)
    draw.text((u3 + 25, 665), "台 灣 第 一 家 碳 烤 鹽 酥 雞", font=get_font(FONT_BOLD, 32), fill=(255, 255, 255))
    draw.text((u3 + 40, 715), "碳烤大雞排・深海魷魚・香酥甜不辣・無骨鹽酥雞", font=get_font(FONT_BOLD, 18), fill=(255, 225, 80))

    draw.rectangle([u3, 770, u3 + unit_w, 1024], fill=(230, 225, 220))
    draw.rectangle([u3 + 80, 830, u3 + 432, 980], fill=(60, 65, 70), outline=(220, 30, 20), width=3)
    draw.rectangle([u3 + 90, 840, u3 + 422, 920], fill=(255, 230, 160))
    draw.text((u3 + 140, 860), "美味食材 歡迎自夾", font=get_font(FONT_BOLD, 24), fill=(180, 30, 20))
    draw.rectangle([u3 + 100, 930, u3 + 412, 975], fill=(200, 205, 210))
    draw.text((u3 + 160, 940), "現 點 現 炸 碳 烤 特 製", font=get_font(FONT_BOLD, 18), fill=(30, 30, 30))

    for rx in range(0, W, 12):
        draw.rectangle([rx, 0, rx + 6, 25], fill=(40, 130, 90))
        draw.rectangle([rx + 6, 0, rx + 12, 25], fill=(25, 95, 65))

    im.save(os.path.join(out_dir, "xinzhuang_old_street_facade.png"))
    print("✓ Xinzhuang Old Street textures generated.")

# ==============================================================================
# 4. Changyi Danmark Residence Textures (1024 x 1024)
# ==============================================================================
def generate_changyi_danmark_textures():
    out_dir = "src/guanxin_sim/models/changyi_danmark_residence/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1024, 1024
    im = Image.new("RGB", (W, H), (235, 230, 220))
    draw = ImageDraw.Draw(im)

    # 4.1 Base Floors 1F-2F: Rusticated Granite Cladding (Y: 820 ~ 1024)
    draw_tiled_pattern(draw, (0, 820, W, 1024), tile_w=64, tile_h=32,
                       color1=(215, 205, 185), color2=(200, 190, 170),
                       mortar_color=(120, 110, 95), mortar_w=3)
    for ax in [100, 320, 540, 760]:
        draw.rectangle([ax, 860, ax + 160, 1024], fill=(30, 42, 50), outline=(160, 140, 110), width=4)
        draw.rectangle([ax - 10, 835, ax + 170, 860], fill=(40, 40, 45), outline=(215, 185, 120), width=2)

    draw.text((105, 840), "歐 洲 村 精 品 迴 廊", font=get_font(FONT_BOLD, 14), fill=(230, 210, 150))
    draw.text((325, 840), "昌益丹麥 迎賓大廳", font=get_font(FONT_BOLD, 14), fill=(230, 210, 150))
    draw.text((545, 840), "日 光 牙 醫 美 學", font=get_font(FONT_BOLD, 14), fill=(230, 210, 150))
    draw.text((765, 840), "有 機 烘 焙 坊", font=get_font(FONT_BOLD, 14), fill=(230, 210, 150))

    # 4.2 Residential Tower Facade 3F~14F (Y: 100 ~ 820)
    draw_tiled_pattern(draw, (0, 100, W, 820), tile_w=32, tile_h=12,
                       color1=(185, 105, 75), color2=(170, 95, 65),
                       mortar_color=(205, 195, 185), mortar_w=2)

    col_x = [0, 128, 256, 384, 512, 640, 768, 896, 1024]
    for cx in col_x:
        draw.rectangle([cx - 8, 100, cx + 8, 820], fill=(240, 238, 235), outline=(190, 185, 180), width=2)

    for fy in range(100, 820, 60):
        draw.rectangle([0, fy - 4, W, fy + 4], fill=(240, 238, 235), outline=(190, 185, 180), width=1)

    for fy in range(100, 820, 60):
        for i in range(len(col_x) - 1):
            wx0 = col_x[i] + 16
            wx1 = col_x[i+1] - 16
            wy0 = fy + 8
            wy1 = fy + 52
            draw.rectangle([wx0, wy0, wx1, wy1], fill=(25, 40, 45), outline=(60, 55, 50), width=2)
            draw.rectangle([wx0 + 4, wy0 + 4, wx0 + (wx1 - wx0)//2 - 2, wy1 - 4], fill=(45, 65, 72))
            draw.rectangle([wx0 + (wx1 - wx0)//2 + 2, wy0 + 4, wx1 - 4, wy1 - 4], fill=(35, 52, 58))
            draw.rectangle([wx0, wy1 - 16, wx1, wy1], fill=(180, 195, 205), outline=(120, 130, 140), width=1)

    # 4.3 Rooftop Classical Cornice Crown (Y: 0 ~ 100)
    draw.rectangle([0, 0, W, 100], fill=(70, 75, 80))
    draw.rectangle([0, 40, W, 70], fill=(225, 220, 210))
    draw.rectangle([0, 70, W, 85], fill=(160, 85, 60))
    draw.text((W // 2 - 160, 45), "CHANGYI DANMARK RESIDENCE", font=get_font(FONT_BOLD, 18), fill=(50, 50, 50))

    im.save(os.path.join(out_dir, "changyi_danmark_tile_facade.png"))
    print("✓ Changyi Danmark textures generated.")

# ==============================================================================
# 5. Guandong Civic Market Textures (1024 x 1024)
# ==============================================================================
def generate_guandong_market_textures():
    out_dir = "src/guanxin_sim/models/guandong_civic_market/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1024, 1024
    im = Image.new("RGB", (W, H), (230, 225, 215))
    draw = ImageDraw.Draw(im)

    # 5.1 Main Municipal Sign Header (Y: 200 ~ 360)
    draw.rectangle([0, 200, W, 360], fill=(190, 35, 30))
    draw.rectangle([0, 350, W, 360], fill=(255, 215, 0))

    font_mkt_big = get_font(FONT_BOLD, 54)
    font_mkt_sub = get_font(FONT_BOLD, 26)

    draw.text((80, 225), "新竹市關東公有零售市場", font=font_mkt_big, fill=(255, 255, 255))
    draw.text((120, 298), "客家美食文化會館・新竹市立圖書館關東分館", font=font_mkt_sub, fill=(255, 235, 140))

    # 5.2 Upper Civic Building Floors 2F~4F (Y: 0 ~ 200)
    draw_tiled_pattern(draw, (0, 0, W, 200), tile_w=32, tile_h=16,
                       color1=(210, 195, 175), color2=(195, 180, 160),
                       mortar_color=(170, 160, 145), mortar_w=2)
    for lx in range(60, W - 60, 180):
        draw.rectangle([lx, 30, lx + 140, 170], fill=(35, 48, 55), outline=(80, 80, 80), width=3)
        for ly in range(45, 165, 20):
            draw.line([lx, ly, lx + 140, ly], fill=(180, 150, 100), width=3)

    # 5.3 Middle Transom & Floor Directory (Y: 360 ~ 580)
    draw.rectangle([0, 360, W, 580], fill=(245, 240, 230))
    draw.rectangle([80, 390, 480, 540], fill=(255, 255, 255), outline=(190, 35, 30), width=3)
    draw.text((100, 405), "【樓層導覽 指引】", font=get_font(FONT_BOLD, 24), fill=(190, 35, 30))
    draw.text((100, 445), "4F 新竹市立圖書館關東分館", font=get_font(FONT_BOLD, 18), fill=(40, 40, 40))
    draw.text((100, 475), "3F 客家文化推廣會館・研習教室", font=get_font(FONT_BOLD, 18), fill=(40, 40, 40))
    draw.text((100, 505), "1F-2F 傳統生鮮公有零售市場", font=get_font(FONT_BOLD, 18), fill=(40, 40, 40))

    draw.rectangle([540, 390, 944, 540], fill=(0, 90, 140), outline=(255, 255, 255), width=3)
    draw.text((560, 410), "關東客家風情", font=get_font(FONT_BOLD, 28), fill=(255, 225, 100))
    draw.text((560, 460), "傳承百年新竹好滋味", font=get_font(FONT_BOLD, 22), fill=(255, 255, 255))
    draw.text((560, 500), "客家米食・在地小農生鮮", font=get_font(FONT_BOLD, 18), fill=(220, 240, 255))

    # 5.4 Ground Floor Morning Market (Y: 580 ~ 1024)
    canopy_colors = [
        [(220, 40, 40), (255, 255, 255)],
        [(30, 80, 180), (255, 255, 255)],
        [(220, 40, 40), (255, 255, 255)],
        [(30, 120, 60), (255, 255, 255)],
    ]
    stalls = [
        ("溫體黑毛土豬肉", "梨山產地直銷蔬果"),
        ("新竹手工貢丸米粉", "現宰土雞・鹽水雞"),
        ("客家傳統米食菜包", "現撈澎湖海鮮魚產"),
        ("古早味熟食滷味", "阿嬤現炸天婦羅雞捲"),
    ]

    for i in range(4):
        sx0 = i * 256
        sx1 = sx0 + 256
        for bx in range(sx0, sx1, 32):
            col = canopy_colors[i][(bx // 32) % 2]
            draw.rectangle([bx, 580, bx + 32, 680], fill=col)

        draw.rectangle([sx0 + 10, 680, sx1 - 10, 1000], fill=(235, 230, 225), outline=(160, 150, 140), width=2)
        draw.rectangle([sx0 + 15, 690, sx1 - 15, 750], fill=(255, 240, 180), outline=(180, 40, 20), width=2)
        draw.text((sx0 + 25, 705), stalls[i][0], font=get_font(FONT_BOLD, 22), fill=(180, 20, 20))
        draw.rectangle([sx0 + 20, 760, sx1 - 20, 940], fill=(210, 215, 220), outline=(100, 100, 100), width=2)
        draw.text((sx0 + 30, 780), stalls[i][1], font=get_font(FONT_BOLD, 18), fill=(30, 30, 30))
        draw.text((sx0 + 35, 830), "產地直銷\n新鮮衛生\n天天便宜！", font=get_font(FONT_BOLD, 20), fill=(160, 30, 30))

    draw.rectangle([0, 1000, W, 1024], fill=(70, 72, 75))

    im.save(os.path.join(out_dir, "guandong_market_facade.png"))
    print("✓ Guandong Market textures generated.")

if __name__ == "__main__":
    generate_711_textures()
    generate_pxmart_textures()
    generate_xinzhuang_old_street_textures()
    generate_changyi_danmark_textures()
    generate_guandong_market_textures()
    print("All Taiwanese building surface textures generated successfully!")
