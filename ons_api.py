"""
Baixa arquivos do ONS - RESTRICAO COFF (fotovoltaica ou eolica)
"""

import requests
from pathlib import Path
import sys

def main(tipo=None, ano=None, meses=None):
    """
    Baixa arquivos Parquet do ONS
    
    Args:
        tipo: 'fotovoltaica' ou 'eolica'
        ano: Ano a baixar
        meses: Lista de meses
    """
    
    # Configuração por tipo
    config = {
        "fotovoltaica": {
            "url": "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_fotovoltaica_tm",
            "pasta": "dados_fotovoltaica",
            "prefixo": "RESTRICAO_COFF_FOTOVOLTAICA"
        },
        "eolica": {
            "url": "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_eolica_tm",
            "pasta": "dados_eolica",
            "prefixo": "RESTRICAO_COFF_EOLICA"
        }
    }
    
    # Pedir tipo se não especificado
    if tipo is None:
        print("\nQual tipo de dado?")
        print("  1 - Fotovoltaica")
        print("  2 - Eólica")
        opcao = input("Escolha (1 ou 2): ")
        
        if opcao == "1":
            tipo = "fotovoltaica"
        elif opcao == "2":
            tipo = "eolica"
        else:
            print("❌ Opção inválida")
            return
    
    # Validar tipo
    tipo = tipo.lower()
    if tipo not in config:
        print(f"❌ Tipo deve ser: fotovoltaica ou eolica")
        print(f"Digite: python baixar_ons.py --tipo eolica --ano 2025 --meses 1-12")
        return
    
    # Obter configuração
    cfg = config[tipo]
    pasta = Path(cfg["pasta"])
    pasta.mkdir(exist_ok=True)
    
    S3_URL = cfg["url"]
    PREFIXO = cfg["prefixo"]
    
    # Nomes dos meses
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    # Input se não especificado
    if ano is None:
        try:
            ano = int(input(f"\nQual ano você quer? (ex: 2025): "))
        except ValueError:
            print("❌ Ano inválido")
            return
    
    if meses is None:
        print("\nQuais meses?")
        print("Opções: 1,2,3 ou 1-12")
        entrada = input("Meses: ")
        
        # Processar entrada
        if "-" in entrada:
            # Intervalo (1-12)
            partes = entrada.split("-")
            inicio = int(partes[0].strip())
            fim = int(partes[1].strip())
            meses = list(range(inicio, fim + 1))
        else:
            # Lista (1,2,3)
            meses = [int(m.strip()) for m in entrada.split(",")]
    
    # Validar meses
    meses = sorted(set([m for m in meses if 1 <= m <= 12]))
    
    if not meses:
        print("❌ Nenhum mês válido")
        return
    
    # Criar pasta do ano
    pasta_ano = pasta / str(ano)
    pasta_ano.mkdir(exist_ok=True)
    
    # ========================================================
    # Começar download
    # ========================================================
    
    print("\n" + "=" * 70)
    print(f"Baixando {len(meses)} arquivo(s)")
    print(f"  Tipo: {tipo.upper()}")
    print(f"  Ano: {ano}")
    print(f"  Meses: {len(meses)}")
    print("=" * 70)
    
    arquivos_ok = 0
    erros = 0
    total_tamanho = 0
    
    for idx, mes in enumerate(meses, 1):
        filename = f"{PREFIXO}_{ano}_{mes:02d}.parquet"
        url = f"{S3_URL}/{filename}"
        filepath = pasta_ano / filename
        
        try:
            print(f"[{idx}/{len(meses)}] {meses_nomes[mes]:10s} ({ano}-{mes:02d})...", end=" ", flush=True)
            
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            filepath.write_bytes(response.content)
            
            tamanho_mb = filepath.stat().st_size / (1024 * 1024)
            total_tamanho += tamanho_mb
            arquivos_ok += 1
            
            print(f"✓ ({tamanho_mb:.1f} MB)")
            
        except Exception as e:
            erros += 1
            print(f"✗ {e}")
    
    # ========================================================
    # Resumo
    # ========================================================
    
    print("\n" + "=" * 70)
    print(f"Resumo:")
    print(f"  Tipo: {tipo.upper()}")
    print(f"  Ano: {ano}")
    print(f"  Sucesso: {arquivos_ok}/{len(meses)}")
    print(f"  Erros: {erros}")
    print(f"  Tamanho total: {total_tamanho:.1f} MB")
    print(f"  Pasta: {pasta_ano.absolute()}")
    print("=" * 70)
    
    # Próximos passos
    if arquivos_ok > 0:
        print(f"\n Próximos passos:")
        print(f"1. python salvar_em_csv.py")
        print(f"2. Analisar com pandas:")
        print(f"   import pandas as pd")
        print(f"   df = pd.read_parquet('{pasta_ano}/RESTRICAO_COFF_{tipo.upper()}_*')")


if __name__ == "__main__":
    tipo = None  
    ano = None
    meses = None
    
    # Processar argumentos da linha de comando
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--tipo" and i + 1 < len(sys.argv):
            tipo = sys.argv[i + 1].lower()
            i += 2
        elif arg == "--ano" and i + 1 < len(sys.argv):
            ano = int(sys.argv[i + 1])
            i += 2
        elif arg == "--meses" and i + 1 < len(sys.argv):
            meses_str = sys.argv[i + 1]
            
            if "-" in meses_str:
                # Intervalo
                inicio, fim = meses_str.split("-")
                meses = list(range(int(inicio), int(fim) + 1))
            else:
                # Lista
                meses = [int(m.strip()) for m in meses_str.split(",")]
            i += 2
        else:
            i += 1
    
    main(tipo=tipo, ano=ano, meses=meses)
