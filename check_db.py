#!/usr/bin/env python3
from models import db, Turma, Equipe, Questao
from app import app

with app.app_context():
    print("=== TURMAS ===")
    turmas = Turma.query.all()
    for turma in turmas:
        print(f"ID: {turma.id}, Nome: {turma.nome}")
        equipes = Equipe.query.filter_by(turma_id=turma.id).all()
        print(f"Equipes na turma {turma.nome}:")
        if equipes:
            for equipe in equipes:
                print(f"  - {equipe.nome} ({equipe.cor})")
        else:
            print("  Nenhuma equipe encontrada!")
        
        # Verificar questões
        questoes = Questao.query.filter_by(turma_id=turma.id).all()
        print(f"Questões na turma {turma.nome}: {len(questoes)}")
        if questoes:
            temas = set(q.tema for q in questoes)
            print(f"  Temas: {', '.join(temas)}")
        print()
