@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

if "%~1"=="" (
  echo.
  echo   このファイルに mp4 動画をドラッグ ^& ドロップしてください。
  echo   複数まとめてドロップもできます。
  echo.
  pause
  exit /b
)

REM --- Python があるか確認 ---
where python >nul 2>nul
if errorlevel 1 (
  echo [エラー] Python が見つかりません。
  echo https://www.python.org/downloads/ からインストールしてください。
  echo インストール画面で "Add Python to PATH" に必ずチェックを入れてください。
  echo.
  pause
  exit /b
)

REM --- ffmpeg があるか確認。なければ winget で導入 ---
where ffmpeg >nul 2>nul
if errorlevel 1 (
  echo [情報] ffmpeg が見つかりません。winget でインストールを試みます...
  winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
  echo.
  echo ffmpeg を入れました。いったんこの画面を閉じ、もう一度ドロップしてください。
  echo （PATH の反映に再起動が必要なためです）
  echo.
  pause
  exit /b
)

REM --- Python の必要パッケージを確認 ---
python -c "import img2pdf, imagehash, PIL" >nul 2>nul
if errorlevel 1 (
  echo [情報] 必要なパッケージをインストール中です。少しお待ちください...
  python -m pip install --quiet img2pdf Pillow ImageHash
)

REM --- ドロップされたファイルを順に処理 ---
:loop
if "%~1"=="" goto done
echo ============================================
echo 処理中: %~1
echo ============================================
python "%~dp0slides2pdf.py" "%~1"
echo.
shift
goto loop

:done
echo すべて完了しました。PDF は元の動画と同じフォルダにできています。
echo.
pause
