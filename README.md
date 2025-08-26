# 🎯 Gincana Cultural Trivia

Um sistema interativo para gincanas culturais que combina sorteio de disciplinas, perguntas e placar para equipes.

## 🚀 Funcionalidades

- **Roleta Interativa**: Sorteia disciplinas aleatoriamente com animação
- **Banco de Perguntas**: Perguntas organizadas por disciplina (História, Geografia, Ciências, Literatura, Matemática, Artes)
- **Sistema de Pontuação**: Placar em tempo real para 4 equipes
- **Interface Responsiva**: Design moderno e intuitivo
- **Controles do Apresentador**: Funções especiais para quem conduz a gincana

## 📁 Estrutura do Projeto

```
gincana/
├── app.py              # Servidor Flask
├── requirements.txt    # Dependências Python
├── data/
│   └── perguntas.json  # Arquivo com as perguntas
├── static/
│   ├── css/
│   │   └── style.css   # Estilos visuais
│   └── js/
│       └── scripts.js  # Lógica de interação
└── templates/
    └── index.html      # Página principal do jogo
```

## 🛠️ Como Executar

### 1. Pré-requisitos
- Python 3.7+ instalado
- Ambiente virtual (recomendado)

### 2. Instalação
```bash
# Clone o repositório
git clone https://github.com/GianKretzl/Trivia_Quizz.git
cd Trivia_Quizz

# Crie um ambiente virtual (opcional)
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução
```bash
python app.py
```

### 4. Acesso
Abra seu navegador e acesse: `http://localhost:5000`

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
