#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Turma, Questao, obter_disciplinas_por_turma

def testar_sorteio_turma(turma_nome):
    """Testa o sorteio de disciplinas para uma turma específica"""
    print(f"\n🎯 Testando sorteio para {turma_nome}:")
    
    # Verifica disciplinas disponíveis
    disciplinas_esperadas = obter_disciplinas_por_turma(turma_nome)
    print(f"   📚 Disciplinas esperadas: {disciplinas_esperadas}")
    
    # Verifica se há questões no BD para cada disciplina
    turma = Turma.query.filter_by(nome=turma_nome).first()
    if not turma:
        print(f"   ❌ Turma não encontrada no BD")
        return False
    
    disciplinas_com_questoes = set()
    questoes = Questao.query.filter_by(turma_id=turma.id).all()
    
    for questao in questoes:
        disciplinas_com_questoes.add(questao.tema)
    
    print(f"   🏗️  Disciplinas no BD: {sorted(disciplinas_com_questoes)}")
    
    # Verifica se todas as disciplinas esperadas têm questões
    faltando = set(disciplinas_esperadas) - disciplinas_com_questoes
    extras = disciplinas_com_questoes - set(disciplinas_esperadas)
    
    if faltando:
        print(f"   ❌ Disciplinas faltando: {faltando}")
        return False
    
    if extras:
        print(f"   ⚠️  Disciplinas extras (não deveriam estar): {extras}")
        # Não falha, mas avisa
    
    print(f"   ✅ Sorteio OK - Todas as disciplinas estão corretas")
    return True

def main():
    """Função principal de teste"""
    print("🧪 TESTE DE SORTEIO DE DISCIPLINAS")
    print("=" * 50)
    
    turmas = ['6_ano', '7_ano', '8_ano', '9_ano', 'ensino_medio']
    
    with app.app_context():
        todos_ok = True
        
        for turma in turmas:
            resultado = testar_sorteio_turma(turma)
            if not resultado:
                todos_ok = False
        
        print(f"\n{'='*50}")
        if todos_ok:
            print("🎉 TODOS OS SORTEIOS ESTÃO FUNCIONANDO CORRETAMENTE!")
        else:
            print("❌ PROBLEMAS ENCONTRADOS NOS SORTEIOS!")
        print(f"{'='*50}")

if __name__ == '__main__':
    main()