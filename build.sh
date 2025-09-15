#!/bin/bash

# Script de build para o Render
echo "🚀 Iniciando build para Render..."

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Criar diretório para banco de dados se necessário
echo "🗄️  Preparando banco de dados..."
python -c "
import os
from app import app, db
import traceback

try:
    with app.app_context():
        print('Criando tabelas do banco de dados...')
        db.create_all()
        print('✅ Banco de dados configurado com sucesso!')
except Exception as e:
    print(f'❌ Erro ao configurar banco: {e}')
    print(traceback.format_exc())
    exit(1)
"

echo "✅ Build concluído com sucesso!"