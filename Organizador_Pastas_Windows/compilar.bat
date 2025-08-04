@echo off
cd /d "C:\Users\romul\Desktop\Python\Programas_Úteis"
pyinstaller --onefile --windowed organizador.py
pause
rmdir /s /q build
del organizador.spec
echo Limpeza concluída!
pause
