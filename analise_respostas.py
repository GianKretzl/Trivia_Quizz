import json
import os
from collections import Counter

def analisar_distribuicao_respostas():
    """Analisa a distribuição das respostas corretas em todos os arquivos de perguntas"""
    
    # Lista dos arquivos para analisar
    arquivos = [
        'data/perguntas_6_ano.json',
        'data/perguntas_7_ano.json', 
        'data/perguntas_8_ano.json',
        'data/perguntas_9_ano.json',
        'data/perguntas_ensino_medio.json'
    ]
    
    distribuicao_total = Counter()
    distribuicao_por_arquivo = {}
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"\n=== Analisando {arquivo} ===")
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            distribuicao_arquivo = Counter()
            total_perguntas = 0
            
            # Percorre todas as séries/anos no arquivo
            for serie, disciplinas in data.items():
                for disciplina, perguntas in disciplinas.items():
                    for pergunta in perguntas:
                        resposta_correta = pergunta['resposta_correta']
                        distribuicao_arquivo[resposta_correta] += 1
                        distribuicao_total[resposta_correta] += 1
                        total_perguntas += 1
            
            distribuicao_por_arquivo[arquivo] = distribuicao_arquivo
            
            print(f"Total de perguntas: {total_perguntas}")
            print("Distribuição das respostas corretas:")
            for alt in sorted(distribuicao_arquivo.keys()):
                letra = chr(65 + alt)  # Converte 0->A, 1->B, 2->C, 3->D
                count = distribuicao_arquivo[alt]
                porcentagem = (count / total_perguntas) * 100
                print(f"  Alternativa {letra} (índice {alt}): {count} questões ({porcentagem:.1f}%)")
    
    print(f"\n=== DISTRIBUIÇÃO GERAL ===")
    total_geral = sum(distribuicao_total.values())
    print(f"Total geral de perguntas: {total_geral}")
    print("Distribuição geral das respostas corretas:")
    
    for alt in sorted(distribuicao_total.keys()):
        letra = chr(65 + alt)  # Converte 0->A, 1->B, 2->C, 3->D
        count = distribuicao_total[alt]
        porcentagem = (count / total_geral) * 100
        print(f"  Alternativa {letra} (índice {alt}): {count} questões ({porcentagem:.1f}%)")
    
    # Verifica se há concentração problemática
    print(f"\n=== ANÁLISE ===")
    for alt in sorted(distribuicao_total.keys()):
        letra = chr(65 + alt)
        count = distribuicao_total[alt]
        porcentagem = (count / total_geral) * 100
        
        if porcentagem > 35:
            print(f"⚠️  ATENÇÃO: Alternativa {letra} tem {porcentagem:.1f}% das respostas - muito concentrada!")
        elif porcentagem < 15:
            print(f"⚠️  ATENÇÃO: Alternativa {letra} tem apenas {porcentagem:.1f}% das respostas - muito baixa!")
    
    # Distribuição ideal seria ~25% para cada alternativa
    print(f"\n💡 Distribuição ideal seria aproximadamente 25% para cada alternativa (A, B, C, D)")

if __name__ == "__main__":
    analisar_distribuicao_respostas()