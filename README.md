# ons-coff-downloader

Script para baixar dados de **restrição COFF** (curtailment) fotovoltaico e eólico do ONS (Operador Nacional do Sistema Elétrico), direto do bucket público S3.

---

## Dados disponíveis

| Tipo           | Formato  | Cobertura              |
|----------------|----------|------------------------|
| Fotovoltaica   | Parquet  | Sem limite definido    |
| Eólica         | Parquet  | Out/2023 em diante     |
| Eólica (legado)| CSV      | Jan/2021 – Set/2023    |

Fonte: [ONS Open Data](https://dados.ons.org.br)

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Uso

### Modo interativo

```bash
python ons_api.py
```

O script guia via menu: tipo de dado → anos → meses.

### Modo CLI

```bash
python ons_api.py --tipo <tipo> --anos <anos> --meses <meses>
```

**Parâmetros:**

| Flag      | Aceita                          | Exemplo            |
|-----------|---------------------------------|--------------------|
| `--tipo`  | `fotovoltaica`, `eolica`, `eolica_csv` | `--tipo eolica` |
| `--anos`  | ano único, lista ou intervalo   | `--anos 2023-2025` |
| `--meses` | mês único, lista ou intervalo   | `--meses 1-12`     |

**Exemplos:**

```bash
# Eólica Parquet, ano completo de 2024
python ons_api.py --tipo eolica --anos 2024 --meses 1-12

# Fotovoltaica, meses específicos de 2023 e 2024
python ons_api.py --tipo fotovoltaica --anos 2023,2024 --meses 1,3,6,12

# Eólica CSV (legado), período completo disponível
python ons_api.py --tipo eolica_csv --anos 2021-2023 --meses 1-12
```

---

## Estrutura de saída

Os arquivos são salvos em subpastas por ano:

```
dados_fotovoltaica/
└── 2024/
    ├── RESTRICAO_COFF_FOTOVOLTAICA_2024_01.parquet
    ├── RESTRICAO_COFF_FOTOVOLTAICA_2024_02.parquet
    └── ...

dados_eolica/
└── 2024/
    ├── RESTRICAO_COFF_EOLICA_2024_01.parquet
    └── ...
```

---

## Leitura dos dados com pandas

```python
import pandas as pd
from pathlib import Path

# Parquet (fotovoltaica ou eólica)
df = pd.read_parquet("dados_fotovoltaica/")

# CSV (eólica legado)
df = pd.concat([pd.read_csv(f) for f in Path("dados_eolica").rglob("*.csv")])
```

---

## Dependências

```
requests
```

> `pandas` e `pyarrow` são necessários apenas para leitura posterior dos arquivos baixados, não para o download em si.