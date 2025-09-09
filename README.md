# 🎯 TRIVIA QUIZ - EUREKA DO PADRE
## Sistema de Gincana do Conhecimento - EXECUÇÃO OFFLINE

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)
![Offline](https://img.shields.io/badge/Status-Offline%20Ready-success?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey?style=flat-square)

Sistema interativo de quiz educacional com **funcionamento 100% offline** para gincanas escolares.

---

## 🎮 **FUNCIONALIDADES**

- ✅ **Funcionamento 100% Offline** - Não requer internet
- 🎯 **Roleta Interativa** - Sorteia disciplinas com animação
- 🏆 **Sistema Multi-Turmas** - 6º, 7º e 8º ano
- 📚 **7 Disciplinas** - Português, Matemática, História, Geografia, Ciências, Inglês, Ed. Física  
- 🎨 **Interface Moderna** - Design responsivo e intuitivo
- 📊 **Placar em Tempo Real** - Sistema de pontuação automático
- 🎨 **Equipes Personalizáveis** - Até 12 equipes com cores diferentes
- 💾 **Banco de Dados Local** - SQLite integrado

---

## 📁 **ESTRUTURA DO PROJETO**

```
Trivia_Quizz/
├── 🐍 app.py                    # Servidor Flask principal
├── 🗃️ models.py                 # Modelos do banco de dados
├── 📋 requirements.txt          # Dependências Python
├── 🚀 start.sh                  # Script de inicialização (Linux)
├── 🖥️ trivia-quiz.desktop      # Ícone para desktop (Linux)
├── 📊 data/
│   ├── perguntas_6_ano.json    # Perguntas 6º ano
│   ├── perguntas_7_ano.json    # Perguntas 7º ano
│   └── perguntas_8_ano.json    # Perguntas 8º ano
├── 🎨 static/
│   ├── css/
│   │   ├── style.css           # Estilos principais
│   │   ├── roleta.css          # Estilos da roleta
│   │   ├── pergunta.css        # Estilos das perguntas
│   │   └── relatorio.css       # Estilos do relatório
│   ├── js/
│   │   └── scripts.js          # Lógica JavaScript
│   └── img/
│       └── Eureka.jpeg         # Logo do projeto
├── 🖼️ templates/
│   ├── index.html              # Página de configuração
│   ├── roleta.html             # Página da roleta/jogo
│   ├── pergunta.html           # Página das perguntas
│   └── relatorio.html          # Relatório final
└── 💽 instance/
    └── trivia_quizz.db         # Banco de dados SQLite
```

---

## 🖥️ **INSTALAÇÃO WINDOWS**

### **1️⃣ Pré-requisitos**
```powershell
# Verificar se Python está instalado
python --version
# Deve mostrar Python 3.7+ 

# Se não tiver Python, baixe em: https://python.org
```

### **2️⃣ Download do Projeto**
```powershell
# Opção A: Via Git
git clone https://github.com/GianKretzl/Trivia_Quizz.git
cd Trivia_Quizz

# Opção B: Download ZIP e extrair para pasta desejada
```

### **3️⃣ Configuração do Ambiente**
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências
pip install flask flask-sqlalchemy
```

### **4️⃣ Executar o Sistema**
```powershell
# Certificar que está no ambiente virtual (deve aparecer (.venv))
python app.py
```

### **5️⃣ Acessar o Jogo**
```
🌐 Abra o navegador: http://localhost:5000
```

---

## 🐧 **INSTALAÇÃO LINUX MINT / UBUNTU**

### **1️⃣ Instalação de Dependências**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e ferramentas
sudo apt install python3 python3-pip python3-venv git -y
```

### **2️⃣ Download e Configuração**
```bash
# Baixar projeto
cd ~/Documents
git clone https://github.com/GianKretzl/Trivia_Quizz.git
cd Trivia_Quizz

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install flask flask-sqlalchemy
```

### **3️⃣ Tornar Script Executável**
```bash
# Dar permissão ao script
chmod +x start.sh

# Executar com o script
./start.sh
```

### **4️⃣ Criar Ícone na Área de Trabalho (Opcional)**
```bash
# Copiar arquivo .desktop para área de trabalho
cp trivia-quiz.desktop ~/Desktop/

# Dar permissão de execução
chmod +x ~/Desktop/trivia-quiz.desktop
```

---

## 🍎 **INSTALAÇÃO macOS**

### **1️⃣ Instalar Homebrew (se necessário)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### **2️⃣ Instalar Python**
```bash
brew install python3
```

### **3️⃣ Configurar Projeto**
```bash
# Baixar e configurar
cd ~/Documents
git clone https://github.com/GianKretzl/Trivia_Quizz.git
cd Trivia_Quizz

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install flask flask-sqlalchemy

# Executar
python3 app.py
```

---

## 🎯 **COMO USAR O SISTEMA**

### **🔧 Configuração Inicial**
1. **Selecionar Turma**: Escolha entre 6º, 7º ou 8º ano
2. **Definir Equipes**: Escolha o número de equipes (2-12)
3. **Selecionar Cores**: Atribua cores únicas para cada equipe
4. **Iniciar Jogo**: Clique em "BORA COMEÇAR!"

### **🎮 Durante o Jogo**
1. **Girar Roleta**: Clique para sortear uma disciplina
2. **Ler Pergunta**: Pergunta aparece automaticamente
3. **Marcar Respostas**: Marque quais equipes acertaram
4. **Acompanhar Placar**: Pontuação atualizada automaticamente
5. **Gerar Relatório**: Acesse relatório completo das rodadas

### **📊 Disciplinas por Turma**

| **Disciplina** | **6º Ano** | **7º Ano** | **8º Ano** |
|---|---|---|---|
| 📖 **Português** | ✅ 6 questões | ✅ 10 questões | ✅ 10 questões |
| 🔢 **Matemática** | ✅ 8 questões | ✅ 10 questões | ✅ 21 questões |
| 🏛️ **História** | ✅ 7 questões | ✅ 10 questões | ✅ 19 questões |
| 🌍 **Geografia** | ✅ 8 questões | ✅ 10 questões | ✅ 15 questões |
| 🔬 **Ciências** | ✅ 8 questões | - | ✅ 10 questões |
| 🇺🇸 **Língua Inglesa** | ✅ 3 questões | ✅ 3 questões | ✅ 2 questões |
| ⚽ **Educação Física** | ✅ 2 questões | ✅ 2 questões | ✅ 2 questões |

---

## 🌐 **ACESSO EM REDE LOCAL**

Para permitir acesso de outros dispositivos na mesma rede:

### **Modificar app.py:**
```python
# Alterar linha final de:
app.run(debug=True)

# Para:
app.run(host='0.0.0.0', port=5000, debug=True)
```

### **Descobrir IP da máquina:**
```bash
# Windows
ipconfig

# Linux/Mac  
ip addr show
```

### **Acessar de outros dispositivos:**
```
http://IP_DA_MAQUINA:5000
```

---

## 🔧 **PERSONALIZAÇÃO**

### **➕ Adicionar Novas Perguntas**
Edite os arquivos em `data/perguntas_X_ano.json`:

```json
{
  "pergunta": "Sua pergunta aqui?",
  "opcoes": [
    "Opção A",
    "Opção B", 
    "Opção C",
    "Opção D"
  ],
  "resposta_correta": 2
}
```

### **🎨 Modificar Cores das Equipes**
No arquivo `static/js/scripts.js`, seção `CORES_EQUIPES`:

```javascript
const CORES_EQUIPES = [
    {'nome': 'NOVA_COR', 'hex': '#FF5733'},
    // Adicione mais cores...
];
```

---

## 🚨 **SOLUÇÃO DE PROBLEMAS**

### **❌ "Módulo não encontrado"**
```bash
# Certificar que está no ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Reinstalar dependências
pip install flask flask-sqlalchemy
```

### **❌ "Porta 5000 em uso"**
```bash
# Modificar porta no app.py:
app.run(port=8080, debug=True)
```

### **❌ "Banco de dados não encontrado"**
```bash
# Deletar arquivo de banco e reiniciar
rm instance/trivia_quizz.db
python app.py
```

---

## 📱 **RECURSOS TÉCNICOS**

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (local)
- **Interface**: Bootstrap + CSS customizado
- **Compatibilidade**: Todos navegadores modernos
- **Responsivo**: Desktop, tablet e mobile

---

## 🤝 **SUPORTE E CONTRIBUIÇÕES**

### **🐛 Reportar Problemas**
Abra uma issue no GitHub com:
- Sistema operacional
- Versão do Python
- Mensagem de erro completa
- Passos para reproduzir

### **💡 Sugestões de Melhoria**
- Novas funcionalidades
- Melhorias na interface
- Correções de bugs
- Otimizações de performance

---

## 📄 **LICENÇA**

Este projeto está sob licença MIT. Uso livre para fins educacionais.

---

## 🎉 **CRÉDITOS**

**Desenvolvido para o Colégio Padre Antonio Vieira**
- 1º EUREKA DO PADRE - Gincana do Conhecimento
- Sistema 100% offline para uso educacional

---

**🎯 Pronto para a Gincana! Que vença a melhor equipe! 🏆**

## 🎮 Como Jogar

1. **Sorteio**: Clique no botão "GIRAR ROLETA" para sortear uma disciplina
2. **Pergunta**: Uma pergunta da disciplina sorteada será exibida
3. **Resposta**: Clique na opção de resposta desejada
4. **Equipe**: Selecione qual equipe está respondendo
5. **Resultado**: O sistema mostra se acertou e atualiza o placar
6. **Nova Rodada**: Use o botão "Nova Rodada" para continuar

## 🎯 Disciplinas Disponíveis

- **História**: Eventos históricos e personalidades
- **Geografia**: Países, capitais, rios e montanhas
- **Ciências**: Química, física, biologia e astronomia
- **Literatura**: Autores e obras clássicas
- **Matemática**: Cálculos básicos e conceitos
- **Artes**: Pinturas, esculturas e música clássica

## ⚙️ Controles do Apresentador

- **Nova Rodada**: Limpa a tela e prepara para nova pergunta
- **Mostrar Resposta**: Revela a resposta correta
- **Resetar Placar**: Zera a pontuação de todas as equipes
- **Teclas de Atalho**:
  - `Espaço`: Gira a roleta
  - `Ctrl + R`: Nova rodada

## 🔧 Personalização

### Adicionar Novas Perguntas
Edite o arquivo `data/perguntas.json` seguindo o formato:

```json
{
  "Nova Disciplina": [
    {
      "id": 1,
      "pergunta": "Sua pergunta aqui?",
      "opcoes": ["Opção A", "Opção B", "Opção C", "Opção D"],
      "resposta_correta": "Opção Correta"
    }
  ]
}
```

### Modificar Equipes
No arquivo `app.py`, altere a variável `placar` para adicionar/remover equipes:

```python
placar = {
    "Equipe 1": 0,
    "Equipe 2": 0,
    # Adicione mais equipes conforme necessário
}
```

### Personalizar Visual
Modifique o arquivo `static/css/style.css` para alterar cores, fontes e layout.

## 🌐 Deploy

Para usar em produção, considere:

1. **Gunicorn** (Linux/Mac):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Waitress** (Windows):
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📱 Recursos Extras

- **Interface Responsiva**: Funciona bem em tablets e smartphones
- **Animações Suaves**: Transições e efeitos visuais
- **Loading Indicators**: Feedback visual durante operações
- **Design Moderno**: Gradientes e sombras para visual profissional

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎉 Créditos

Desenvolvido para facilitar gincanas culturais e eventos educativos.

---

**Divirta-se com sua Gincana Cultural! 🎯📚**
