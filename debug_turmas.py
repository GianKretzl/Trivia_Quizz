from models import db, Turma, Questao
from app import app

with app.app_context():
    print('=== TODAS AS TURMAS ===')
    turmas = Turma.query.all()
    for t in turmas:
        print(f'  ID {t.id}: {t.nome}')
    
    print('\n=== QUESTÕES POR TURMA ===')
    questoes = Questao.query.all()
    for turma_id in set(q.turma_id for q in questoes):
        turma = Turma.query.get(turma_id)
        turma_nome = turma.nome if turma else 'TURMA_INEXISTENTE'
        count = len([q for q in questoes if q.turma_id == turma_id])
        print(f'  Turma ID {turma_id} ({turma_nome}): {count} questões')