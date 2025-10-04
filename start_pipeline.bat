@echo off
REM Script para iniciar o pipeline CDC
REM Navega para o diretório do projeto
cd /d "C:\Users\tiago\Documentos\GitHub\cdc-kaggle"

REM Ativa o ambiente Python (se necessário)
REM call venv\Scripts\activate

REM Executa o pipeline
python main.py

REM Pausa para ver mensagens de erro (opcional)
pause
