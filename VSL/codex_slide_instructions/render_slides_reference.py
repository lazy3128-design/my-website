"""
UTAGE VSL スライドレンダリング 参考実装
=========================================

Codexはこれを参考に8つの関数を実装してください。
本実装はサンプル動作確認用。実運用時は Noto Sans JP Bold/Medium のフォントパスに差し替えてください。

【依存】
- Pillow (PIL)
- 日本語フォント（システムにNoto Sans JP / ヒラギノ角ゴ / 游ゴシック等が必要）

【出力】1920×1080 PNG
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import random
import math

# ========================================
# 共通定数
# ========================================
WIDTH, HEIGHT = 1920, 1080
SAFE_MARGIN = 120
WIPE_AREA = (1440, 0, 1920, 270)  # 右上 顔ワイプ予約
SUBTITLE_AREA_Y = 960  # 下120pxは字幕用

# UTAGEブランドカラー（HEX→RGB変換用）
def hex2rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

BRAND_BLUE = "#58A3E6"
BRAND_PURPLE = "#A75FF5"
DEEP_BLUE = "#396995"
DEEP_PURPLE = "#6C3D9F"
MID_BLUE = "#4A8AC3"
MID_PURPLE = "#8D50D0"
SOFT_BLUE = "#ABD1F2"
SOFT_PURPLE = "#D3AFFA"
TINT_BLUE = "#E5F1FB"
TINT_PURPLE = "#F1E7FD"
WHITE_BG = "#FAFAF7"
TEXT_DARK = "#1A1F36"
TEXT_MID = "#5A6378"
TEXT_SOFT = "#9CA3AF"
HIGHLIGHT_BLUE = "#2563EB"
HIGHLIGHT_GOLD = "#D4A04C"
SOFT_CORAL = "#C56B5A"
CTA_GREEN = "#25A04A"

# フォント設定（環境に応じて差し替え）
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 仮：本番はNotoSansJP-Bold.ttf
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # 仮：本番はNotoSansJP-Regular.ttf
FONT_JP_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"  # 日本語対応


def get_font(size: int, bold: bool = True):
    """フォント取得（日本語対応・サイズ指定）"""
    try:
        # 日本語対応フォントを優先
        return ImageFont.truetype(FONT_JP_PATH, size)
    except Exception:
        return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_REG_PATH, size)


# ========================================
# ヘルパー：グラデーション背景
# ========================================
def make_diagonal_gradient(start_color: str, end_color: str) -> Image.Image:
    """斜め45度のグラデーション背景を生成"""
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    sr, sg, sb = hex2rgb(start_color)
    er, eg, eb = hex2rgb(end_color)
    # 対角線距離で補間
    max_d = WIDTH + HEIGHT
    for y in range(HEIGHT):
        for x in range(WIDTH):
            t = (x + (HEIGHT - y)) / max_d
            r = int(sr + (er - sr) * t)
            g = int(sg + (eg - sg) * t)
            b = int(sb + (eb - sb) * t)
            pixels[x, y] = (r, g, b)
    return img


def make_subtle_texture(img: Image.Image, opacity: float = 0.05) -> Image.Image:
    """背景に微細な粒子テクスチャを重ねる"""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for _ in range(3000):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        alpha = int(255 * opacity * random.random())
        c = random.choice([(255, 255, 255), (200, 200, 220)])
        draw.point((x, y), fill=(*c, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def draw_centered_text(draw, text_lines: list, font_size: int, color: str, line_spacing: float = 1.6, emphasis_index: int = None, emphasis_ratio: float = 1.8):
    """テキストを中央寄せで描画（複数行・強調行対応）"""
    base_font = get_font(font_size, bold=True)
    emphasis_font = get_font(int(font_size * emphasis_ratio), bold=True) if emphasis_index is not None else None

    # 各行の高さを算出
    line_heights = []
    for i, line in enumerate(text_lines):
        f = emphasis_font if i == emphasis_index else base_font
        if not line.strip():
            line_heights.append(int(font_size * 0.5))
        else:
            bbox = draw.textbbox((0, 0), line, font=f)
            line_heights.append(bbox[3] - bbox[1])

    total_h = sum(line_heights) + int(font_size * (line_spacing - 1)) * (len(text_lines) - 1)
    start_y = (HEIGHT - total_h) // 2

    y = start_y
    for i, line in enumerate(text_lines):
        if not line.strip():
            y += line_heights[i] + int(font_size * (line_spacing - 1))
            continue
        f = emphasis_font if i == emphasis_index else base_font
        bbox = draw.textbbox((0, 0), line, font=f)
        text_w = bbox[2] - bbox[0]
        # 右上ワイプエリアと衝突する場合は中央位置を左にずらす
        x = (WIDTH - text_w) // 2
        if y < WIPE_AREA[3] and x + text_w > WIPE_AREA[0]:
            x = max(SAFE_MARGIN, (WIPE_AREA[0] - text_w) // 2)
        draw.text((x, y), line, fill=color, font=f)
        y += line_heights[i] + int(font_size * (line_spacing - 1))


# ========================================
# パターン①：UTAGEブランドグラデーション
# ========================================
def render_pattern_1_gradient(
    text_lines: list,
    slide_id: str,
    output_dir: str = "./slides",
    emphasis_index: int = None,
    emphasis_size_ratio: float = 1.8,
):
    img = make_diagonal_gradient(BRAND_BLUE, BRAND_PURPLE)
    img = make_subtle_texture(img, opacity=0.04)
    draw = ImageDraw.Draw(img)
    base_size = 64 if len(text_lines) > 5 else 72
    draw_centered_text(draw, text_lines, base_size, "white",
                       line_spacing=1.7, emphasis_index=emphasis_index,
                       emphasis_ratio=emphasis_size_ratio)
    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# パターン②：ディープパープル
# ========================================
def render_pattern_2_deep_purple(
    text_lines: list,
    slide_id: str,
    output_dir: str = "./slides",
    emphasis_index: int = None,
    side_band: bool = True,
):
    img = Image.new("RGB", (WIDTH, HEIGHT), DEEP_PURPLE)
    img = make_subtle_texture(img, opacity=0.05)
    draw = ImageDraw.Draw(img)
    if side_band:
        # 左上にコーラル縦帯
        draw.rectangle([60, 60, 60 + 8, 60 + 200], fill=SOFT_CORAL)
    base_size = 60
    # 強調行はSOFT_PURPLEで描画したいが、ここでは色は統一して大きさのみ強調
    draw_centered_text(draw, text_lines, base_size, "white",
                       line_spacing=1.5,
                       emphasis_index=emphasis_index, emphasis_ratio=1.4)
    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# パターン③-list：白＋箇条書き
# ========================================
def render_pattern_3_list(
    section_title: str,
    items: list,
    slide_id: str = "",
    output_dir: str = "./slides",
    intro_text: str = "",
):
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE_BG)
    draw = ImageDraw.Draw(img)
    # 上部セクション帯
    draw.rectangle([SAFE_MARGIN, 90, SAFE_MARGIN + 6, 90 + 50], fill=BRAND_PURPLE)
    title_font = get_font(28, bold=True)
    draw.text((SAFE_MARGIN + 24, 96), section_title, fill=TEXT_DARK, font=title_font)
    # イントロ
    y = 220
    if intro_text:
        intro_font = get_font(36, bold=True)
        bbox = draw.textbbox((0, 0), intro_text, font=intro_font)
        intro_w = bbox[2] - bbox[0]
        draw.text(((WIDTH - intro_w) // 2, y), intro_text, fill=TEXT_DARK, font=intro_font)
        y += 100
    # 各項目
    item_font = get_font(34, bold=True)
    for i, item in enumerate(items):
        # ① 〜⑤ の番号付き or ✅ プレフィックス
        prefix = f"{chr(0x2460 + i)} "  # ①②③④⑤
        text = prefix + item
        bbox = draw.textbbox((0, 0), text, font=item_font)
        text_w = bbox[2] - bbox[0]
        x = (WIDTH - text_w) // 2
        # 中央寄せ
        draw.text((x, y), text, fill=TEXT_DARK, font=item_font)
        y += 75
    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# パターン③-card：白＋実績カード
# ========================================
def render_pattern_3_card(
    business_role: str,
    name: str,
    metrics: list,
    quote: str = None,
    photo_path: str = None,
    slide_id: str = "",
    output_dir: str = "./slides",
):
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE_BG)
    draw = ImageDraw.Draw(img)
    # 上部セクション帯
    draw.rectangle([SAFE_MARGIN, 90, SAFE_MARGIN + 6, 90 + 50], fill=BRAND_PURPLE)
    title_font = get_font(28, bold=True)
    draw.text((SAFE_MARGIN + 24, 96), "| 実績", fill=TEXT_DARK, font=title_font)

    # 左に円形顔写真
    photo_size = 320
    photo_x = SAFE_MARGIN + 50
    photo_y = 280
    if photo_path and Path(photo_path).exists():
        try:
            photo = Image.open(photo_path).convert("RGB").resize((photo_size, photo_size), Image.LANCZOS)
            # 円形マスク
            mask = Image.new("L", (photo_size, photo_size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, photo_size, photo_size), fill=255)
            img.paste(photo, (photo_x, photo_y), mask)
        except Exception:
            draw.ellipse([photo_x, photo_y, photo_x+photo_size, photo_y+photo_size], outline=TEXT_MID, width=3)
    else:
        # ダミー円
        draw.ellipse([photo_x, photo_y, photo_x+photo_size, photo_y+photo_size], fill=TINT_PURPLE)

    # 右側にテキスト
    text_x = photo_x + photo_size + 80
    # 業種小キャプション
    role_font = get_font(24, bold=False)
    draw.text((text_x, photo_y + 20), business_role, fill=TEXT_MID, font=role_font)
    # 名前
    name_font = get_font(48, bold=True)
    draw.text((text_x, photo_y + 70), name, fill=TEXT_DARK, font=name_font)
    # 数字
    metric_font = get_font(36, bold=True)
    y = photo_y + 160
    for m in metrics:
        # 数字部分（→の周辺）を金色にしたいが、簡略化のため全体DARK
        draw.text((text_x, y), m, fill=TEXT_DARK, font=metric_font)
        y += 60

    # クオート（下部）
    if quote:
        quote_y = photo_y + photo_size + 80
        draw.rectangle([SAFE_MARGIN, quote_y - 20, SAFE_MARGIN + 8, quote_y + 80], fill=BRAND_BLUE)
        quote_font = get_font(28, bold=False)
        draw.text((SAFE_MARGIN + 28, quote_y), f"「{quote}」", fill=TEXT_DARK, font=quote_font)

    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# パターン④：センチメンタル
# ========================================
def render_pattern_4_sentimental(
    text_lines: list,
    background_concept: str,
    slide_id: str = "",
    output_dir: str = "./slides",
):
    # 抽象的なグラデ背景（風景の代わり）
    img = make_diagonal_gradient(SOFT_BLUE, SOFT_PURPLE)
    img = make_subtle_texture(img, opacity=0.06)
    # オーバーレイ
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (*hex2rgb(DEEP_BLUE), 100))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw_centered_text(draw, text_lines, 52, "white", line_spacing=1.7)
    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# パターン⑤：ディープイマージョン
# ========================================
def render_pattern_5_dark(
    text_lines: list,
    is_quote: bool = True,
    slide_id: str = "",
    output_dir: str = "./slides",
):
    img = Image.new("RGB", (WIDTH, HEIGHT), TEXT_DARK)
    # 紫青の星雲もや
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for _ in range(200):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(30, 80)
        c = random.choice([hex2rgb(MID_PURPLE), hex2rgb(DEEP_BLUE)])
        alpha = random.randint(10, 40)
        odraw.ellipse([x-r, y-r, x+r, y+r], fill=(*c, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw_centered_text(draw, text_lines, 68, "white", line_spacing=1.6)
    out = Path(output_dir) / f"slide_{slide_id}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return out


# ========================================
# 10枚サンプル一括実行
# ========================================
if __name__ == "__main__":
    import json

    data_path = Path(__file__).parent / "10slides_sample_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    function_map = {
        "p1_gradient":     render_pattern_1_gradient,
        "p2_deep_purple":  render_pattern_2_deep_purple,
        "p3_list":         render_pattern_3_list,
        "p3_card":         render_pattern_3_card,
        "p4_sentimental":  render_pattern_4_sentimental,
        "p5_dark":         render_pattern_5_dark,
    }

    out_dir = "/tmp/utage_slides_sample"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for slide in data["slides"]:
        func = function_map.get(slide["pattern"])
        if not func:
            print(f"⚠ Unknown pattern: {slide['pattern']}")
            continue
        params = dict(slide["params"])
        # photo_pathの相対パスを絶対パスに（顔写真は別途用意）
        if "photo_path" in params:
            params["photo_path"] = f"/tmp/utage_thumbs/{Path(params['photo_path']).name.replace('01_kato','01_kato').replace('02_tezuka','02_tezuka')}"
        result = func(slide_id=slide["id"], output_dir=out_dir, **params)
        print(f"✓ slide_{slide['id']}.png ({slide['pattern']}) → {result}")
