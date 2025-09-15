#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

# Adiciona o diretório do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Turma, Questao

def corrigir_6_ano():
    """Corrige especificamente o problema do 6º ano"""
    print("🔧 CORRIGINDO PROBLEMA DO 6º ANO")
    print("=" * 50)
    
    with app.app_context():
        # Remove todas as questões incorretas do 6º ano
        turma_6 = Turma.query.filter_by(nome='6_ano').first()
        if turma_6:
            count_removidas = Questao.query.filter_by(turma_id=turma_6.id).count()
            Questao.query.filter_by(turma_id=turma_6.id).delete()
            db.session.delete(turma_6)
            db.session.commit()
            print(f"✅ Removidas {count_removidas} questões incorretas do 6º ano")
        
        # Reimporta as questões corretas
        from app import importar_perguntas_6ano
        importar_perguntas_6ano()
        
        # Verifica se foi importado corretamente
        turma_6_nova = Turma.query.filter_by(nome='6_ano').first()
        if turma_6_nova:
            questoes_novas = Questao.query.filter_by(turma_id=turma_6_nova.id).all()
            print(f"✅ 6º ano corrigido com {len(questoes_novas)} questões")
            
            # Mostra distribuição por disciplina
            from collections import defaultdict
            por_disciplina = defaultdict(int)
            for questao in questoes_novas:
                por_disciplina[questao.tema] += 1
                
            print("📚 Disciplinas corretas do 6º ano:")
            for disciplina, count in sorted(por_disciplina.items()):
                print(f"   • {disciplina}: {count} questões")
        
        print("\n🎯 Correção do 6º ano finalizada!")

if __name__ == '__main__':
    corrigir_6_ano()