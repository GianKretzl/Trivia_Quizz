import os
import random
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

from models import db, Turma, Equipe, Questao, Rodada, Pergunta6Ano, Pergunta7Ano, Pergunta8Ano, Pergunta9Ano, PerguntaEnsinoMedio
from sqlalchemy import func, case

if os.environ.get('RENDER'):
    database_path = 'sqlite:///trivia_quizz.db'
else:
    database_path = 'sqlite:///trivia_quizz.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ROTA DO RELATÓRIO

# ROTA DO RELATÓRIO (escopo global, antes do main)
@app.route('/relatorio')
def relatorio_route():
    print('[LOG] /relatorio acessado')
    return relatorio()

# ROTA DO RELATÓRIO

def relatorio():
    rodadas_db = Rodada.query.order_by(Rodada.numero.asc()).all()
    print(f'[LOG] Rodadas encontradas: {len(rodadas_db)}')
    rodadas = []
    for rodada in rodadas_db:
        equipe = Equipe.query.get(rodada.equipe_id)
        turma = Turma.query.get(equipe.turma_id) if equipe else None
        tabela_map = {
            '6_ano': Pergunta6Ano,
            '7_ano': Pergunta7Ano,
            '8_ano': Pergunta8Ano,
            '9_ano': Pergunta9Ano,
            'ensino_medio': PerguntaEnsinoMedio
        }
        tabela = tabela_map.get(turma.nome) if turma else None
        questao = tabela.query.get(rodada.questao_id) if tabela else None
        alternativas = []
        resposta_texto = None
        tema = None
        enunciado = None
        if questao:
            alternativas = json.loads(questao.alternativas)
            tema = questao.tema
            enunciado = questao.enunciado
            try:
                posicao = int(questao.resposta_correta)
                if 0 <= posicao < len(alternativas):
                    resposta_texto = alternativas[posicao]
            except Exception:
                resposta_texto = questao.resposta_correta
        rodadas.append({
            'numero': rodada.numero,
            'turma': turma.nome if turma else None,
            'tema': tema,
            'enunciado': enunciado,
            'resposta': resposta_texto,
            'alternativas': alternativas,
            'equipe': equipe.nome if equipe else None,
            'cor': equipe.cor if equipe else None,
            'acertou': rodada.acertou
        })
    total_participacoes = len(rodadas)
    total_acertos = sum(1 for r in rodadas if r['acertou'])
    total_erros = total_participacoes - total_acertos
    taxa_acerto = (total_acertos / total_participacoes * 100) if total_participacoes > 0 else 0
    estatisticas = {
        'total_rodadas': len(rodadas),
        'total_participacoes': total_participacoes,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
        'taxa_acerto': taxa_acerto
    }
    return render_template('relatorio.html', rodadas=rodadas, stats=estatisticas)
def importar_perguntas(ano, arquivo):
    """Importa perguntas de um arquivo específico para uma tabela específica do ano"""
    try:
        with open(arquivo, encoding='utf-8') as f:
            perguntas = json.load(f)

        tabela_map = {
            6: Pergunta6Ano,
            7: Pergunta7Ano,
            8: Pergunta8Ano,
            9: Pergunta9Ano
        }
        tabela = tabela_map.get(ano)
        if not tabela:
            print(f'Tabela para o ano {ano} não encontrada.')
            return

        existe = tabela.query.first()
        if not existe:
            turma_nome = f'{ano}_ano'
            for disciplina, lista in perguntas[turma_nome].items():
                for p in lista:
                    enunciado = p['pergunta']
                    alternativas = json.dumps(p['opcoes'], ensure_ascii=False)
                    resposta_correta = str(p['resposta_correta'])
                    tema = disciplina
                    pergunta = tabela(
                        enunciado=enunciado,
                        resposta_correta=resposta_correta,
                        alternativas=alternativas,
                        tema=tema
                    )
                    db.session.add(pergunta)
            db.session.commit()
            print(f'Perguntas do {ano}º ano importadas automaticamente.')
    except Exception as e:
        print(f'Erro ao importar perguntas do {ano}º ano:', e)

def importar_perguntas_6ano():
    """Importa perguntas do 6º ano"""
    importar_perguntas(6, 'data/perguntas_6_ano.json')

def importar_perguntas_7ano():
    """Importa perguntas do 7º ano"""
    importar_perguntas(7, 'data/perguntas_7_ano.json')

def importar_perguntas_8ano():
    """Importa perguntas do 8º ano"""
    importar_perguntas(8, 'data/perguntas_8_ano.json')

def importar_perguntas_9ano():
    """Importa perguntas do 9º ano"""
    importar_perguntas(9, 'data/perguntas_9_ano.json')

def importar_perguntas_ensino_medio():
    """Importa perguntas do ensino médio para tabela específica"""
    try:
        with open('data/perguntas_ensino_medio.json', encoding='utf-8') as f:
            perguntas = json.load(f)

        tabela = PerguntaEnsinoMedio
        existe = tabela.query.first()
        if not existe:
            turma_nome = 'ensino_medio'
            for disciplina, lista in perguntas[turma_nome].items():
                for p in lista:
                    enunciado = p['pergunta']
                    alternativas = json.dumps(p['opcoes'], ensure_ascii=False)
                    resposta_correta = str(p['resposta_correta'])
                    tema = disciplina
                    pergunta = tabela(
                        enunciado=enunciado,
                        resposta_correta=resposta_correta,
                        alternativas=alternativas,
                        tema=tema
                    )
                    db.session.add(pergunta)
            db.session.commit()
            print('Perguntas do ensino médio importadas automaticamente.')
    except Exception as e:
        print(f'Erro ao importar perguntas do ensino médio:', e)

import os
import random
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# Configuração do banco de dados
if os.environ.get('RENDER'):
    database_path = 'sqlite:///trivia_quizz.db'
else:
    database_path = 'sqlite:///trivia_quizz.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Turma, Equipe, Questao, Rodada, Pergunta6Ano, Pergunta7Ano, Pergunta8Ano, Pergunta9Ano, PerguntaEnsinoMedio
from sqlalchemy import func, case
db.init_app(app)

def importar_perguntas(ano, arquivo):
    """Importa perguntas de um arquivo específico para uma tabela específica do ano"""
    try:
        with open(arquivo, encoding='utf-8') as f:
            perguntas = json.load(f)
        tabela_map = {
            6: Pergunta6Ano,
            7: Pergunta7Ano,
            8: Pergunta8Ano,
            9: Pergunta9Ano
        }
        tabela = tabela_map.get(ano)
        if not tabela:
            print(f'Tabela para o ano {ano} não encontrada.')
            return
        existe = tabela.query.first()
        if not existe:
            turma_nome = f'{ano}_ano'
            for disciplina, lista in perguntas[turma_nome].items():
                for p in lista:
                    enunciado = p['pergunta']
                    alternativas = json.dumps(p['opcoes'], ensure_ascii=False)
                    resposta_correta = str(p['resposta_correta'])
                    tema = disciplina
                    pergunta = tabela(
                        enunciado=enunciado,
                        resposta_correta=resposta_correta,
                        alternativas=alternativas,
                        tema=tema
                    )
                    db.session.add(pergunta)
            db.session.commit()
            print(f'Perguntas do {ano}º ano importadas automaticamente.')
    except Exception as e:
        print(f'Erro ao importar perguntas do {ano}º ano:', e)
    # Nada relacionado a rodadas aqui, bloco removido
    # Função relatorio corrigida
    rodadas_db = Rodada.query.order_by(Rodada.numero.asc()).all()
    rodadas = []
    for rodada in rodadas_db:
        equipe = Equipe.query.get(rodada.equipe_id)
        turma = Turma.query.get(equipe.turma_id) if equipe else None
        tabela_map = {
            '6_ano': Pergunta6Ano,
            '7_ano': Pergunta7Ano,
            '8_ano': Pergunta8Ano,
            '9_ano': Pergunta9Ano,
            'ensino_medio': PerguntaEnsinoMedio
        }
        tabela = tabela_map.get(turma.nome) if turma else None
        questao = tabela.query.get(rodada.questao_id) if tabela else None
        alternativas = []
        resposta_texto = None
        tema = None
        enunciado = None
        if questao:
            alternativas = json.loads(questao.alternativas)
            tema = questao.tema
            enunciado = questao.enunciado
            try:
                posicao = int(questao.resposta_correta)
                if 0 <= posicao < len(alternativas):
                    resposta_texto = alternativas[posicao]
            except Exception:
                resposta_texto = questao.resposta_correta
        rodadas.append({
            'numero': rodada.numero,
            'turma': turma.nome if turma else None,
            'tema': tema,
            'enunciado': enunciado,
            'resposta': resposta_texto,
            'alternativas': alternativas,
            'equipe': equipe.nome if equipe else None,
            'cor': equipe.cor if equipe else None,
            'acertou': rodada.acertou
        })
    total_participacoes = len(rodadas)
    total_acertos = sum(1 for r in rodadas if r['acertou'])
    total_erros = total_participacoes - total_acertos
    taxa_acerto = (total_acertos / total_participacoes * 100) if total_participacoes > 0 else 0
    estatisticas = {
        'total_rodadas': len(rodadas),
        'total_participacoes': total_participacoes,
        'total_acertos': total_acertos,
        'total_erros': total_erros,
        'taxa_acerto': taxa_acerto
    }
    return render_template('relatorio.html', rodadas=rodadas, stats=estatisticas)

@app.route('/api/relatorio/dados')
def api_relatorio_dados():
    """API para obter dados do relatório em formato JSON"""
    from sqlalchemy import func
    import json
    
    rodadas_db = Rodada.query.order_by(Rodada.numero.asc()).all()
    dados = []
    for rodada in rodadas_db:
        equipe = Equipe.query.get(rodada.equipe_id)
        turma = Turma.query.get(equipe.turma_id) if equipe else None
        tabela_map = {
            '6_ano': Pergunta6Ano,
            '7_ano': Pergunta7Ano,
            '8_ano': Pergunta8Ano,
            '9_ano': Pergunta9Ano,
            'ensino_medio': PerguntaEnsinoMedio
        }
        tabela = tabela_map.get(turma.nome) if turma else None
        questao = tabela.query.get(rodada.questao_id) if tabela else None
        alternativas = []
        resposta_texto = None
        tema = None
        enunciado = None
        if questao:
            alternativas = json.loads(questao.alternativas)
            tema = questao.tema
            enunciado = questao.enunciado
            try:
                posicao = int(questao.resposta_correta)
                if 0 <= posicao < len(alternativas):
                    resposta_texto = alternativas[posicao]
            except Exception:
                resposta_texto = questao.resposta_correta
        dados.append({
            'numero': rodada.numero,
            'turma': turma.nome if turma else None,
            'tema': tema,
            'enunciado': enunciado,
            'resposta': resposta_texto,
            'alternativas': alternativas,
            'equipe': equipe.nome if equipe else None,
            'cor': equipe.cor if equipe else None,
            'acertou': rodada.acertou
        })
    return jsonify(dados)

@app.route('/api/relatorio/estatisticas')
def api_relatorio_estatisticas():
    """API para obter estatísticas do relatório"""
    total_rodadas = Rodada.query.count()
    total_acertos = Rodada.query.filter_by(acertou=True).count()
    total_erros = total_rodadas - total_acertos
    taxa_acerto = (total_acertos / total_rodadas * 100) if total_rodadas > 0 else 0
    
    # Estatísticas por tema
    stats_tema = (
        db.session.query(
            Questao.tema,
            func.count(Rodada.id).label('total'),
            func.sum(case((Rodada.acertou == True, 1), else_=0)).label('acertos')
        )
        .join(Questao, Rodada.questao_id == Questao.id)
        .group_by(Questao.tema)
        .all()
    )
    
    # Estatísticas por equipe
    stats_equipe = (
        db.session.query(
            Equipe.nome.label('equipe'),
            Equipe.cor,
            func.count(Rodada.id).label('total'),
            func.sum(case((Rodada.acertou == True, 1), else_=0)).label('acertos')
        )
        .join(Equipe, Rodada.equipe_id == Equipe.id)
        .group_by(Equipe.nome, Equipe.cor)
        .all()
    )
    
    return jsonify({
        'geral': {
            'total_rodadas': total_rodadas,
            'total_acertos': total_acertos,
            'total_erros': total_erros,
            'taxa_acerto': round(taxa_acerto, 1)
        },
        'por_tema': [
            {
                'tema': s.tema,
                'total': s.total,
                'acertos': s.acertos or 0,
                'taxa_acerto': round((s.acertos or 0) / s.total * 100, 1) if s.total > 0 else 0
            }
            for s in stats_tema
        ],
        'por_equipe': [
            {
                'equipe': s.equipe,
                'cor': s.cor,
                'total': s.total,
                'acertos': s.acertos or 0,
                'taxa_acerto': round((s.acertos or 0) / s.total * 100, 1) if s.total > 0 else 0
            }
            for s in stats_equipe
        ]
    })

@app.route('/novo_jogo')
def novo_jogo():
    # Limpa apenas rodadas, equipes e turmas, mantendo as questões
    Rodada.query.delete()
    Equipe.query.delete()
    Turma.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/pergunta')
@app.route('/pergunta/<tema>')
def pergunta(tema=None):
    import random
    import json
    
    # Se não há tema especificado, tenta buscar do parâmetro GET
    if not tema:
        tema = request.args.get('tema')
    
    # Buscar uma pergunta aleatória do tema
    # Priorizar turma que tem equipes cadastradas
    turma = Turma.query.join(Equipe).first()
    if not turma:
        # Fallback para a primeira turma disponível
        turma = Turma.query.first()
    if not turma:
        return "Erro: Nenhuma turma encontrada", 404
    
    # Mapeamento de nomes de disciplinas baseado na turma
    if turma.nome == 'ensino_medio':
        mapeamento_temas = {
            'Português': 'portugues',
            'Matemática': 'matematica',
            'Biologia': 'biologia',  # Ciências vira Biologia no ensino médio
            'História': 'historia',
            'Geografia': 'geografia',
            'Língua Inglesa': 'lingua_inglesa',
            'Educação Física': 'educacao_fisica',
            'Educação Financeira': 'educacao_financeira',
            'Filosofia': 'filosofia',
            'Química': 'quimica',
            'Física': 'fisica'
        }
    else:
        # Para fundamental (6º, 7º, 8º, 9º ano)
        mapeamento_temas = {
            'Português': 'portugues',
            'Matemática': 'matematica',
            'Ciências': 'ciencias',
            'História': 'historia',
            'Geografia': 'geografia',
            'Língua Inglesa': 'lingua_inglesa',
            'Educação Física': 'educacao_fisica'
        }
    
    tema_db = mapeamento_temas.get(tema, tema.lower() if tema else None)
    
    if not tema_db:
        return f"Erro: Disciplina '{tema}' não disponível para {turma.nome}", 400
    
    # Verificar se a disciplina é válida para a turma
    disciplinas_validas = obter_disciplinas_por_turma(turma.nome)
    if tema_db not in disciplinas_validas:
        return f"Erro: Disciplina '{tema}' não disponível para {turma.nome}", 400
    
    tabela_map = {
        '6_ano': Pergunta6Ano,
        '7_ano': Pergunta7Ano,
        '8_ano': Pergunta8Ano,
        '9_ano': Pergunta9Ano,
        'ensino_medio': PerguntaEnsinoMedio
    }
    tabela = tabela_map.get(turma.nome)
    if not tabela:
        return f"Erro: Tabela de perguntas não encontrada para {turma.nome}", 400

    questoes = tabela.query.filter_by(tema=tema_db).all()
    if not questoes:
        return f"Erro: Nenhuma pergunta encontrada para o tema {tema}", 404

    questao_escolhida = random.choice(questoes)
    alternativas = json.loads(questao_escolhida.alternativas)
    
    print("-" * 50)
    print("### LOG: Questão Selecionada para a Rodada ###")
    print(f"Turma: {turma.nome}")
    print(f"Disciplina: {tema}")
    print(f"ID da Questão: {questao_escolhida.id}")
    print(f"Enunciado: {questao_escolhida.enunciado}")
    print(f"Alternativas: {alternativas}")
    print(f"Resposta Correta: {alternativas[int(questao_escolhida.resposta_correta)]}")
    print("-" * 50)
    
    # Buscar equipes da turma
    equipes = Equipe.query.filter_by(turma_id=turma.id).all()
    
    return render_template('pergunta.html', 
                         questao=questao_escolhida,
                         alternativas=alternativas,
                         tema=tema,
                         equipes=equipes)

@app.route('/processar_respostas', methods=['POST'])
def processar_respostas():
    try:
        dados = request.get_json()
        print(f"[DEBUG] Dados recebidos: {dados}")
        
        questao_id = dados.get('questao_id')
        equipes_acertos = dados.get('equipes_acertos', [])
        
        print(f"[DEBUG] Processando questao_id: {questao_id}, equipes_acertos: {equipes_acertos}")
        
        # Buscar turma ativa
        turma = db.session.query(Turma).join(Equipe).first()
        tabela_map = {
            '6_ano': Pergunta6Ano,
            '7_ano': Pergunta7Ano,
            '8_ano': Pergunta8Ano,
            '9_ano': Pergunta9Ano,
            'ensino_medio': PerguntaEnsinoMedio
        }
        tabela = tabela_map.get(turma.nome) if turma else None
        questao = tabela.query.get(questao_id) if tabela else None
        if not questao:
            print(f"[DEBUG] ❌ Questão {questao_id} não encontrada na tabela {tabela.__name__ if tabela else 'N/A'}")
            return jsonify({'erro': 'Questão não encontrada', 'sucesso': False}), 404
        
        # Pegar o último número de rodada
        ultima_rodada = db.session.query(db.func.max(Rodada.numero)).scalar() or 0
        novo_numero_rodada = ultima_rodada + 1
        
        print(f"[DEBUG] Nova rodada número: {novo_numero_rodada}")
        
        # Registrar rodadas para todas as equipes
        # Buscar a turma que tem equipes cadastradas
        turma = db.session.query(Turma).join(Equipe).first()
        if not turma:
            print("[DEBUG] ❌ Nenhuma turma com equipes encontrada")
            return jsonify({'erro': 'Nenhuma turma com equipes encontrada', 'sucesso': False}), 404
            
        print(f"[DEBUG] Turma selecionada: {turma.id} - {turma.nome}")
        equipes = Equipe.query.filter_by(turma_id=turma.id).all()
        print(f"[DEBUG] Equipes encontradas: {[(e.id, e.nome) for e in equipes]}")
        
        rodadas_criadas = 0
        for equipe in equipes:
            acertou = equipe.id in equipes_acertos
            print(f"[DEBUG] Equipe {equipe.nome} (ID: {equipe.id}): {'ACERTOU' if acertou else 'ERROU'}")
            
            rodada = Rodada(
                equipe_id=equipe.id,
                questao_id=questao_id,
                tema=questao.tema,
                acertou=acertou,
                resposta=questao.resposta_correta if acertou else "",
                numero=novo_numero_rodada
            )
            db.session.add(rodada)
            rodadas_criadas += 1
        
        db.session.commit()
        print(f"[DEBUG] ✅ Sucesso! {rodadas_criadas} rodadas criadas, commit realizado")
        
        # Verificar se as rodadas foram salvas
        total_rodadas = Rodada.query.count()
        print(f"[DEBUG] Total de rodadas no banco agora: {total_rodadas}")
        
        return jsonify({'sucesso': True, 'rodada': novo_numero_rodada, 'rodadas_criadas': rodadas_criadas})
        
    except Exception as e:
        print(f"[DEBUG] ❌ Erro ao processar respostas: {str(e)}")
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}', 'sucesso': False}), 500

@app.route('/api/estado_jogo', methods=['GET'])
def estado_jogo():
    """Retorna o estado atual do jogo (equipes, cores, pontuação, etc) do banco"""
    # Buscar a turma que tem equipes cadastradas
    turma = db.session.query(Turma).join(Equipe).first()
    equipes = []
    if turma:
        equipes_db = Equipe.query.filter_by(turma_id=turma.id).all()
        for eq in equipes_db:
            # Calcular pontuação total da equipe
            pontos = db.session.query(db.func.count(Rodada.id)).filter_by(
                equipe_id=eq.id, 
                acertou=True
            ).scalar() * 1
            
            equipes.append({
                'id': eq.id,
                'nome': eq.nome,
                'cor': eq.cor,
                'pontos': pontos
            })
    return jsonify({
        'equipes': equipes,
        'turma': turma.nome if turma else None,
        'turma_ativa': turma.nome if turma else None
    })

# Estado do jogo
jogo_estado = {
    'turma_selecionada': None,
    'equipes': [],
    'pergunta_atual': None,
    'disciplina_atual': None,
    'pontuacao': {}
}

# Disciplinas disponíveis por nível de ensino
DISCIPLINAS_FUNDAMENTAL = [
    'portugues',
    'matematica', 
    'lingua_inglesa',
    'ciencias',
    'geografia',
    'historia',
    'educacao_fisica'
]

DISCIPLINAS_ENSINO_MEDIO = [
    'portugues',
    'matematica', 
    'lingua_inglesa',
    'biologia',  # Ciências vira Biologia no ensino médio
    'geografia',
    'historia',
    'educacao_fisica',
    'educacao_financeira',
    'filosofia',
    'quimica',
    'fisica'
]

# Mapeamento de disciplinas para nomes amigáveis
NOMES_DISCIPLINAS = {
    'portugues': 'Português',
    'matematica': 'Matemática',
    'lingua_inglesa': 'Língua Inglesa', 
    'ciencias': 'Ciências',
    'biologia': 'Biologia',
    'geografia': 'Geografia',
    'historia': 'História',
    'educacao_fisica': 'Educação Física',
    'educacao_financeira': 'Educação Financeira',
    'filosofia': 'Filosofia',
    'quimica': 'Química',
    'fisica': 'Física'
}

# Função para obter disciplinas baseada na turma
def obter_disciplinas_por_turma(turma_nome):
    """Retorna as disciplinas disponíveis para uma turma específica (baseado nas questões reais no BD)"""
    tabela_map = {
        '6_ano': Pergunta6Ano,
        '7_ano': Pergunta7Ano,
        '8_ano': Pergunta8Ano,
        '9_ano': Pergunta9Ano,
        'ensino_medio': PerguntaEnsinoMedio
    }
    tabela = tabela_map.get(turma_nome)
    if not tabela:
        print(f"[LOG] Tabela de perguntas não encontrada para '{turma_nome}'.", flush=True)
        return []
    print(f"[LOG] Buscando disciplinas na tabela: {tabela.__name__}", flush=True)
    disciplinas_reais = db.session.query(tabela.tema).distinct().all()
    disciplinas_disponiveis = [d[0] for d in disciplinas_reais]
    print(f"[LOG] Disciplinas reais encontradas para turma '{turma_nome}': {disciplinas_disponiveis}", flush=True)
    return disciplinas_disponiveis

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

def carregar_perguntas(ano=None):
    """Carrega as perguntas do arquivo JSON correspondente ao ano"""
    if ano:
        arquivo = f'data/perguntas_{ano}_ano.json'
    else:
        # Para manter compatibilidade
        arquivo = 'data/perguntas_6_ano.json'

    print(f"[LOG] Carregando perguntas do arquivo: {arquivo}", flush=True)
    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Arquivo de perguntas não encontrado: {arquivo}")
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
    turma_nome = dados.get('turma')
    
    # Obter disciplinas disponíveis para a turma
    disciplinas_disponiveis = obter_disciplinas_por_turma(turma_nome)

    # Se não houver disciplinas, importar perguntas automaticamente
    if not disciplinas_disponiveis:
        print(f"[LOG] Nenhuma disciplina encontrada para '{turma_nome}'. Importando perguntas automaticamente...", flush=True)
        ano_param = turma_nome.split('_')[0] if turma_nome != 'ensino_medio' else 'ensino_medio'
        importar_perguntas(int(ano_param) if ano_param.isdigit() else ano_param, f'data/perguntas_{ano_param}_ano.json' if ano_param != 'ensino_medio' else 'data/perguntas_ensino_medio.json')
        disciplinas_disponiveis = obter_disciplinas_por_turma(turma_nome)

    print(f"[DEBUG] Configurando jogo com dados: {dados}")
    turma = Turma.query.filter_by(nome=turma_nome).first()
    # Adicionar o log da turma selecionada
    print(f"[DEBUG] ### LOG: Jogo configurado para a turma: {turma.nome if turma else turma_nome} ###")
    print(f"[DEBUG] Disciplinas disponíveis para {turma_nome}: {disciplinas_disponiveis}")

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
    print(f"[DEBUG] Jogo configurado com sucesso! Equipes: {equipes}")
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
    
    turma = jogo_estado['turma_selecionada']
    ano_param = turma.split('_')[0] if turma != 'ensino_medio' else 'ensino_medio'
    # Corrige para garantir que o bloco de perguntas seja do ano correto
    if ano_param != 'ensino_medio':
        arquivo_perguntas = f"data/perguntas_{ano_param}_ano.json"
    else:
        arquivo_perguntas = "data/perguntas_ensino_medio.json"
    perguntas = carregar_perguntas(ano=ano_param)
    print(f"[LOG] Arquivo de perguntas utilizado: {arquivo_perguntas}")

    # Garante que o bloco de perguntas seja do ano/turma correto
    bloco_turma = turma if turma in perguntas else f"{ano_param}_ano"
    if bloco_turma not in perguntas:
        print(f"[ERRO] Bloco de perguntas '{bloco_turma}' não encontrado no arquivo {arquivo_perguntas}", flush=True)
        return jsonify({'erro': f'Perguntas não encontradas para {turma}'}), 404
    
    # Sorteio sem repetição: ciclo de disciplinas por turma
    if 'disciplinas_ciclo' not in jogo_estado or jogo_estado.get('turma_ciclo') != turma:
        # Inicia ciclo novo se mudou de turma ou não existe
        disciplinas_disponiveis = obter_disciplinas_por_turma(turma)
        print(f"[LOG] Disciplinas disponíveis para sorteio: {disciplinas_disponiveis}", flush=True)
        if 'geografia' not in [d.lower() for d in disciplinas_disponiveis]:
            print(f"[ALERTA] Geografia NÃO está entre as disciplinas sorteáveis para a turma '{turma}'. Verifique perguntas cadastradas!", flush=True)
        random.shuffle(disciplinas_disponiveis)
        jogo_estado['disciplinas_ciclo'] = disciplinas_disponiveis
        jogo_estado['turma_ciclo'] = turma
        jogo_estado['indice_disciplina_ciclo'] = 0
    else:
        disciplinas_disponiveis = jogo_estado['disciplinas_ciclo']

    print(f"[LOG] Ciclo atual de disciplinas: {disciplinas_disponiveis}", flush=True)
    indice = jogo_estado.get('indice_disciplina_ciclo', 0)
    disciplina = disciplinas_disponiveis[indice]
    print(f"[LOG] Sorteando disciplina: {disciplina} (índice {indice})", flush=True)

    # Verifica se a disciplina tem perguntas
    if disciplina not in perguntas[turma] or not perguntas[turma][disciplina]:
        print(f"[LOG] Disciplina '{disciplina}' não tem perguntas disponíveis. Pulando para próxima.", flush=True)
        jogo_estado['indice_disciplina_ciclo'] = (indice + 1) % len(disciplinas_disponiveis)
        return sortear_disciplina()

    pergunta = random.choice(perguntas[turma][disciplina])

    jogo_estado['indice_disciplina_ciclo'] = (indice + 1) % len(disciplinas_disponiveis)
    jogo_estado['disciplina_atual'] = disciplina
    jogo_estado['pergunta_atual'] = pergunta

    print(f"[LOG] Pergunta sorteada para disciplina '{disciplina}': {pergunta['pergunta']}", flush=True)

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
            jogo_estado['pontuacao'][equipe_key] += 1
            
            # Atualizar também na lista de equipes
            for equipe in jogo_estado['equipes']:
                if equipe['id'] == int(equipe_id):
                    equipe['pontos'] += 1
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

@app.route('/api/ajustar_pontos', methods=['POST'])
def ajustar_pontos():
    """Ajusta pontos de uma equipe (+1 ou -1) criando uma rodada fictícia no banco"""
    try:
        data = request.get_json()
        nome_equipe = data.get('equipe')
        pontos = data.get('pontos', 0)
        
        if not nome_equipe:
            return jsonify({'sucesso': False, 'erro': 'Nome da equipe é obrigatório'}), 400
            
        if pontos not in [-1, 1]:
            return jsonify({'sucesso': False, 'erro': 'Apenas +1 ou -1 ponto permitido'}), 400
        
        # Buscar a equipe no banco de dados
        equipe = Equipe.query.filter_by(nome=nome_equipe).first()
        if not equipe:
            return jsonify({'sucesso': False, 'erro': 'Equipe não encontrada no banco'}), 404

        # Calcular pontuação atual da equipe
        pontos_atuais = db.session.query(db.func.count(Rodada.id)).filter_by(
            equipe_id=equipe.id,
            acertou=True
        ).scalar() or 0

        # Calcular nova pontuação
        nova_pontuacao = pontos_atuais + pontos

        # Não permitir pontuação negativa
        if nova_pontuacao < 0:
            return jsonify({'sucesso': False, 'erro': 'Pontuação não pode ser negativa'}), 400

        # Buscar a turma da equipe
        turma = Turma.query.get(equipe.turma_id)
        tabela_map = {
            '6_ano': Pergunta6Ano,
            '7_ano': Pergunta7Ano,
            '8_ano': Pergunta8Ano,
            '9_ano': Pergunta9Ano,
            'ensino_medio': PerguntaEnsinoMedio
        }
        tabela = tabela_map.get(turma.nome) if turma else None

        if pontos == 1:
            # Adicionar ponto: criar uma rodada fictícia com acerto
            questao = tabela.query.first() if tabela else None
            if not questao:
                return jsonify({'sucesso': False, 'erro': 'Nenhuma questão encontrada no sistema'}), 404

            # Pegar o último número de rodada
            ultima_rodada = db.session.query(db.func.max(Rodada.numero)).scalar() or 0
            novo_numero_rodada = ultima_rodada + 1

            # Criar rodada de ajuste com acerto
            rodada_ajuste = Rodada(
                equipe_id=equipe.id,
                questao_id=questao.id,
                tema='ajuste_manual',
                acertou=True,
                resposta=questao.resposta_correta,
                numero=novo_numero_rodada
            )
            db.session.add(rodada_ajuste)

        else:  # pontos == -1
            # Remover ponto: encontrar a última rodada com acerto desta equipe e marcar como erro
            ultima_rodada_acerto = Rodada.query.filter_by(
                equipe_id=equipe.id,
                acertou=True
            ).order_by(Rodada.id.desc()).first()

            if not ultima_rodada_acerto:
                return jsonify({'sucesso': False, 'erro': 'Equipe não tem pontos para remover'}), 400

            # Marcar como erro (ou excluir a rodada - vou marcar como erro para manter histórico)
            ultima_rodada_acerto.acertou = False
            ultima_rodada_acerto.tema = 'ajuste_manual_remocao'
        
        db.session.commit()
        
        print(f"[DEBUG] ✅ Pontos ajustados no banco: {nome_equipe} {'+' if pontos > 0 else ''}{pontos} = {nova_pontuacao}")
        
        return jsonify({
            'sucesso': True, 
            'equipe': nome_equipe,
            'pontos_ajustados': pontos,
            'nova_pontuacao': nova_pontuacao
        })
        
    except Exception as e:
        print(f"[DEBUG] ❌ Erro ao ajustar pontos: {e}")
        db.session.rollback()
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/api/reset_jogo', methods=['POST'])
def reset_jogo():
    global jogo_estado
    jogo_estado = {
        'turma_selecionada': None,
        'equipes': [],
        'pergunta_atual': None,
        'disciplina_atual': None,
        'pontuacao': {}
    }
    return jsonify({'sucesso': True})

# ROTA DO RELATÓRIO
@app.route('/relatorio')
def relatorio_route():
    print('[LOG] /relatorio acessado')
    return relatorio()

if __name__ == '__main__':


    # Garante que todas as tabelas do banco existem antes de iniciar o app
    with app.app_context():
        db.create_all()

    # Para produção no Render
    if os.environ.get('RENDER'):
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Para desenvolvimento local
        # Para acesso apenas local: app.run(debug=True)
        # Para acesso na rede local: app.run(host='0.0.0.0', port=5000, debug=True)
        app.run(debug=True)

# Endpoint para informar a última disciplina sorteada para a roleta
@app.route('/api/ultima_disciplina', methods=['GET'])
def ultima_disciplina():
    global jogo_estado
    disciplina = jogo_estado.get('disciplina_atual')
    return jsonify({'disciplina': disciplina})