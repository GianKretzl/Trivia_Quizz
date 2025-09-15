from app import app

# Listar todas as rotas registradas
print("Rotas registradas no Flask:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint} (métodos: {list(rule.methods)})")

# Verificar especificamente a rota ajustar_pontos
print("\nVerificando rota /api/ajustar_pontos:")
for rule in app.url_map.iter_rules():
    if 'ajustar_pontos' in rule.rule:
        print(f"  Encontrada: {rule.rule} -> {rule.endpoint} (métodos: {list(rule.methods)})")