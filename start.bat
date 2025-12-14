@echo off
echo ====================================
echo  Flask Ping Monitor 起動中...
echo ====================================
echo.

cd /d %~dp0

REM 仮想環境の確認
if not exist venv (
    echo [エラー] 仮想環境が見つかりません
    echo python -m venv venv を実行してください
    pause
    exit /b 1
)

REM 仮想環境を有効化
call venv\Scripts\activate.bat

REM Flaskアプリ起動
echo [INFO] Flask Ping Monitor を起動しています...
echo [INFO] ブラウザで http://localhost:5000 を開いてください
echo.
python app.py

pause