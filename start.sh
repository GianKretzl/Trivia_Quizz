#!/bin/bash
# Script para iniciar o Trivia Quiz no Linux Mint

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 INICIANDO TRIVIA QUIZ - EUREKA DO PADRE${NC}"
echo -e "${YELLOW}================================================${NC}"

# Verificar se está na pasta correta
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Erro: app.py não encontrado. Execute este script na pasta do projeto.${NC}"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado. Criando...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-sqlalchemy
else
    echo -e "${GREEN}✅ Ativando ambiente virtual...${NC}"
    source venv/bin/activate
fi

# Verificar dependências
echo -e "${BLUE}🔍 Verificando dependências...${NC}"
python3 -c "import flask, flask_sqlalchemy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Instalando dependências...${NC}"
    pip install flask flask-sqlalchemy
fi

# Limpar terminal
clear

echo -e "${GREEN}🚀 INICIANDO SERVIDOR...${NC}"
echo -e "${BLUE}📱 Acesse: http://localhost:5000${NC}"
echo -e "${YELLOW}⏹️  Para parar: Ctrl+C${NC}"
echo -e "${YELLOW}================================================${NC}"

# Iniciar aplicação
python3 app.py
