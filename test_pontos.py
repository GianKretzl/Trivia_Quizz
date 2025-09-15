import requests
import json

# Testar remover ponto
try:
    response = requests.post('http://127.0.0.1:5000/api/ajustar_pontos', 
                           json={'equipe': 'Equipe LARANJA', 'pontos': -1},
                           headers={'Content-Type': 'application/json'})
    
    print(f"Teste REMOVER ponto:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Erro: {e}")

# Testar adicionar ponto novamente
try:
    response = requests.post('http://127.0.0.1:5000/api/ajustar_pontos', 
                           json={'equipe': 'Equipe LARANJA', 'pontos': 1},
                           headers={'Content-Type': 'application/json'})
    
    print(f"\nTeste ADICIONAR ponto:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Erro: {e}")