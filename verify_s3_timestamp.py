"""
Verifica se os arquivos CDC no S3 contêm a coluna DtAtualizacao
"""
import boto3
import pandas as pd
from dotenv import load_dotenv
import os
from io import BytesIO

# Carrega credenciais
load_dotenv()

# Cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

print("=" * 70)
print("VERIFICANDO COLUNA DtAtualizacao NOS ARQUIVOS CDC NO S3")
print("=" * 70)

# Arquivos CDC mais recentes que foram enviados
files = [
    'upcell/cdc/clientes/clientes_20251003_163731.parquet',
    'upcell/cdc/produtos/produtos_20251003_163731.parquet',
    'upcell/cdc/transacoes/transacoes_20251003_163733.parquet',
    'upcell/cdc/transacao_produto/transacao_produto_20251003_163734.parquet'
]

for key in files:
    try:
        # Baixa o arquivo do S3
        obj = s3.get_object(Bucket='meudatalake-raw', Key=key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        
        filename = key.split('/')[-1]
        has_dt = 'DtAtualizacao' in df.columns
        
        print(f"\n📁 {filename}")
        print(f"   Colunas: {list(df.columns)}")
        print(f"   {'✅' if has_dt else '❌'} DtAtualizacao presente: {has_dt}")
        
        if has_dt:
            print(f"   📅 Sample: {df['DtAtualizacao'].iloc[0]}")
        
    except Exception as e:
        print(f"\n❌ {key}")
        print(f"   ERRO: {e}")

print("\n" + "=" * 70)
