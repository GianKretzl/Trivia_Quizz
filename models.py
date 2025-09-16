from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    equipes = db.relationship('Equipe', backref='turma', lazy=True)
    questoes = db.relationship('Questao', backref='turma', lazy=True)

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(30), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    rodadas = db.relationship('Rodada', backref='equipe', lazy=True)

class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)
    rodadas = db.relationship('Rodada', backref='questao', lazy=True)

class Rodada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    tema = db.Column(db.String(50))
    acertou = db.Column(db.Boolean)
    resposta = db.Column(db.String(255))
    numero = db.Column(db.Integer)

# Modelos separados para perguntas de cada ano
class Pergunta6Ano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)

class Pergunta7Ano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)

class Pergunta8Ano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)

class Pergunta9Ano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)

class PerguntaEnsinoMedio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    resposta_correta = db.Column(db.String(255), nullable=False)
    alternativas = db.Column(db.Text, nullable=False)
    tema = db.Column(db.String(50), nullable=False)
