import json
def importar_perguntas_6ano():
    try:
        with open('data/perguntas.json', encoding='utf-8') as f:
            perguntas = json.load(f)
        turma = Turma.query.filter_by(nome='6_ano').first()
        if not turma:
            turma = Turma(nome='6_ano')
            db.session.add(turma)
            db.session.commit()
        # Só importa se não houver questões dessa turma
        existe = Questao.query.filter_by(turma_id=turma.id).first()
        if not existe:
            for disciplina, lista in perguntas['6_ano'].items():
                for p in lista:
                    enunciado = p['pergunta']
                    alternativas = json.dumps(p['opcoes'], ensure_ascii=False)
                    resposta_correta = str(p['resposta_correta'])
                    tema = disciplina
                    questao = Questao(
                        turma_id=turma.id,
                        enunciado=enunciado,
                        resposta_correta=resposta_correta,
                        alternativas=alternativas,
                        tema=tema
                    )
                    db.session.add(questao)
            db.session.commit()
            print('Perguntas do 6º ano importadas automaticamente.')
    except Exception as e:
        print('Erro ao importar perguntas do 6º ano:', e)
from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from models import db, Turma, Equipe, Questao, Rodada
import json
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia_quizz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Inicializar banco de dados se não existir
with app.app_context():
    db.create_all()
    importar_perguntas_6ano()
# Rotas extras para relatório, novo jogo e pergunta
@app.route('/relatorio')
def relatorio():
    # Busca rodadas, equipes, temas, perguntas e acertos usando SQLAlchemy
    rodadas = (
        db.session.query(
            Rodada.numero,
            Turma.nome.label('turma'),
            Equipe.nome.label('equipe'),
            Equipe.cor,
            Questao.tema,
            Questao.enunciado,
            Rodada.resposta,
            Rodada.acertou
        )
        .join(Equipe, Rodada.equipe_id == Equipe.id)
        .join(Questao, Rodada.questao_id == Questao.id)
        .join(Turma, Equipe.turma_id == Turma.id)
        .order_by(Rodada.numero.asc())
        .all()
    )
    return render_template('relatorio.html', rodadas=rodadas)

@app.route('/novo_jogo')
def novo_jogo():
    # Limpa apenas rodadas, equipes e turmas, mantendo as questões
    Rodada.query.delete()
    Equipe.query.delete()
    Turma.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/pergunta')
def pergunta():
    return render_template('pergunta.html')

@app.route('/api/estado_jogo', methods=['GET'])
def estado_jogo():
    """Retorna o estado atual do jogo (equipes, cores, pontuação, etc) do banco"""
    turma = Turma.query.order_by(Turma.id.desc()).first()
    equipes = []
    if turma:
        equipes_db = Equipe.query.filter_by(turma_id=turma.id).all()
        for eq in equipes_db:
            equipes.append({
                'id': eq.id,
                'nome': eq.nome,
                'cor': eq.cor,
                'pontos': 0
            })
    return jsonify({
        'equipes': equipes,
        'turma': turma.nome if turma else None
    })

# Estado do jogo
jogo_estado = {
    'turma_selecionada': None,
    'equipes': [],
    'pergunta_atual': None,
    'disciplina_atual': None,
    'pontuacao': {}
}

# Disciplinas disponíveis
DISCIPLINAS = [
    'portugues',
    'matematica', 
    'lingua_inglesa',
    'ciencias',
    'geografia',
    'historia',
    'educacao_fisica'
]

# Mapeamento de disciplinas para nomes amigáveis
NOMES_DISCIPLINAS = {
    'portugues': 'Português',
    'matematica': 'Matemática',
    'lingua_inglesa': 'Língua Inglesa', 
    'ciencias': 'Ciências',
    'geografia': 'Geografia',
    'historia': 'História',
    'educacao_fisica': 'Educação Física'
}

# Cores disponíveis para as equipes (cores personalizadas da gincana)
CORES_EQUIPES = [
    {'nome': 'VERDE', 'hex': '#00FF00'},
    {'nome': 'AMARELO', 'hex': '#FFFF00'},
    {'nome': 'VERMELHO', 'hex': '#FF0000'},
    {'nome': 'AZUL', 'hex': '#0066FF'},
    {'nome': 'LARANJA', 'hex': '#FFA500'},
    {'nome': 'ROXO', 'hex': '#8A2BE2'},
    {'nome': 'AZUL CLARO', 'hex': '#87CEEB'},
    {'nome': 'PRETO', 'hex': '#000000'},
    {'nome': 'BRANCO', 'hex': '#FFFFFF'},
    {'nome': 'ROSA BEBÊ', 'hex': '#FFB6C1'}
]

def carregar_perguntas():
    """Carrega as perguntas do arquivo JSON"""
    try:
        with open('data/perguntas.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Arquivo de perguntas não encontrado!")
        return {}


@app.route('/')
def index():
    """Página principal do jogo"""
    return render_template('index.html')

@app.route('/roleta')
def roleta():
    """Tela da roleta e placar"""
    return render_template('roleta.html')

@app.route('/api/configurar_jogo', methods=['POST'])
def configurar_jogo():
    """Configura o jogo com turma e equipes selecionadas, salvando no banco"""
    dados = request.get_json()
    print(f"Configurando jogo com dados: {dados}")
    turma_nome = dados.get('turma')
    num_equipes = dados.get('num_equipes')
    cores_selecionadas = dados.get('cores_equipes', [])
    if not turma_nome or turma_nome not in ['6_ano', '7_ano', '8_ano', '9_ano', 'ensino_medio']:
        return jsonify({'erro': 'Turma inválida'}), 400
    if not num_equipes or num_equipes < 2 or num_equipes > 12:
        return jsonify({'erro': 'Número de equipes deve ser entre 2 e 12'}), 400
    if len(cores_selecionadas) != num_equipes:
        return jsonify({'erro': 'Número de cores deve corresponder ao número de equipes'}), 400
    nomes_cores_validas = [cor['nome'] for cor in CORES_EQUIPES]
    for cor_nome in cores_selecionadas:
        if cor_nome not in nomes_cores_validas:
            return jsonify({'erro': f'Cor inválida: {cor_nome}'}), 400
    # Cria turma (ou busca existente)
    turma = Turma.query.filter_by(nome=turma_nome).first()
    if not turma:
        turma = Turma(nome=turma_nome)
        db.session.add(turma)
        db.session.commit()
    # Remove equipes antigas dessa turma
    Equipe.query.filter_by(turma_id=turma.id).delete()
    db.session.commit()
    # Adiciona equipes novas
    equipes = []
    for i, cor_nome in enumerate(cores_selecionadas):
        cor_info = next((cor for cor in CORES_EQUIPES if cor['nome'] == cor_nome), None)
        equipe = Equipe(
            nome=f'Equipe {cor_nome}',
            cor=cor_nome,
            turma_id=turma.id
        )
        db.session.add(equipe)
        equipes.append({
            'id': i + 1,
            'nome': f'Equipe {cor_nome}',
            'cor': cor_nome,
            'pontos': 0
        })
    db.session.commit()
    print(f"Jogo configurado com sucesso! Equipes: {equipes}")
    return jsonify({
        'sucesso': True,
        'turma': turma_nome,
        'num_equipes': num_equipes,
        'equipes': equipes,
        'mensagem': f'Jogo configurado com sucesso! {num_equipes} equipes prontas para a gincana.'
    })

@app.route('/api/sortear_disciplina', methods=['GET'])
def sortear_disciplina():
    """Sorteia uma disciplina e uma pergunta aleatória"""
    global jogo_estado
    
    if not jogo_estado['turma_selecionada']:
        return jsonify({'erro': 'Jogo não configurado'}), 400
    
    # Carregar perguntas
    perguntas = carregar_perguntas()
    turma = jogo_estado['turma_selecionada']
    
    if turma not in perguntas:
        return jsonify({'erro': f'Perguntas não encontradas para {turma}'}), 404
    
    # Sortear disciplina
    disciplina = random.choice(DISCIPLINAS)
    
    # Verificar se a disciplina tem perguntas
    if disciplina not in perguntas[turma] or not perguntas[turma][disciplina]:
        return jsonify({'erro': f'Nenhuma pergunta encontrada para {disciplina}'}), 404
    
    # Sortear pergunta da disciplina
    pergunta = random.choice(perguntas[turma][disciplina])
    
    # Salvar estado atual
    jogo_estado['disciplina_atual'] = disciplina
    jogo_estado['pergunta_atual'] = pergunta
    
    return jsonify({
        'disciplina': NOMES_DISCIPLINAS.get(disciplina, disciplina.replace('_', ' ').title()),
        'disciplina_id': disciplina,
        'pergunta': pergunta['pergunta'],
        'opcoes': pergunta['opcoes'],
        'id_pergunta': len(perguntas[turma][disciplina])  # ID temporário
    })

@app.route('/api/responder', methods=['POST'])
def responder():
    """Verifica a resposta e atualiza a pontuação"""
    global jogo_estado
    
    dados = request.get_json()
    equipe_id = dados.get('equipe_id')
    resposta = dados.get('resposta')
    
    if not jogo_estado['pergunta_atual']:
        return jsonify({'erro': 'Nenhuma pergunta ativa'}), 400
    
    # Verificar se a resposta está correta
    resposta_correta = jogo_estado['pergunta_atual']['resposta_correta']
    acertou = resposta == resposta_correta
    
    # Atualizar pontuação se acertou
    if acertou and equipe_id:
        equipe_key = f'equipe_{equipe_id}'
        if equipe_key in jogo_estado['pontuacao']:
            jogo_estado['pontuacao'][equipe_key] += 10
            
            # Atualizar também na lista de equipes
            for equipe in jogo_estado['equipes']:
                if equipe['id'] == int(equipe_id):
                    equipe['pontos'] += 10
                    break
    
    return jsonify({
        'acertou': acertou,
        'resposta_correta': resposta_correta,
        'opcao_correta': jogo_estado['pergunta_atual']['opcoes'][resposta_correta],
        'pontuacao': jogo_estado['pontuacao'],
        'equipes': jogo_estado['equipes']
    })

@app.route('/api/placar', methods=['GET'])
def obter_placar():
    """Retorna o placar atual do jogo"""
    return jsonify({
        'equipes': jogo_estado['equipes'],
        'pontuacao': jogo_estado['pontuacao']
    })

@app.route('/api/cores_disponiveis', methods=['GET'])
def cores_disponiveis():
    """Retorna as cores disponíveis para as equipes"""
    return jsonify({'cores': CORES_EQUIPES})

@app.route('/api/reset_jogo', methods=['POST'])
def reset_jogo():
    """Reinicia o jogo"""
    global jogo_estado
    jogo_estado = {
        'turma_selecionada': None,
        'equipes': [],
        'pergunta_atual': None,
        'disciplina_atual': None,
        'pontuacao': {}
    }
    return jsonify({'sucesso': True})

if __name__ == '__main__':
    app.run(debug=True)
