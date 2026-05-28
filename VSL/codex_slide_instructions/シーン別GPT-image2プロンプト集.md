# UTAGE VSL シーン別 GPT-image-2 プロンプト集

**バージョン**：v1.0
**作成日**：2026-05-28
**対象**：GPT-image-2（または同等の画像生成AI）でUTAGE VSLのシーン別代表サンプル**21枚**を生成する用
**目的**：本番220枚展開前の品質検証。1シーン1枚で全パターンの世界観を確認

---

## 0. 全枚共通のスタイル原則（必読）

**全てのプロンプトに以下の基本要素を含める：**

```
1920x1080 cinematic VSL slide.
Centered composition.
Color palette: UTAGE brand colors – primary blue #58A3E6 and primary purple #A75FF5.
Modern Japanese SaaS aesthetic, Apple Keynote-level polish, premium feel.
Bold Japanese typography with one accent word in UTAGE blue or purple gradient.
Reserve top-right 480×270px area for face wipe overlay (leave clean).
Reserve bottom 120px area for subtitle overlay (leave clean).
NO clutter, generous whitespace, sophisticated.
```

**Japanese textをそのままプロンプト内に書いてOK**。GPT-image-2は日本語対応しています（ただし長文より短いフレーズが綺麗に出る）。

---

## シーン01 - タイトル提示（パターン①）

**狙い**：何の動画かを即座に伝達＋実績バナーで権威付け

```
1920x1080 cinematic VSL title slide.
Diagonal gradient background: lower-left UTAGE blue #58A3E6 to upper-right UTAGE purple #A75FF5.
Centered composition.
Top center: small ribbon banner with text "わずか14日間で雑務ゼロを実現する".
Center: huge bold Japanese title "UTAGE" in white, 240pt.
Below title: smaller text "オールインワン・マーケティングシステム" in soft white.
Subtle geometric dots pattern in background, opacity 8%.
Subtle film grain texture.
Reserve top-right 480×270 for face wipe.
Modern Japanese SaaS premium aesthetic.
```

---

## シーン03 - 期待値設定・約束（パターン①）

**狙い**：学習の見通しを示す／3つの約束で期待値設定

```
1920x1080 cinematic VSL slide, declaration style.
Diagonal gradient background: lower-left #58A3E6 to upper-right #A75FF5.
Centered composition with three vertical pillars or numbered cards.
Top text: "動画を見終える頃 / あなたが手にしているのは / 3つのこと" in white 56pt.
Three minimalist icon cards centered below with numbers 1, 2, 3.
Each card: subtle white outline with rounded corners 24px, transparent fill.
Bold accent typography in white.
Sophisticated, premium, Apple Keynote-style.
Reserve top-right 480×270 for face wipe.
Reserve bottom 120 for subtitle.
```

---

## シーン04 - 理想未来の提示（パターン④）

**狙い**：『もし〜だったら？』で未来を植える

```
1920x1080 cinematic VSL slide, sentimental future vision.
Background: abstract early morning sky, soft gradient from dawn blue #58A3E6 to lavender purple #A75FF5.
Slight cloud whisps, dreamy bokeh light particles.
Semi-transparent navy overlay rgba(30,42,82,0.45) for text legibility.
Centered text in white 60pt bold:
"集客は伸びている
受講生やクライアントからの問い合わせも止まらず入ってくる
お客様からは『ありがとうございました』と
心のこもった声をいただけている"
Soft elegant aesthetic, hopeful, premium.
Reserve top-right 480×270 for face wipe.
Reserve bottom 120 for subtitle.
```

---

## シーン05 - 痛みの言語化（パターン②）

**狙い**：典型痛みを連発し『自分の話だ』と感じさせる

```
1920x1080 cinematic VSL slide, emotional pain expression.
Background: deep UTAGE purple #6C3D9F full bleed with subtle smoky purple texture.
Small thin vertical accent bar in soft coral #C56B5A on left edge, 8px wide, 240px tall.
Centered text in white, bold Japanese typography:
"それなのに——
なぜかしんどい"
The word "しんどい" enlarged 1.5x and in soft lavender #D3AFFA.
Below in smaller white 40pt:
"朝目が覚めた瞬間から / 今日のタスクの山が頭に押し寄せる"
Heavy atmosphere, premium, NOT aggressive red (replace traditional red with deep purple).
Reserve top-right 480×270 for face wipe.
```

---

## シーン06 - 一網打尽の宣言（パターン②）

**狙い**：痛みを束ねて解決策の予告

```
1920x1080 cinematic VSL slide, powerful declaration on dark.
Background: deep UTAGE purple #6C3D9F with subtle gradient toward darker #4A2880 at edges.
Centered huge Japanese typography in white 100pt bold:
"こうした課題のすべては
たった一つの選択で解決します"
Small underline accent in soft lavender below text.
Single thin gradient line from #58A3E6 to #A75FF5 underneath the text.
Premium, declarative, sophisticated.
Reserve top-right 480×270 for face wipe.
```

---

## シーン07 - 責任解除（パターン③）

**狙い**：外的要因で自責を解除

```
1920x1080 cinematic VSL slide, structured list on white.
Background: off-white #FAFAF7 with very subtle lavender tint on edges.
Top: thin vertical purple bar #A75FF5 6px wide + section label "| あなたのせいではありません" in dark #1A1F36 28pt.
Center: large heading "ビジネス成長に悩むのは / あなたのせいではない" in #1A1F36 56pt bold.
Below: clean numbered list of 5 items with circle icons in UTAGE blue:
1. 部分最適化しかできない広告代理店や代行業者の乱立
2. たえまなくいっぱい立ち上がるSNS投稿や無料サンプル情報
3. 100年前のマーケティング理論や時代遅れのプロモーション戦略
Each item with thin separator line.
Bottom one-liner highlight in UTAGE blue.
Modern minimal, sophisticated, Notion-style.
Reserve top-right 480×270 for face wipe.
```

---

## シーン08 - 実績による証明（パターン③）

**狙い**：数字スタッツで権威付け

```
1920x1080 cinematic VSL slide, stats display on white.
Background: off-white #FAFAF7.
Top: thin purple vertical bar + "| UTAGEの利用実績" 28pt.
Centered two huge stat blocks side by side:
LEFT: "1.5万社" in UTAGE gradient text (blue-purple), 180pt bold + small label "累計事業者が導入" 28pt grey.
RIGHT: "100万人" in UTAGE gradient text, 180pt bold + small label "利用ユーザー" 28pt grey.
Below in smaller text 24pt center grey:
"コンサルタント・コーチ / 講座やスクール運営 / オンラインサロン・士業..."
Subtle decorative dots or thin gradient line above stats.
Premium SaaS company report aesthetic.
Reserve top-right 480×270 for face wipe.
```

---

## シーン10 - 解決策の宣言（パターン①）

**狙い**：『雑務ゼロ』を超大型強調

```
1920x1080 cinematic VSL slide, hero declaration.
Diagonal gradient background: lower-left #58A3E6 to upper-right #A75FF5.
Subtle geometric pattern overlay opacity 6%, soft film grain.
Centered composition:
TOP small text in soft white 36pt: "中途半端な「効率化」では届きません"
CENTER huge bold Japanese "雑務ゼロ" 240pt in pure white with subtle drop shadow.
BOTTOM smaller text: "これがすべての始まりです" 32pt soft white.
Premium, declarative, Apple Keynote hero slide aesthetic.
Reserve top-right 480×270 for face wipe.
Reserve bottom 120 for subtitle.
```

---

## シーン11 - 市場・消費者行動の変化（パターン③）

**狙い**：古いやり方が通用しないと教育

```
1920x1080 cinematic VSL slide, data visualization on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| 事業環境はここ数年で劇的に変わった" 28pt.
Centered: two side-by-side simple line charts in UTAGE blue/purple.
LEFT chart labeled "従来型: ジャーニー型消費" with classic step-up line shape.
RIGHT chart labeled "現代: パルス型消費" with spiky bursts.
Above charts: subtle source citation "出典：Think with Google".
Below: one-line summary in dark text "100年前のマーケティング理論はもう通用しない" 36pt.
Clean educational, data-driven aesthetic, McKinsey report style.
Reserve top-right 480×270 for face wipe.
```

---

## シーン12 - 集客方法の比較（パターン③）

**狙い**：競合解決策をマトリクスで自分の優位性可視化

```
1920x1080 cinematic VSL slide, 2x2 matrix comparison on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| 従来型オンライン集客方法のメリット・デメリット" 28pt.
Centered 2x2 matrix with axes labeled "工数/運営の楽さ" (vertical) and "売上" (horizontal).
Four quadrants with method labels:
- Top-Left: エバーグリーンローンチ
- Top-Right (highlighted with UTAGE blue tint): ハイチケットウェビナーファネル
- Bottom-Left: SNSマーケティング / 旧型DRM
- Bottom-Right: リアルタイムセミナー / ZOOMウェビナー
Clean grid, sophisticated typography, soft shadows on highlighted quadrant.
Educational consulting report aesthetic.
Reserve top-right 480×270 for face wipe.
```

---

## シーン13 - ファネル構造の図解（パターン③）

**狙い**：解決策の中身を視覚教育（口頭同期）

```
1920x1080 cinematic VSL slide, horizontal funnel flow diagram on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| UTAGEの売れる流れ" 28pt.
Centered left-to-right flow diagram with 5 stages connected by gradient arrows:
[オプトイン] → [教育] → [販売・決済] → [会員サイト] → [継続フォロー]
Each stage as a rounded card with icon and label.
Arrows use UTAGE blue-purple gradient.
Soft shadows on cards, subtle background tints.
Below: one-line summary "事業の売上を生む一連の流れがUTAGEひとつで動きます" 32pt.
Clean modern flow chart aesthetic.
Reserve top-right 480×270 for face wipe.
```

---

## シーン15 - 市況変化（競合・飽和）（パターン②）

**狙い**：競合脅威の警告

```
1920x1080 cinematic VSL slide, market threat emphasis on dark.
Background: deep UTAGE purple #6C3D9F with subtle dramatic gradient.
Centered text in white 88pt bold:
"市況変化①
競合プレイヤー強すぎ問題"
Below in 32pt soft lavender #D3AFFA:
"VCから数十億の資金調達済みプレイヤーが / オンライン教育市場に参入"
Subtle warning icon or accent in soft coral #C56B5A on top-left.
Heavy atmosphere, serious tone, NOT aggressive red.
Reserve top-right 480×270 for face wipe.
```

---

## シーン16 - 時間 vs 金銭（パターン①）

**狙い**：時間の希少性で解決策の必要性を後押し

```
1920x1080 cinematic VSL slide, value proposition hero.
Diagonal gradient background: lower-left #58A3E6 to upper-right #A75FF5.
Centered single huge typography in pure white:
"お金 < 時間"
With "<" symbol enlarged and "時間" emphasized at 280pt.
Below in smaller text 32pt soft white:
"時間こそが、最大の資産です"
Minimalist, single message, Apple Keynote single-statement style.
Premium declarative.
Reserve top-right 480×270 for face wipe.
```

---

## シーン17 - 集客コスト高騰（パターン③）

**狙い**：数字で具体性、危機感を最大化

```
1920x1080 cinematic VSL slide, cost analysis on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| 集客コストの現実" 28pt.
Centered three side-by-side columns with icons and key numbers:
LEFT: SNS広告 icon (Facebook/Instagram/Youtube logos) + "リスト単価 ¥3,500〜¥8,000" 48pt amber gold #D4A04C
CENTER: セミナー icon (people in room) + "着席率50% / 着席単価 ¥90,000" 48pt amber gold
RIGHT: 個別面談 icon (two people) + "顧客獲得単価 ¥180,000〜¥300,000" 48pt amber gold
Below: small warning "集客コストはここ数年でどんどん上がっている" 32pt grey.
Clean data presentation, financial report style.
Reserve top-right 480×270 for face wipe.
```

---

## シーン20 - セールスファネルの困難（パターン②）

**狙い**：『自分でやろうとすると挫折』再痛み

```
1920x1080 cinematic VSL slide, frustration emphasis on dark.
Background: deep UTAGE purple #6C3D9F full bleed.
Centered text in white 96pt bold:
"セールスファネルは
つくるのが超たいへん..."
The word "超たいへん" emphasized at 110pt in soft coral #C56B5A.
Subtle scattered tool icons/UI fragments faded in background opacity 8%.
Heavy weight, exhausted atmosphere.
Reserve top-right 480×270 for face wipe.
```

---

## シーン21 - テンプレで解決の予告（パターン③）

**狙い**：プログラム解決策の提示

```
1920x1080 cinematic VSL slide, solution features on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| UTAGEなら、つくるものがほぼない" 28pt.
Centered three rounded card icons in a row with soft shadows:
LEFT: green check icon + "成果実証済み / 広告運用手法" 32pt
CENTER: gold trophy icon + "月商8桁実績 / ファネルテンプレ" 32pt
RIGHT: rocket icon + "個別相談獲得特化型 / ウェビナーテンプレ" 32pt
Below: tagline "テンプレを元にあなたのビジネスVerに書き換えるだけ" in gradient text 36pt.
Modern SaaS product feature card aesthetic.
Reserve top-right 480×270 for face wipe.
```

---

## シーン22 - 反論処理（広告経験）（パターン⑤）

**狙い**：視聴者の本音代弁

```
1920x1080 cinematic VSL slide, internal monologue on dark.
Background: deep navy #0F1419 with subtle nebula texture in purple/blue.
Aurora-like soft glow in upper area, very low opacity.
Centered text in white 72pt with quote marks:
"「でも、広告運用の経験もスキルもないし
設定も難しいと聞きますよ...」"
Quotation marks in soft purple #A75FF5, slightly larger.
Premium, contemplative, internal voice atmosphere.
Reserve top-right 480×270 for face wipe.
```

---

## シーン25 - まとめ・3つのコア再強調（パターン③）

**狙い**：UTAGE機能を再確認、購入前ブリーフ

```
1920x1080 cinematic VSL slide, feature summary on white.
Background: off-white #FAFAF7.
Top: thin purple bar + "| UTAGEを手にした先の毎日" 28pt.
Centered organized two-column checklist with UTAGE blue check icons:
LEFT column:
✓ ファネル構築・LP作成
✓ メール・LINE配信（一元化）
✓ 申込フォーム＋決済（同ページ完結）
✓ 会員サイト構築
RIGHT column:
✓ ステップ配信＋シナリオ分岐
✓ 自動ウェビナー
✓ 予約管理／アフィリエイト
✓ A/Bテスト分析
Bottom: "事業の運営に必要なもの、ほぼすべてがUTAGEひとつに" 36pt centered.
Clean SaaS feature summary aesthetic.
Reserve top-right 480×270 for face wipe.
```

---

## シーン26 - プログラム紹介・体制（パターン①）

**狙い**：価格・特典を提示

```
1920x1080 cinematic VSL slide, pricing reveal hero.
Diagonal gradient background: lower-left #58A3E6 to upper-right #A75FF5.
Centered composition:
TOP small label "UTAGE 月額料金" in soft white 32pt.
CENTER huge price "¥21,670 / 月" in pure white 200pt bold.
Below in soft white 32pt: "クレジットカードで14日間無料お試し可"
Subtle gold accent line below price.
Premium pricing reveal, Apple-style.
Reserve top-right 480×270 for face wipe.
```

---

## シーン27 - 3つの道の選択（パターン①＋④）

**狙い**：自己選択感／パートナーシップ宣言

```
1920x1080 cinematic VSL slide, partnership invitation.
Background: cinematic landscape – soft early morning sea horizon or open road, in UTAGE color tones (blue-purple atmospheric).
Semi-transparent navy overlay rgba(30,42,82,0.55) for text legibility.
Centered text in white 88pt bold:
"あなたには3つの道があります"
Below in 36pt soft white:
"このまま閉じる / 独学で進む / 私たちと一緒に進む"
The third option "私たちと一緒に進む" highlighted in gradient gold-purple.
Hopeful, contemplative, partnership atmosphere.
Reserve top-right 480×270 for face wipe.
```

---

## シーン28 - 最終CTA・希少性・謝辞（パターン①）

**狙い**：希少性で行動促進＋温かく締め

```
1920x1080 cinematic VSL slide, final call to action.
Diagonal gradient background: lower-left #58A3E6 to upper-right #A75FF5.
Centered composition:
TOP small text 32pt soft white: "今すぐ——"
CENTER main message in white 72pt bold:
"動画の下にあるボタンを押してください"
Below in soft white 40pt: "14日間完全無料で / UTAGEのすべての機能をお試しいただけます"
Subtle white border button shape suggested by typography.
Premium, sincere, warm closing atmosphere.
Reserve top-right 480×270 for face wipe.
Reserve bottom 120 for subtitle.
```

---

## 補足：除外シーン

| 元シーン | 内容 | 除外理由 |
|---|---|---|
| #19 受講者ビフォーアフター | 個別ケースカード（顔写真） | 顔写真UP→GPT-image-2で別途生成のため除外 |
| #29 新SFCメンバー | 内部実証3名（顔写真） | 同上 |

これら2シーンは後日、顔写真をアップロードしてGPT-image-2に直接渡して生成します。

---

## Codexへの依頼テンプレ

このファイルをCodexに渡すときの指示文：

```
タスク：UTAGE VSLシーン別サンプル21枚をGPT-image-2で生成

添付ファイル：
- シーン別GPT-image-2プロンプト集.md（このファイル）

【お願い】
1. 上記MDの21シーン分のプロンプトを順に GPT-image-2 API へ送信
2. 各レスポンスのPNGを /slides/scene_XX_<name>.png として保存
3. 21枚を3列×7行のサムネ一覧 /tmp/all_scenes_thumb.png にまとめて出力

【絶対ルール】
- 全枚 1920×1080 PNG
- 章0「全枚共通のスタイル原則」をすべてのプロンプト先頭に追加
- 顔ワイプエリア（右上480×270）と字幕エリア（下120px）は空白を維持

【出力】
- /slides/ ディレクトリに21枚
- サムネ一覧 PNG
- 各シーンの生成自己評価（特に難しかった箇所）
```
