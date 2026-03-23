@echo off
title Sistem Pakar Penyakit Liver
echo.
echo  ==============================
echo   Sistem Pakar Penyakit Liver
echo  ==============================
echo.
echo  Menjalankan server...
echo  Buka browser: http://localhost:5000
echo.
echo  Tekan CTRL+C untuk menutup server
echo  ==============================
echo.
start "" "http://localhost:5000"
.\venv\Scripts\python.exe app.py
pause
