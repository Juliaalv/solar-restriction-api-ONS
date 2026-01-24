"""
API para acessar dados Parquet do ONS
"""

from fastapi import FastAPI
import pandas as pd
import requests
from pathlib import Path
import tempfile

app = FastAPI(title="ONS API")

# Cache local
CACHE_DIR = Path(tempfile.gettempdir()) / "ons_data"
CACHE_DIR.mkdir(exist_ok=True)

S3_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/restricao_coff_fotovoltaica_tm"


def get_file(year: int, month: int) -> Path:
    """Baixa ou retorna arquivo do cache"""
    filename = f"RESTRICAO_COFF_FOTOVOLTAICA_{year}_{month:02d}.parquet"
    local_path = CACHE_DIR / filename
    
    if not local_path.exists():
        url = f"{S3_URL}/{filename}"
        response = requests.get(url)
        response.raise_for_status()
        local_path.write_bytes(response.content)
    
    return local_path


@app.get("/dados")
async def dados(year: int, month: int, limite: int = None):
    """Retorna dados em JSON"""
    local_path = get_file(year, month)
    df = pd.read_parquet(local_path)
    
    if limite:
        df = df.head(limite)
    
    return {
        "periodo": f"{year}-{month:02d}",
        "total": len(df),
        "colunas": list(df.columns),
        "dados": df.to_dict('records')
    }


@app.get("/info")
async def info(year: int, month: int):
    """Informações sobre o arquivo"""
    local_path = get_file(year, month)
    df = pd.read_parquet(local_path)
    
    return {
        "periodo": f"{year}-{month:02d}",
        "linhas": len(df),
        "colunas": list(df.columns)
    }


@app.get("/")
async def root():
    """Info da API"""
    return {
        "api": "ONS Parquet",
        "endpoints": {
            "/dados?year=2025&month=12": "Dados em JSON",
            "/info?year=2025&month=12": "Info do arquivo",
            "/docs": "Documentação"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
