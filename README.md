# API ONS Fotovoltaica

API para acessar dados Parquet do ONS, caso queira usar para eólica necessário alterar os parâmetros.

## Setup

```bash
pip install -r requirements.txt
python ons_api.py
```

API rodará em: `http://localhost:8000`

## Endpoints

### 1. Dados
```
GET /dados?year=2025&month=12&limite=100
```
Retorna dados em JSON.

### 2. Info
```
GET /info?year=2025&month=12
```
Retorna informações do arquivo (linhas, colunas).

### 3. Root
```
GET /
```
Info da API.
