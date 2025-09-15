import requests
import json

# Testar a API de ajustar pontos
try:
    response = requests.post('http://127.0.0.1:5000/api/ajustar_pontos', 
                           json={'equipe': 'Equipe LARANJA', 'pontos': 1},
                           headers={'Content-Type': 'application/json'})
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")
    
    if response.status_code == 404:
        print("\n=== ERRO 404 DETECTADO ===")
        print("Vamos tentar listar todas as rotas disponíveis:")
        
        # Testar uma rota que sabemos que existe
        test_response = requests.get('http://127.0.0.1:5000/api/estado_jogo')
        print(f"Teste rota existente: {test_response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("Servidor não está rodando")
except Exception as e:
    print(f"Erro: {e}")