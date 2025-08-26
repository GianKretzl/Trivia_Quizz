from flask import Flask, render_template, jsonify, request
import json
import random
import os

app = Flask(__name__)

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

@app.route('/api/configurar_jogo', methods=['POST'])
def configurar_jogo():
    """Configura o jogo com turma e equipes selecionadas"""
    global jogo_estado
    
    dados = request.get_json()
    print(f"Configurando jogo com dados: {dados}")
    
    turma = dados.get('turma')
    num_equipes = dados.get('num_equipes')
    cores_selecionadas = dados.get('cores_equipes', [])
    
    # Validações
    if not turma or turma not in ['6_ano', '7_ano', '8_ano', '9_ano', 'ensino_medio']:
        return jsonify({'erro': 'Turma inválida'}), 400
    
    if not num_equipes or num_equipes < 2 or num_equipes > 12:
        return jsonify({'erro': 'Número de equipes deve ser entre 2 e 12'}), 400
    
    if len(cores_selecionadas) != num_equipes:
        return jsonify({'erro': 'Número de cores deve corresponder ao número de equipes'}), 400
    
    # Validar se as cores selecionadas existem
    nomes_cores_validas = [cor['nome'] for cor in CORES_EQUIPES]
    for cor_nome in cores_selecionadas:
        if cor_nome not in nomes_cores_validas:
            return jsonify({'erro': f'Cor inválida: {cor_nome}'}), 400
    
    # Configurar o estado do jogo
    jogo_estado['turma_selecionada'] = turma
    jogo_estado['equipes'] = []
    jogo_estado['pontuacao'] = {}
    
    # Buscar informações completas das cores
    cores_completas = []
    for cor_nome in cores_selecionadas:
        cor_info = next((cor for cor in CORES_EQUIPES if cor['nome'] == cor_nome), None)
        if cor_info:
            cores_completas.append(cor_info)
        else:
            # Fallback se não encontrar a cor
            cores_completas.append({'nome': cor_nome, 'hex': '#808080'})
    
    for i, cor_info in enumerate(cores_completas):
        equipe = {
            'id': i + 1,
            'nome': f'Equipe {cor_info["nome"]}',
            'cor': cor_info['nome'],
            'hex': cor_info['hex'],
            'pontos': 0
        }
        jogo_estado['equipes'].append(equipe)
        jogo_estado['pontuacao'][f'equipe_{i + 1}'] = 0
    
    print(f"Jogo configurado com sucesso! Equipes: {jogo_estado['equipes']}")
    
    return jsonify({
        'sucesso': True,
        'turma': turma,
        'num_equipes': num_equipes,
        'equipes': jogo_estado['equipes'],
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
