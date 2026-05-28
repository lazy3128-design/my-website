# 21枚一括生成 — 完全自動化手順

**バージョン**：v3.0（一括生成版）
**作成日**：2026-05-28

1スライドずつ手動コピペは不要です。**Python 1コマンドで21枚を一気に生成**します。

---

## ⚠️ 通し版（v2_220）は今は不要

**Stage 1（21枚サンプル生成）の今段階では、通し版v2_220は添付不要です。**

理由：
- 21枚のプロンプトは既に `21_prompts_data.json` に正確な台本テキスト埋め込み済み
- このJSONがv2_220から抽出したテキストを保持しているため、改めて参照する必要なし

通し版が必要になるのは **Stage 2（残り199枚生成）** のタイミングです（そこで全220枚分のプロンプトをJSONに展開）。

---

## 必要なファイル（3つだけ）

```
1. generate_21_slides.py     ← 実行スクリプト
2. 21_prompts_data.json      ← 21枚分のプロンプトデータ
3. （OpenAI APIキー）          ← 環境変数 or スクリプト内に直書き
```

---

## 実行手順

### A. ローカル環境で実行（最短）

```bash
# 1. OpenAIライブラリをインストール
pip install openai

# 2. APIキーを設定
export OPENAI_API_KEY="sk-..."

# 3. 実行
python generate_21_slides.py
```

→ `./slides_output/` に21枚のPNGが生成されます。約3〜10分。

### B. Google Colab で実行

1. https://colab.research.google.com にアクセス
2. 新規ノートブック作成
3. `21_prompts_data.json` を左サイドバー📁にアップロード
4. 以下をセルに貼って実行：

```python
!pip install openai
import os
os.environ["OPENAI_API_KEY"] = "sk-..."  # ← APIキーを貼る

!wget -O generate_21_slides.py https://raw.githubusercontent.com/lazy3128-design/my-website/claude/simplify-counter-argument-PvXnb/VSL/codex_slide_instructions/generate_21_slides.py
!python generate_21_slides.py
```

→ `slides_output` フォルダにPNGが生成されます。左サイドバーからDLしてください。

### C. ChatGPT Pro の Advanced Data Analysis で実行

1. https://chatgpt.com で新規チャット
2. モデル：GPT-5 Thinking
3. 📎で `generate_21_slides.py` と `21_prompts_data.json` をアップロード
4. メッセージ：

```
添付した generate_21_slides.py を実行して、21_prompts_data.json から
全21枚のスライド画像を生成してください。

OpenAI API使用、出力は /tmp/slides_output/ ディレクトリ。
全部完了したら、各PNGファイルへのリンクをまとめて出してください。

APIキー: sk-...（実際のキーを入れる）
```

→ ChatGPTが自動実行→21枚生成→ダウンロードリンクを返してくれます。

---

## コスト目安

GPT-image-1 の料金（2026年5月時点）：

| 品質 | サイズ | 1枚あたり | 21枚合計 |
|---|---|---|---|
| low | 1024×1024 | 約$0.011 | 約$0.23 |
| medium | 1536×1024 | 約$0.042 | 約$0.88 |
| **high（推奨）** | **1536×1024** | **約$0.080** | **約$1.68** |

スクリプトのデフォルトは **high** です。低コストにしたければ `QUALITY = "medium"` に書き換え。

---

## カスタマイズ

`generate_21_slides.py` の上部設定で変更可能：

```python
SIZE = "1536x1024"   # "1024x1024" / "1536x1024" / "1024x1536" から選択
QUALITY = "high"     # "low" / "medium" / "high"
OUTPUT_DIR = "./slides_output"  # 出力先
```

注：GPT-image-1 は 1920×1080 を直接サポートしません。`1536x1024` が最も16:9に近いサイズです。
1920×1080にしたい場合は、生成後に PIL でリサイズしてください。

---

## 生成結果のチェックポイント

21枚生成後、以下を確認：

- [ ] 全21枚が出力されているか（失敗0件）
- [ ] UTAGE色（青#58A3E6 / 紫#A75FF5）が使われているか
- [ ] 日本語テキストが崩れていないか
- [ ] 右上25%エリアが空白か（顔ワイプ用）
- [ ] 下11%エリアが空白か（字幕用）
- [ ] 大賀の煽り赤（#FF3D2F）が混入していないか
- [ ] 中央寄せ構図か

NGがあれば、`21_prompts_data.json` の該当slideのpromptを調整→該当だけ単独生成。

---

## トラブルシューティング

### Q1：「OPENAI_API_KEY が設定されていません」
→ APIキーを環境変数にセット or スクリプト14行目に直書き

### Q2：「Rate limit exceeded」
→ 連続リクエスト過多。スクリプトに `time.sleep(2)` を各ループに挿入

### Q3：日本語テキストが崩れる
→ プロンプトを短く分割／「Spell exactly: 雑務ゼロ」など追記

### Q4：色がUTAGE色じゃない
→ プロンプト末尾に「Use ONLY these colors: #58A3E6, #A75FF5」を強調追加

### Q5：構図がバラつく
→ 各プロンプトに「centered composition, no asymmetry」を統一追加

---

## Stage 2（残り199枚）への流れ

21枚サンプルOKが出たら：

1. 通し版 `UTAGE_VSL_通しチェック版_v2_220枚版.md` を読み込ませる
2. 残り199スライド分のプロンプトデータを `220_prompts_data.json` として自動展開
3. 同じスクリプトのJSON参照先を切り替えて再実行
4. 約3〜5時間で全220枚完成（コスト ≈ $18）

ここまで来てから通し版を使います。
