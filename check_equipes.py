from app import app, db, Turma, Equipe

with app.app_context():
    # Verificar qual turma tem equipes
    turma_com_equipes = db.session.query(Turma).join(Equipe).first()
    print(f'Turma com equipes: {turma_com_equipes.nome if turma_com_equipes else "Nenhuma"}')
    
    # Listar todas as equipes
    equipes = Equipe.query.all()
    print(f'Equipes no banco: {[(e.nome, e.turma_id) for e in equipes]}')
    
    # Verificar se a turma das equipes tem questões
    if turma_com_equipes:
        from models import Questao
        questoes = Questao.query.filter_by(turma_id=turma_com_equipes.id).count()
        print(f'Questões na turma {turma_com_equipes.nome}: {questoes}')