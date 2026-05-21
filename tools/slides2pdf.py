#!/usr/bin/env python3
"""mp4動画からスライド切り替えを検出し、1枚のPDFにまとめる。

使い方:
    python3 slides2pdf.py 入力.mp4
    python3 slides2pdf.py 入力.mp4 -o 出力.pdf
    python3 slides2pdf.py 入力.mp4 --start 00:05:00 --duration 60   # 5分地点から60秒だけ
    python3 slides2pdf.py 入力.mp4 --scan                            # 閾値の下見だけ

依存: ffmpeg / ffprobe (PATH上), Python: img2pdf, Pillow, ImageHash

スライド動画はシーン変化スコアが小さい(背景が変わらないため)。
うまく検出されない場合は --scan でスコアを確認し --threshold を調整する。
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import img2pdf
import imagehash
from PIL import Image

HASH_SIZE = 16  # phashのビット数(16 -> 256bit)。テキストスライドの識別精度が高い


def check_tools():
    missing = [t for t in ("ffmpeg", "ffprobe") if shutil.which(t) is None]
    if missing:
        sys.exit(f"エラー: {', '.join(missing)} が見つかりません。ffmpegをインストールしてください。")


def probe_duration(video: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        capture_output=True, text=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def trim_args(start, duration):
    """--start / --duration を ffmpeg の入力前オプションに変換する。"""
    args = []
    if start:
        args += ["-ss", str(start)]
    if duration:
        args += ["-t", str(duration)]
    return args


def scan_scores(video: Path, start, duration):
    """シーンスコアの分布を表示する(検出されないときの閾値の目安)。"""
    meta = Path(tempfile.mktemp(suffix=".txt"))
    cmd = ["ffmpeg", "-v", "error"] + trim_args(start, duration) + [
        "-i", str(video),
        "-vf", f"select='gt(scene,0)',metadata=print:file={meta}",
        "-vsync", "vfr", "-f", "null", "-"]
    print("スコアをスキャン中... (動画全体をデコードします)")
    subprocess.run(cmd, check=True)
    scores = []
    if meta.exists():
        for line in meta.read_text().splitlines():
            m = re.search(r"scene_score=([0-9.]+)", line)
            if m:
                scores.append(float(m.group(1)))
        meta.unlink()
    scores.sort(reverse=True)
    print(f"全フレーム数: {len(scores)}")
    print("上位スコア:", ", ".join(f"{s:.4f}" for s in scores[:15]) or "なし")
    for th in (0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02, 0.01):
        print(f"  threshold {th:<5}: {sum(1 for s in scores if s > th)}フレーム検出")


def extract_first_frame(video: Path, dest: Path, start):
    """先頭スライドはシーン変化を起こさないので明示的に取得する。"""
    cmd = ["ffmpeg", "-v", "error", "-y"] + trim_args(start, None) + [
        "-i", str(video), "-frames:v", "1", str(dest)]
    subprocess.run(cmd, check=True)


def detect_scene_frames(video: Path, frames_dir: Path, threshold, start, duration):
    """シーン検出フレームをPNG書き出しし、各フレームのタイムスタンプを返す。"""
    meta = frames_dir / "scenes.txt"
    vf = f"select='gt(scene,{threshold})',metadata=print:file={meta}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + trim_args(start, duration) + [
        "-i", str(video), "-vf", vf, "-vsync", "vfr",
        str(frames_dir / "scene_%06d.png")]
    subprocess.run(cmd, check=True)
    times = []
    if meta.exists():
        for line in meta.read_text().splitlines():
            m = re.search(r"pts_time:([0-9.]+)", line)
            if m:
                times.append(float(m.group(1)))
    return times


def main():
    p = argparse.ArgumentParser(description="mp4のスライド切り替えを1枚のPDFにまとめる")
    p.add_argument("input", help="入力mp4ファイル")
    p.add_argument("-o", "--output", help="出力PDF (既定: <入力名>_slides.pdf)")
    p.add_argument("--threshold", type=float, default=0.03,
                   help="シーン検出の閾値 0-1。小さいほど敏感 (既定: 0.03)")
    p.add_argument("--min-interval", type=float, default=2.0,
                   help="採用フレーム間の最小秒数。連続誤検出を抑制 (既定: 2.0)")
    p.add_argument("--hash-threshold", type=int, default=12,
                   help="重複排除のハッシュ距離。小さいほど厳密に区別 (既定: 12)")
    p.add_argument("--start", help="処理開始位置 秒 または HH:MM:SS")
    p.add_argument("--duration", help="処理する長さ 秒 または HH:MM:SS (テスト用)")
    p.add_argument("--max-slides", type=int, default=5000,
                   help="安全弁。候補がこれを超えたら中止 (既定: 5000)")
    p.add_argument("--keep-frames", action="store_true", help="抽出したPNGを残す")
    p.add_argument("--scan", action="store_true",
                   help="検出せずシーンスコアの分布だけ表示する")
    args = p.parse_args()

    check_tools()
    video = Path(args.input).expanduser()
    if not video.is_file():
        sys.exit(f"エラー: ファイルが見つかりません: {video}")

    duration = probe_duration(video)
    print(f"入力: {video}  長さ: {duration:.0f}秒")

    if args.scan:
        scan_scores(video, args.start, args.duration)
        return

    output = Path(args.output) if args.output else video.with_name(video.stem + "_slides.pdf")
    work = Path(tempfile.mkdtemp(prefix="slides2pdf_"))
    frames_dir = work / "frames"
    frames_dir.mkdir(parents=True)

    try:
        print("先頭フレームを取得中...")
        first = frames_dir / "scene_000000.png"
        extract_first_frame(video, first, args.start)

        print("シーン検出中... (動画長によっては数分かかります)")
        scene_times = detect_scene_frames(
            video, frames_dir, args.threshold, args.start, args.duration)
        print(f"  検出: {len(scene_times)}フレーム")

        if not scene_times:
            print("\nシーン変化が検出されませんでした。")
            print("--threshold を下げるか、--scan でスコア分布を確認してください。")

        # 先頭フレーム(t=0) + 検出フレームを時刻順に並べる
        candidates = [(0.0, first)]
        for i, t in enumerate(scene_times, start=1):
            png = frames_dir / f"scene_{i:06d}.png"
            if png.exists():
                candidates.append((t, png))

        if len(candidates) > args.max_slides:
            sys.exit(
                f"エラー: 候補が{len(candidates)}枚で上限({args.max_slides})を超えました。"
                f"--threshold を上げるか --max-slides を調整してください。")

        # 最小間隔フィルタ(遷移中の連続発火を除去)
        spaced = []
        last_t = -1e9
        for t, png in candidates:
            if t - last_t >= args.min_interval:
                spaced.append((t, png))
                last_t = t
        print(f"  最小間隔フィルタ後: {len(spaced)}枚")

        # 連続するほぼ同一スライドを重複排除
        selected = []
        prev_hash = None
        for t, png in spaced:
            try:
                h = imagehash.phash(Image.open(png), hash_size=HASH_SIZE)
            except Exception:
                continue
            if prev_hash is not None and (h - prev_hash) <= args.hash_threshold:
                continue
            selected.append(png)
            prev_hash = h
        print(f"  重複排除後: {len(selected)}枚")

        if not selected:
            sys.exit("エラー: スライドを1枚も抽出できませんでした。")

        print(f"PDF生成中... -> {output}")
        with open(output, "wb") as f:
            f.write(img2pdf.convert([str(s) for s in selected]))
        print(f"完了: {output}  ({len(selected)}ページ)")

        if args.keep_frames:
            keep = output.with_name(output.stem + "_frames")
            if keep.exists():
                shutil.rmtree(keep)
            shutil.copytree(frames_dir, keep)
            print(f"PNGを保存: {keep}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
