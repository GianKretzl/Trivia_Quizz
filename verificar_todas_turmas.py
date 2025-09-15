#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from collections import defaultdict

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Turma, Questao

def verificar_arquivo_json(arquivo, turma_esperada):
    """Verifica a estrutura de um arquivo JSON"""
    print(f"\n📁 Verificando {arquivo}...")
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return False
        
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        if turma_esperada not in dados:
            print(f"❌ Turma '{turma_esperada}' não encontrada no arquivo")
            print(f"   Turmas disponíveis: {list(dados.keys())}")
            return False
            
        disciplinas = dados[turma_esperada]
        total_questoes = 0
        
        print(f"✅ Arquivo válido - Estrutura encontrada:")
        for disciplina, questoes in disciplinas.items():
            print(f"   📚 {disciplina}: {len(questoes)} questões")
            total_questoes += len(questoes)
            
        print(f"   📊 Total: {total_questoes} questões")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False

def verificar_bd_turma(turma_nome):
    """Verifica as questões de uma turma no banco de dados"""
    print(f"\n🏗️  Verificando BD para {turma_nome}...")
    
    turma = Turma.query.filter_by(nome=turma_nome).first()
    if not turma:
        print(f"❌ Turma '{turma_nome}' não encontrada no BD")
        return False
        
    questoes = Questao.query.filter_by(turma_id=turma.id).all()
    if not questoes:
        print(f"❌ Nenhuma questão encontrada para '{turma_nome}'")
        return False
        
    # Agrupa por disciplina
    por_disciplina = defaultdict(int)
    for questao in questoes:
        por_disciplina[questao.tema] += 1
        
    print(f"✅ {len(questoes)} questões no BD:")
    for disciplina, count in sorted(por_disciplina.items()):
        print(f"   📚 {disciplina}: {count} questões")
        
    return True

def forcar_reimportacao(turma_nome, arquivo):
    """Força a reimportação de questões"""
    print(f"\n🔄 Forçando reimportação para {turma_nome}...")
    
    # Remove turma existente se houver
    turma = Turma.query.filter_by(nome=turma_nome).first()
    if turma:
        Questao.query.filter_by(turma_id=turma.id).delete()
        db.session.delete(turma)
        db.session.commit()
        print(f"   🗑️  Removida turma existente")
    
    # Importa novamente
    try:
        if turma_nome == 'ensino_medio':
            from app import importar_perguntas_ensino_medio
            importar_perguntas_ensino_medio()
        else:
            ano = turma_nome.split('_')[0]
            from app import importar_perguntas
            importar_perguntas(int(ano), arquivo)
        
        print(f"   ✅ Reimportação concluída")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na reimportação: {e}")
        return False

def main():
    """Função principal de verificação"""
    print("🔍 VERIFICAÇÃO COMPLETA DAS TURMAS E QUESTÕES\n")
    print("=" * 60)
    
    # Lista de verificações
    verificacoes = [
        ('6_ano', 'data/perguntas_6_ano.json'),
        ('7_ano', 'data/perguntas_7_ano.json'), 
        ('8_ano', 'data/perguntas_8_ano.json'),
        ('9_ano', 'data/perguntas_9_ano.json'),
        ('ensino_medio', 'data/perguntas_ensino_medio.json')
    ]
    
    problemas = []
    
    with app.app_context():
        for turma_nome, arquivo in verificacoes:
            print(f"\n{'='*60}")
            print(f"🎯 VERIFICANDO: {turma_nome.upper()}")
            print(f"{'='*60}")
            
            # Verifica arquivo JSON
            arquivo_ok = verificar_arquivo_json(arquivo, turma_nome)
            if not arquivo_ok:
                problemas.append(f"Arquivo {arquivo} com problemas")
                continue
                
            # Verifica BD
            bd_ok = verificar_bd_turma(turma_nome)
            if not bd_ok:
                print(f"⚠️  Problema no BD, tentando reimportar...")
                reimport_ok = forcar_reimportacao(turma_nome, arquivo)
                if reimport_ok:
                    verificar_bd_turma(turma_nome)  # Verifica novamente
                else:
                    problemas.append(f"Falha na reimportação de {turma_nome}")
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📋 RESUMO FINAL")
    print(f"{'='*60}")
    
    if problemas:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"   • {problema}")
    else:
        print("✅ TODAS AS TURMAS ESTÃO FUNCIONANDO CORRETAMENTE!")
        
    print(f"\n🎓 Verificação completa finalizada.")

if __name__ == '__main__':
    main()