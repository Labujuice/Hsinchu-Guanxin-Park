#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate exact aspect-ratio, ultra-high-clarity Taiwanese shop signs and architectural textures.
Every texture is mathematically matched 1:1 to the 3D box geometry dimensions to eliminate any distortion.
Also synchronizes all materials folders into install/ directory.
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_REGULAR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def sync_materials_to_install(model_name):
    src_mat = os.path.join("src/guanxin_sim/models", model_name, "materials")
    dst_mat = os.path.join("install/guanxin_sim/share/guanxin_sim/models", model_name, "materials")
    if os.path.exists(src_mat):
        os.makedirs(os.path.dirname(dst_mat), exist_ok=True)
        if os.path.exists(dst_mat):
            shutil.rmtree(dst_mat)
        shutil.copytree(src_mat, dst_mat)
        print(f"✓ Synced {model_name}/materials to install/")

# ==============================================================================
# 1. 7-ELEVEN Signboards (Aspect Ratio: 15.0m x 1.4m = 10.71:1)
# ==============================================================================
def gen_711():
    out_dir = "src/guanxin_sim/models/convenience_store_711/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    # 1.1 Main Fascia Signboard (1500 x 140, ratio 10.71:1)
    W, H = 1500, 140
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)

    # Tri-color horizontal stripes across the top
    d.rectangle([0, 0, W, 22], fill=(234, 91, 12))     # Orange
    d.rectangle([0, 22, W, 44], fill=(0, 132, 61))     # Green
    d.rectangle([0, 44, W, 66], fill=(227, 27, 35))    # Red
    d.rectangle([0, 66, W, H], fill=(255, 255, 255))   # White main field

    # 7-Eleven Logo on the left
    d.rectangle([30, 8, 140, 125], fill=(0, 132, 61), outline=(234, 91, 12), width=3)
    d.text((60, 10), "7", font=get_font(FONT_BOLD, 90), fill=(234, 91, 12))
    d.rectangle([30, 68, 140, 92], fill=(227, 27, 35))
    d.text((36, 70), "ELEVEN", font=get_font(FONT_BOLD, 22), fill=(255, 255, 255))

    # Bold store typography
    d.text((170, 72), "7-ELEVEN", font=get_font(FONT_BOLD, 52), fill=(227, 27, 35))
    d.text((430, 74), "新竹關新門市", font=get_font(FONT_BOLD, 52), fill=(0, 132, 61))

    # Badges on the right
    d.rectangle([980, 72, 1120, 126], fill=(255, 215, 0), outline=(200, 160, 0), width=2)
    d.text((995, 82), "★ 24H 營業", font=get_font(FONT_BOLD, 24), fill=(30, 30, 30))

    d.rectangle([1140, 72, 1300, 126], fill=(234, 91, 12))
    d.text((1155, 84), "CITY CAFE", font=get_font(FONT_BOLD, 24), fill=(255, 255, 255))

    d.rectangle([1320, 72, 1470, 126], fill=(245, 245, 245), outline=(0, 132, 61), width=2)
    d.text((1340, 84), "iBon・ATM", font=get_font(FONT_BOLD, 22), fill=(0, 132, 61))

    im.save(os.path.join(out_dir, "seven_eleven_fascia_sign.png"))

    # 1.2 Blade Sign (512 x 1024, ratio 1:2)
    W_b, H_b = 512, 1024
    im_b = Image.new("RGB", (W_b, H_b), (255, 255, 255))
    db = ImageDraw.Draw(im_b)
    db.rectangle([0, 0, W_b, H_b], outline=(80, 80, 80), width=8)
    db.rectangle([8, 8, 38, H_b - 8], fill=(234, 91, 12))
    db.rectangle([38, 8, 68, H_b - 8], fill=(0, 132, 61))
    db.rectangle([68, 8, 98, H_b - 8], fill=(227, 27, 35))

    db.rectangle([130, 50, 470, 350], fill=(0, 132, 61), outline=(234, 91, 12), width=6)
    db.text((220, 55), "7", font=get_font(FONT_BOLD, 240), fill=(234, 91, 12))
    db.rectangle([130, 200, 470, 265], fill=(227, 27, 35))
    db.text((145, 205), "ELEVEN", font=get_font(FONT_BOLD, 54), fill=(255, 255, 255))

    chars = ["關", "新", "門", "市"]
    y_pos = 420
    for ch in chars:
        db.text((230, y_pos), ch, font=get_font(FONT_BOLD, 96), fill=(0, 132, 61))
        y_pos += 115

    db.rectangle([130, 890, 470, 980], fill=(234, 91, 12))
    db.text((170, 905), "24H 營業", font=get_font(FONT_BOLD, 52), fill=(255, 255, 255))
    im_b.save(os.path.join(out_dir, "seven_eleven_blade_sign.png"))
    sync_materials_to_install("convenience_store_711")

# ==============================================================================
# 2. PX MART Signboards (Aspect Ratio: 24.0m x 2.4m = 10.0:1)
# ==============================================================================
def gen_pxmart():
    out_dir = "src/guanxin_sim/models/px_mart_store/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    # 2.1 Main Fascia Signboard (1600 x 160, ratio 10.0:1)
    W, H = 1600, 160
    im = Image.new("RGB", (W, H), (0, 45, 110)) # PX Blue
    d = ImageDraw.Draw(im)

    # Red bottom accent stripe
    d.rectangle([0, H - 20, W, H], fill=(215, 20, 40))

    # Concentric circles logo
    cx, cy, cr = 100, 70, 50
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255))
    d.ellipse([cx - cr + 10, cy - cr + 10, cx + cr - 10, cy + cr - 10], fill=(0, 45, 110))
    d.ellipse([cx - cr + 24, cy - cr + 24, cx + cr - 24, cy + cr - 24], fill=(215, 20, 40))
    d.ellipse([cx - cr + 36, cy - cr + 36, cx + cr - 36, cy + cr - 36], fill=(255, 255, 255))

    # Giant typography
    d.text((190, 24), "全聯福利中心", font=get_font(FONT_BOLD, 76), fill=(255, 255, 255))
    d.text((680, 36), "PX MART", font=get_font(FONT_BOLD, 62), fill=(255, 255, 255))
    d.text((1020, 45), "關新旗艦店", font=get_font(FONT_BOLD, 44), fill=(255, 215, 0))

    d.text((195, 112), "買進美好生活・生鮮蔬果・請支援收銀！", font=get_font(FONT_BOLD, 22), fill=(255, 235, 120))
    d.text((1020, 112), "營業時間 08:00 - 23:00", font=get_font(FONT_BOLD, 20), fill=(255, 255, 255))

    im.save(os.path.join(out_dir, "pxmart_fascia_sign.png"))

    # 2.2 Blade Sign (512 x 1024, ratio 1:2)
    W_b, H_b = 512, 1024
    im_b = Image.new("RGB", (W_b, H_b), (0, 45, 110))
    db = ImageDraw.Draw(im_b)
    db.rectangle([0, 0, W_b, H_b], outline=(255, 255, 255), width=8)
    db.rectangle([10, H_b - 50, W_b - 10, H_b - 10], fill=(215, 20, 40))

    cx, cy, cr = 256, 150, 95
    db.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255))
    db.ellipse([cx - cr + 20, cy - cr + 20, cx + cr - 20, cy + cr - 20], fill=(0, 45, 110))
    db.ellipse([cx - cr + 46, cy - cr + 46, cx + cr - 46, cy + cr - 46], fill=(215, 20, 40))
    db.ellipse([cx - cr + 68, cy - cr + 68, cx + cr - 68, cy + cr - 68], fill=(255, 255, 255))

    chars = ["全", "聯", "福", "利", "中", "心"]
    y_pos = 280
    for ch in chars:
        db.text((176, y_pos), ch, font=get_font(FONT_BOLD, 92), fill=(255, 255, 255))
        y_pos += 105

    im_b.save(os.path.join(out_dir, "pxmart_blade_sign.png"))
    sync_materials_to_install("px_mart_store")

# ==============================================================================
# 3. Xinzhuang Old Street 4 Shophouse Signs (Aspect Ratio: 12.0m x 1.5m = 8.0:1)
# ==============================================================================
def gen_xinzhuang_signs():
    out_dir = "src/guanxin_sim/models/xinzhuang_street_block/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1200, 150  # 8.0:1

    # Shop 1: 林記老麵手工小籠包
    im1 = Image.new("RGB", (W, H), (255, 225, 0)) # Yellow
    d1 = ImageDraw.Draw(im1)
    d1.rectangle([0, 0, W, H], outline=(200, 30, 20), width=6)
    d1.text((40, 22), "林記老麵手工小籠包", font=get_font(FONT_BOLD, 68), fill=(210, 20, 20))
    d1.text((700, 35), "永和傳統豆漿・燒餅油條・手工蛋餅", font=get_font(FONT_BOLD, 32), fill=(30, 30, 30))
    d1.text((700, 90), "營業時間：05:30 - 13:30 (每週一公休)", font=get_font(FONT_BOLD, 22), fill=(60, 60, 60))
    im1.save(os.path.join(out_dir, "sign_xiaolongbao.png"))

    # Shop 2: KYMCO 光陽機車
    im2 = Image.new("RGB", (W, H), (220, 25, 35)) # Red
    d2 = ImageDraw.Draw(im2)
    d2.rectangle([0, 0, W, H], outline=(0, 40, 120), width=6)
    d2.rectangle([20, 20, 420, H - 20], fill=(255, 255, 255))
    d2.text((35, 35), "KYMCO 光陽機車", font=get_font(FONT_BOLD, 46), fill=(220, 25, 35))
    d2.text((460, 25), "新莊機車保修廠・環保排氣定檢站", font=get_font(FONT_BOLD, 44), fill=(255, 255, 255))
    d2.text((465, 88), "道路救援・電腦噴射檢測・換正廠機油 150 起", font=get_font(FONT_BOLD, 28), fill=(255, 230, 120))
    im2.save(os.path.join(out_dir, "sign_kymco.png"))

    # Shop 3: 清心福全冷飲站
    im3 = Image.new("RGB", (W, H), (0, 135, 90)) # Jade Green
    d3 = ImageDraw.Draw(im3)
    d3.rectangle([0, 0, W, H], outline=(255, 255, 255), width=5)
    d3.ellipse([40, 40, 100, 100], fill=(225, 30, 40)) # Heart
    d3.text((120, 24), "清心福全", font=get_font(FONT_BOLD, 74), fill=(255, 255, 255))
    d3.text((450, 42), "新竹新莊店", font=get_font(FONT_BOLD, 40), fill=(255, 225, 120))
    d3.text((700, 32), "烏龍綠茶・珍珠奶茶・優多綠", font=get_font(FONT_BOLD, 36), fill=(255, 255, 255))
    d3.text((700, 88), "產地直選茶葉・天天現泡好茶", font=get_font(FONT_BOLD, 24), fill=(230, 255, 240))
    im3.save(os.path.join(out_dir, "sign_chingshin.png"))

    # Shop 4: 台灣第一家碳烤鹽酥雞
    im4 = Image.new("RGB", (W, H), (215, 25, 20)) # Night Market Red
    d4 = ImageDraw.Draw(im4)
    d4.rectangle([0, 0, W, H], outline=(255, 215, 0), width=6)
    d4.text((40, 22), "台灣第一家碳烤鹽酥雞", font=get_font(FONT_BOLD, 64), fill=(255, 255, 255))
    d4.text((720, 32), "碳烤大雞排・深海魷魚・香酥甜不辣", font=get_font(FONT_BOLD, 30), fill=(255, 225, 80))
    d4.text((720, 88), "獨家秘製醬汁・現點現烤・營業至凌晨 01:00", font=get_font(FONT_BOLD, 22), fill=(255, 255, 255))
    im4.save(os.path.join(out_dir, "sign_yansuji.png"))

    sync_materials_to_install("xinzhuang_street_block")

# ==============================================================================
# 4. Guangfu Road 9 Commercial Signs (Aspect Ratio: 16.0m x 1.4m = 11.43:1)
# ==============================================================================
def gen_guangfu_signs():
    out_dir = "src/guanxin_sim/models/guangfu_south_strip_east/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1143, 100  # 11.43:1

    shops = [
        ("sign_esun.png", "玉山銀行 E.SUN BANK", "新竹分行・24H 智慧 ATM", (0, 135, 90), (255, 255, 255), (255, 255, 255)),
        ("sign_great_tree.png", "大樹連鎖藥局", "Great Tree Pharmacy・健保特約處方箋", (235, 95, 15), (255, 255, 255), (255, 255, 255)),
        ("sign_tokiya.png", "王品 陶板屋", "和風創作料理・新竹光復店", (85, 25, 75), (255, 230, 150), (240, 210, 130)),
        ("sign_50lan.png", "50 嵐", "經典手搖茶飲・四季春茶・波霸奶茶", (255, 215, 0), (0, 45, 120), (0, 45, 120)),
        ("sign_chunshuitang.png", "春 水 堂", "人文茶館・世界珍珠奶茶發源地", (42, 32, 28), (245, 220, 160), (210, 190, 140)),
        ("sign_dbs.png", "星展銀行 DBS BANK", "星展新竹財富管理中心・私人銀行", (215, 20, 30), (255, 255, 255), (255, 255, 255)),
        ("sign_anyoung.png", "安 永 鮮 物", "Anyoung Fresh・頂級產銷履歷健康超市", (0, 75, 135), (255, 255, 255), (180, 235, 255)),
        ("sign_taian.png", "台安聯合診所", "小兒科・家醫科・健保門診成人健檢", (0, 130, 100), (255, 255, 255), (255, 235, 150)),
        ("sign_watsons.png", "屈 臣 氏 Watsons", "個人保健與美妝門市・醫美保養專櫃", (0, 155, 160), (255, 255, 255), (255, 255, 255)),
    ]

    for fname, title, sub, bg, t_col, s_col in shops:
        im = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, H], outline=(255, 255, 255), width=3)
        d.text((40, 14), title, font=get_font(FONT_BOLD, 46), fill=t_col)
        d.text((620, 30), sub, font=get_font(FONT_BOLD, 26), fill=s_col)
        im.save(os.path.join(out_dir, fname))

    sync_materials_to_install("guangfu_south_strip_east")

# ==============================================================================
# 5. Guandong Market Sign (Aspect Ratio: 24.0m x 3.0m = 8.0:1)
# ==============================================================================
def gen_guandong_sign():
    out_dir = "src/guanxin_sim/models/guandong_civic_market/materials/textures"
    os.makedirs(out_dir, exist_ok=True)

    W, H = 1600, 200  # 8.0:1
    im = Image.new("RGB", (W, H), (190, 25, 20)) # Traditional Red
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], outline=(255, 215, 0), width=6)
    d.rectangle([0, H - 16, W, H], fill=(255, 215, 0))

    d.text((80, 24), "新竹市關東公有零售市場", font=get_font(FONT_BOLD, 84), fill=(255, 255, 255))
    d.text((1050, 45), "客家美食文化會館\n新竹市立圖書館關東分館", font=get_font(FONT_BOLD, 34), fill=(255, 235, 130))
    im.save(os.path.join(out_dir, "guandong_market_sign.png"))
    sync_materials_to_install("guandong_civic_market")

# Sync others as well
def sync_all():
    for m in ["changyi_danmark_residence", "fuyu_junding_tower"]:
        sync_materials_to_install(m)

if __name__ == "__main__":
    gen_711()
    gen_pxmart()
    gen_xinzhuang_signs()
    gen_guangfu_signs()
    gen_guandong_sign()
    sync_all()
    print("All exact-ratio signboards generated and synced successfully!")
