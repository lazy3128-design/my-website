"""
UTAGE VSL シーン別サンプル21枚を GPT-image-1 で一括生成

【前提】
- OpenAI APIキーが必要（環境変数 OPENAI_API_KEY または下記に直書き）
- pip install openai
- 21_prompts_data.json が同じディレクトリにある

【使い方】
$ pip install openai
$ export OPENAI_API_KEY="sk-..."（または下のAPI_KEY変数に直書き）
$ python generate_21_slides.py

【出力】
./slides_output/scene_01_理想未来.png
./slides_output/scene_02_雑務リスト導入.png
... (21枚)

【コスト概算】
gpt-image-1 standardサイズ1024×1024で約$0.04/枚 → 21枚 ≈ $0.84
1536×1024やhigh qualityにすると $0.08〜0.19/枚 → 21枚 ≈ $1.68〜$4.00
"""

import json
import base64
import os
import sys
from pathlib import Path
import time

# ============================
# 設定
# ============================
API_KEY = os.environ.get("OPENAI_API_KEY", "")  # 環境変数優先
# 直書きする場合は↓のコメントを外してキーを入れる
# API_KEY = "sk-..."

MODEL = "gpt-image-1"
SIZE = "1536x1024"   # 16:9に最も近いサイズ（1920x1080想定）
QUALITY = "high"     # "low" / "medium" / "high"

OUTPUT_DIR = "./slides_output"
PROMPTS_JSON = "./21_prompts_data.json"

# ============================
# 実行
# ============================
def main():
    if not API_KEY:
        print("❌ OPENAI_API_KEY が設定されていません。")
        print("   方法1: 環境変数 → export OPENAI_API_KEY='sk-...'")
        print("   方法2: このスクリプト14行目のAPI_KEYに直書き")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("❌ openai パッケージがインストールされていません。")
        print("   $ pip install openai")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY)

    with open(PROMPTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    common_suffix = data["_meta"].get("common_style_suffix", "")
    slides = data["slides"]

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"\n🎨 {len(slides)}枚の生成を開始します")
    print(f"   モデル: {MODEL} / サイズ: {SIZE} / 品質: {QUALITY}")
    print(f"   出力先: {OUTPUT_DIR}\n")

    results = []
    for i, slide in enumerate(slides, 1):
        sid = slide["id"]
        filename = slide["filename"]
        prompt = slide["prompt"] + common_suffix

        print(f"[{i:2d}/{len(slides)}] {sid} → {filename}")
        print(f"    生成中...", end="", flush=True)
        t0 = time.time()

        try:
            response = client.images.generate(
                model=MODEL,
                prompt=prompt,
                size=SIZE,
                quality=QUALITY,
                n=1,
            )
            img_data = base64.b64decode(response.data[0].b64_json)
            out_path = Path(OUTPUT_DIR) / filename
            with open(out_path, "wb") as f:
                f.write(img_data)
            elapsed = time.time() - t0
            size_kb = len(img_data) / 1024
            print(f" ✅ ({elapsed:.1f}秒, {size_kb:.0f}KB)")
            results.append({"id": sid, "ok": True, "file": str(out_path)})
        except Exception as e:
            elapsed = time.time() - t0
            print(f" ❌ エラー ({elapsed:.1f}秒): {e}")
            results.append({"id": sid, "ok": False, "error": str(e)})

    # サマリー
    print("\n" + "=" * 60)
    print("📊 サマリー")
    print("=" * 60)
    ok_count = sum(1 for r in results if r["ok"])
    print(f"  成功: {ok_count}/{len(results)}")
    if ok_count < len(results):
        print(f"  失敗:")
        for r in results:
            if not r["ok"]:
                print(f"    - {r['id']}: {r['error'][:80]}")
    print(f"\n  出力先: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
