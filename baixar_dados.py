"""
Baixa arquivos Parquet do ONS 
"""

import requests
from pathlib import Path

# Criar pasta para salvar os arquivos
pasta = Path("dados_ons")
pasta.mkdir(exist_ok=True)

# URL base
S3_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_fotovoltaica_tm"

meses_nomes = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# ============================================================
# OPÇÃO 1: Input do Usuário 
# ============================================================

print("=" * 70)
print("Baixador de Arquivos Parquet - ONS")
print("=" * 70)

# Pedir ano
while True:
    try:
        ano = int(input("\nQual ano você quer? (ex: 2025): "))
        if ano < 2020 or ano > 2030:
            print("❌ Ano deve estar entre 2020 e 2030")
            continue
        break
    except ValueError:
        print("❌ Digite um número válido")

# Pedir meses
print("\nQual mês você quer?")
print("Opções:")
print("  1 - Um mês específico")
print("  2 - Vários meses")
print("  3 - Todos os meses (1-12)")

while True:
    try:
        opcao = int(input("\nEscolha (1/2/3): "))
        if opcao not in [1, 2, 3]:
            print("❌ Digite 1, 2 ou 3")
            continue
        break
    except ValueError:
        print("❌ Digite um número válido")

meses = []

if opcao == 1:
    # Um mês específico
    while True:
        try:
            mes = int(input(f"Qual mês? (1-12): "))
            if mes < 1 or mes > 12:
                print("❌ Mês deve estar entre 1 e 12")
                continue
            meses = [mes]
            break
        except ValueError:
            print("❌ Digite um número válido")

elif opcao == 2:
    # Vários meses
    print("\nDigite os meses separados por vírgula")
    print("Exemplo: 1,2,3 ou 1,5,9,12")
    while True:
        try:
            entrada = input("\nMeses (1-12): ")
            meses = [int(m.strip()) for m in entrada.split(",")]
            
            # Validar
            invalidos = [m for m in meses if m < 1 or m > 12]
            if invalidos:
                print(f"❌ Meses inválidos: {invalidos}")
                continue
            
            # Remover duplicatas e ordenar
            meses = sorted(set(meses))
            break
        except ValueError:
            print("❌ Digite números válidos separados por vírgula")

else:  # opcao == 3
    # Todos os meses
    meses = list(range(1, 13))

# ============================================================
# Começar download
# ============================================================

print("\n" + "=" * 70)
print(f"Baixando {len(meses)} arquivo(s) de {ano}")
print("=" * 70)

arquivos_baixados = []
total_tamanho = 0
erros = 0

# Criar subpasta com ano
pasta_ano = pasta / str(ano)
pasta_ano.mkdir(exist_ok=True)

# Baixar cada mês
for mes in meses:
    filename = f"RESTRICAO_COFF_FOTOVOLTAICA_{ano}_{mes:02d}.parquet"
    url = f"{S3_URL}/{filename}"
    
    filepath = pasta_ano / filename
    
    try:
        print(f"[{meses.index(mes)+1}/{len(meses)}] {meses_nomes[mes]:10s} ({ano}-{mes:02d})...", end=" ", flush=True)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # Salvar arquivo
        filepath.write_bytes(response.content)
        
        tamanho_mb = filepath.stat().st_size / (1024 * 1024)
        total_tamanho += tamanho_mb
        arquivos_baixados.append(filepath)
        
        print(f"✓ ({tamanho_mb:.1f} MB)")
        
    except Exception as e:
        erros += 1
        print(f"✗ Erro: {e}")

# ============================================================
# Resumo
# ============================================================

print("\n" + "=" * 70)
print("Resumo:")
print(f"  Ano: {ano}")
print(f"  Meses: {len(meses)}")
print(f"  Sucesso: {len(arquivos_baixados)}")
print(f"  Erros: {erros}")
print(f"  Tamanho total: {total_tamanho:.1f} MB")
print(f"  Pasta: {pasta_ano.absolute()}")
print("=" * 70)

# Baixar cada mês
for mes in range(1, 13):
    filename = f"RESTRICAO_COFF_FOTOVOLTAICA_2025_{mes:02d}.parquet"
    url = f"{S3_URL}/{filename}"
    
    filepath = pasta / filename
    
    try:
        print(f"[{mes:2d}/12] Baixando {meses_nomes[mes]:10s}...", end=" ", flush=True)
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # Salvar arquivo
        filepath.write_bytes(response.content)
        
        tamanho_mb = filepath.stat().st_size / (1024 * 1024)
        total_tamanho += tamanho_mb
        arquivos_baixados.append(filepath)
        
        print(f"✓ ({tamanho_mb:.1f} MB)")
        
    except Exception as e:
        print(f"✗ Erro: {e}")

print(f"\nTotal baixado: {total_tamanho:.1f} MB")
