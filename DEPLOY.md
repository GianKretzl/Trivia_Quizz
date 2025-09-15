# 🚀 DEPLOY NO RENDER - GUIA SIMPLIFICADO

## ✅ Pré-requisitos
- Conta no GitHub
- Conta no Render (render.com)
- Repositório no GitHub

## 📝 PASSOS PARA DEPLOY:

### 1. **Commit e Push**
```bash
git add .
git commit -m "Deploy para Render"
git push origin main
```

### 2. **Configurar no Render**
1. Acesse: https://render.com
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Conecte o repositório: `Trivia_Quizz`

### 3. **Configurações**
- **Name**: `trivia-quiz`
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: `Free`

### 4. **Variáveis de Ambiente**
Adicione estas variáveis na seção "Environment Variables":
- `PYTHON_VERSION`: `3.11.0`
- `RENDER`: `true`

### 5. **Deploy**
1. Clique "Create Web Service"
2. Aguarde o build (alguns minutos)
3. Acesse sua aplicação na URL fornecida

## 🔧 ARQUIVOS PREPARADOS:
- ✅ `requirements.txt` - Dependências
- ✅ `Procfile` - Comando de inicialização
- ✅ `app.py` - Configurado para produção
- ✅ `.gitignore` - Arquivos ignorados

## 🎯 IMPORTANTE:
- O banco SQLite será criado automaticamente
- As questões serão importadas na primeira execução
- URL final: `https://trivia-quiz-xxx.onrender.com`

## 🛠️ Se der erro:
1. Verifique os logs no dashboard do Render
2. Certifique-se que todos os arquivos foram commitados
3. Aguarde alguns minutos (primeira execução é mais lenta)

---
**Status**: ✅ Pronto para deploy!