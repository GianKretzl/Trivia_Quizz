from app import app, db
from models import Turma, Equipe

with app.app_context():
    print("=== TURMAS DISPONÍVEIS ===")
    turmas = Turma.query.all()
    for turma in turmas:
        equipes_count = Equipe.query.filter_by(turma_id=turma.id).count()
        print(f"ID: {turma.id}, Nome: {turma.nome}, Equipes: {equipes_count}")
    
    print("\n=== CONFIGURANDO TURMA ATIVA ===")
    # Usar turma 6_ano que tem equipes
    turma_6ano = Turma.query.filter_by(nome='6_ano').first()
    if turma_6ano:
        print(f"Definindo turma '{turma_6ano.nome}' como ativa")
        
        # Vamos criar uma configuração no banco ou usar sessão
        # Por enquanto, vamos modificar a lógica do app.py
        equipes = Equipe.query.filter_by(turma_id=turma_6ano.id).all()
        print(f"Equipes encontradas na turma {turma_6ano.nome}:")
        for equipe in equipes:
            print(f"  - {equipe.nome} ({equipe.cor})")
    else:
        print("Turma 6_ano não encontrada!")
