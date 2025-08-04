@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Instalando dependências do projeto...
pip install reportlab

echo Gerando arquivo requirements.txt...
pip freeze > requirements.txt

echo.
echo ✅ Tudo pronto! Ambiente criado e dependências instaladas.
pause
