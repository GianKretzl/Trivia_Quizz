#!/usr/bin/env python3
from models import db, Turma, Equipe, Rodada
from app import app

with app.app_context():
    print("=== RODADAS NO BANCO ===")
    rodadas = Rodada.query.all()
    if rodadas:
        for rodada in rodadas:
            equipe = Equipe.query.get(rodada.equipe_id)
            print(f"Rodada {rodada.numero}: Equipe {equipe.nome} - Acertou: {rodada.acertou} - Tema: {rodada.tema}")
    else:
        print("Nenhuma rodada encontrada!")
    
    print(f"\nTotal de rodadas: {len(rodadas)}")
    
    print("\n=== PONTUAÇÃO ATUAL ===")
    turma = Turma.query.first()
    if turma:
        equipes = Equipe.query.filter_by(turma_id=turma.id).all()
        for equipe in equipes:
            acertos = Rodada.query.filter_by(equipe_id=equipe.id, acertou=True).count()
            pontos = acertos * 10
            print(f"Equipe {equipe.nome}: {acertos} acertos = {pontos} pontos")
