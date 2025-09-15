import sqlite3
import json
import os

def verificar_banco_dados():
    """Verifica se as perguntas do ensino médio estão no banco de dados"""
    
    # Conectar ao banco
    conn = sqlite3.connect('instance/trivia_quizz.db')
    cursor = conn.cursor()
    
    print("=== VERIFICANDO BANCO DE DADOS ===")
    
    # Verificar turmas
    cursor.execute("SELECT * FROM turma")
    turmas = cursor.fetchall()
    print(f"Turmas encontradas: {turmas}")
    
    # Verificar se existe turma ensino_medio
    cursor.execute("SELECT * FROM turma WHERE nome = 'ensino_medio'")
    turma_em = cursor.fetchone()
    if turma_em:
        print(f"Turma ensino médio encontrada: {turma_em}")
        
        # Verificar questões do ensino médio
        cursor.execute("SELECT COUNT(*) FROM questao WHERE turma_id = ?", (turma_em[0],))
        total_questoes = cursor.fetchone()[0]
        print(f"Total de questões do ensino médio: {total_questoes}")
        
        # Verificar questões por tema
        cursor.execute("SELECT tema, COUNT(*) FROM questao WHERE turma_id = ? GROUP BY tema", (turma_em[0],))
        questoes_por_tema = cursor.fetchall()
        print(f"Questões por tema:")
        for tema, count in questoes_por_tema:
            print(f"  {tema}: {count} questões")
            
    else:
        print("❌ Turma ensino_medio NÃO encontrada!")
    
    conn.close()

def verificar_arquivo_json():
    """Verifica o arquivo JSON do ensino médio"""
    print("\n=== VERIFICANDO ARQUIVO JSON ===")
    
    try:
        with open('data/perguntas_ensino_medio.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        if 'ensino_medio' in dados:
            print("✅ Estrutura ensino_medio encontrada no JSON")
            disciplinas = dados['ensino_medio'].keys()
            print(f"Disciplinas disponíveis: {list(disciplinas)}")
            
            for disciplina, perguntas in dados['ensino_medio'].items():
                print(f"  {disciplina}: {len(perguntas)} perguntas")
        else:
            print("❌ Estrutura ensino_medio NÃO encontrada no JSON")
            print(f"Chaves encontradas: {list(dados.keys())}")
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo JSON: {e}")

def reimportar_ensino_medio():
    """Reimporta as perguntas do ensino médio"""
    print("\n=== REIMPORTANDO ENSINO MÉDIO ===")
    
    # Conectar ao banco
    conn = sqlite3.connect('instance/trivia_quizz.db')
    cursor = conn.cursor()
    
    try:
        # Carregar JSON
        with open('data/perguntas_ensino_medio.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Verificar se existe turma ensino_medio, se não criar
        cursor.execute("SELECT id FROM turma WHERE nome = 'ensino_medio'")
        turma_result = cursor.fetchone()
        
        if turma_result:
            turma_id = turma_result[0]
            print(f"Turma ensino_medio já existe com ID: {turma_id}")
            
            # Deletar questões existentes
            cursor.execute("DELETE FROM questao WHERE turma_id = ?", (turma_id,))
            print("Questões antigas removidas")
        else:
            # Criar turma
            cursor.execute("INSERT INTO turma (nome) VALUES ('ensino_medio')")
            turma_id = cursor.lastrowid
            print(f"Turma ensino_medio criada com ID: {turma_id}")
        
        # Inserir questões
        total_inseridas = 0
        for disciplina, perguntas in dados['ensino_medio'].items():
            for pergunta in perguntas:
                cursor.execute("""
                    INSERT INTO questao (turma_id, enunciado, resposta_correta, alternativas, tema)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    turma_id,
                    pergunta['pergunta'],
                    str(pergunta['resposta_correta']),
                    json.dumps(pergunta['opcoes'], ensure_ascii=False),
                    disciplina
                ))
                total_inseridas += 1
        
        conn.commit()
        print(f"✅ {total_inseridas} questões importadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante reimportação: {e}")
        conn.rollback()
    finally:
        conn.close()

def testar_consulta_ensino_medio():
    """Testa uma consulta específica para ensino médio"""
    print("\n=== TESTANDO CONSULTA ===")
    
    conn = sqlite3.connect('instance/trivia_quizz.db')
    cursor = conn.cursor()
    
    # Buscar turma ensino_medio
    cursor.execute("SELECT id FROM turma WHERE nome = 'ensino_medio'")
    turma = cursor.fetchone()
    
    if turma:
        turma_id = turma[0]
        print(f"Turma ID: {turma_id}")
        
        # Testar busca por algumas disciplinas específicas
        disciplinas_teste = ['portugues', 'matematica', 'biologia', 'filosofia']
        
        for disciplina in disciplinas_teste:
            cursor.execute("SELECT COUNT(*) FROM questao WHERE turma_id = ? AND tema = ?", (turma_id, disciplina))
            count = cursor.fetchone()[0]
            print(f"  {disciplina}: {count} questões encontradas")
            
            if count > 0:
                # Buscar uma pergunta exemplo
                cursor.execute("SELECT enunciado FROM questao WHERE turma_id = ? AND tema = ? LIMIT 1", (turma_id, disciplina))
                exemplo = cursor.fetchone()
                if exemplo:
                    print(f"    Exemplo: {exemplo[0][:100]}...")
    else:
        print("❌ Turma ensino_medio não encontrada")
    
    conn.close()

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DO ENSINO MÉDIO")
    print("=" * 50)
    
    # Verificar se o arquivo do banco existe
    if os.path.exists('instance/trivia_quizz.db'):
        verificar_banco_dados()
    else:
        print("❌ Banco de dados não encontrado!")
    
    # Verificar arquivo JSON
    verificar_arquivo_json()
    
    # Perguntar se quer reimportar
    resposta = input("\n🔧 Deseja reimportar as perguntas do ensino médio? (s/n): ")
    if resposta.lower() == 's':
        reimportar_ensino_medio()
        print("\n🔍 Verificando após reimportação...")
        verificar_banco_dados()
        testar_consulta_ensino_medio()
    else:
        testar_consulta_ensino_medio()